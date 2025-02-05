import datetime
import pandas
import collections
import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape


def check_year(year):

    last_two_num = year % 100
    last_num = year % 10

    if 11 <= last_two_num <= 19:
        return "лет"
    elif last_num == 1:
        return "год"
    elif 2 <= last_num <= 4:
        return "года"
    else:
        return "лет"


def main():

    parser = argparse.ArgumentParser(description='Путь к файлу с напитками')
    parser.add_argument('file', nargs='?', help='Ваш файл', default='wine3.xlsx')
    args = parser.parse_args()

    excel_drinks_data = pandas.read_excel(args.file, na_values=['N/A', 'NA'], keep_default_na=False)
    drinks_data = excel_drinks_data.to_dict(orient='records')
    drinks_collection = collections.defaultdict(list)

    for wine in drinks_data:
        drinks_collection[wine['Категория']].append(wine)

    drink_categories = [drink for drink in drinks_collection]


    start_date = datetime.datetime(year=1920, month=1, day=1)
    end_date = datetime.datetime.today()
    day_in_year = 365
    delta = end_date-start_date
    final_year = int(delta.days/day_in_year)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        year_title=f'{final_year} {check_year(final_year)}',
        drinks_collection=drinks_collection,
        categories = drinks_collection.keys()
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()