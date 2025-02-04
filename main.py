from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections
import argparse


parser = argparse.ArgumentParser(description='Путь к файлу')
parser.add_argument('url', help='Ваш файл')
args = parser.parse_args()

user_input = args.url


excel_drinks_data = pandas.read_excel(user_input, na_values=['N/A', 'NA'], keep_default_na=False)
drinks_data = excel_drinks_data.to_dict(orient='records')
drinks_collection = collections.defaultdict(list)

for wine in drinks_data:
    drinks_collection[wine['Категория']].append(wine)

type_drink = []

for drink in drinks_collection:
    type_drink.append(drink)


start_date = datetime.datetime(year=1920, month=1, day=1)
end_date = datetime.datetime(year=2023, month=1, day=1)
day_in_year = 365
delta = end_date-start_date
final_year = int(delta.days/day_in_year)


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


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(
    year_title=f'{final_year} {check_year(final_year)}',
    white_wines=drinks_collection[type_drink[0]],
    drinks=drinks_collection[type_drink[1]],
    red_wines=drinks_collection[type_drink[2]]
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
