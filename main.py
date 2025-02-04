from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections

excel_wine_data = pandas.read_excel('wine3.xlsx', na_values=['N/A', 'NA'], keep_default_na=False)
excel_data_wine_dict = excel_wine_data.to_dict(orient='records')
wine_dict = collections.defaultdict(list)

for wine in excel_data_wine_dict:
    wine_dict[wine['Категория']].append(wine)


start_date = datetime.datetime(year=1920, month=1, day=1)
end_date = datetime.datetime(year=2023, month=1, day=1)
day_in_year = 365
delta = end_date-start_date
final_year = int(delta.days/day_in_year)


def year_check(year):

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
    year_title=f'{final_year} {year_check(final_year)}',
    white_wines=wine_dict["Белые вина"],
    red_wines=wine_dict["Красные вина"],
    drinks=wine_dict["Напитки"]
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
