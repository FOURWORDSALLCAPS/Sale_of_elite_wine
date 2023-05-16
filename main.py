from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

products = pandas.read_excel('wine3.xlsx', keep_default_na=False).to_dict(orient='records')

products_by_categories = collections.defaultdict(list)
for product in products:
    products_by_categories[product['Категория']].append(product)


def count_age():
    today = datetime.datetime.now()
    test = today.year
    delta = test - 1920
    return delta


def spell_check():
    year = 'лет'
    if (count_age() // 10) % 10 != 1:
        if count_age() % 10 == 1:
            year = 'год'
        elif count_age() % 10 in (2, 3, 4):
            year = 'года'
    return year


rendered_pages = template.render(
    age=f"Уже {count_age()} {spell_check()} с вами",
    products_by_categories=products_by_categories
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_pages)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
