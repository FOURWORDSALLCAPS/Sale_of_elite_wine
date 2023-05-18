from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections
import argparse


def count_age():
    today = datetime.datetime.now()
    year_now = today.year
    foundation_year = 1920
    age = year_now - foundation_year
    return age


def get_year(age):
    year = 'лет'
    if (age // 10) % 10 != 1:
        if age % 10 == 1:
            year = 'год'
        elif age % 10 in (2, 3, 4):
            year = 'года'
    return year


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    arguments = argparse.ArgumentParser(
        description='Сайт магазина авторского вина "Новое русское вино"'
    )
    arguments.add_argument('-d', default='default.xlsx', help='Введите название вашего .xlsx файла')
    arguments = arguments.parse_args()

    products = pandas.read_excel(f'{arguments.d}', keep_default_na=False).to_dict(orient='records')

    products_by_categories = collections.defaultdict(list)

    for product in products:
        products_by_categories[product['Категория']].append(product)

    age = count_age()

    rendered_pages = template.render(
        age=f"Уже {age} {get_year(age)} с вами",
        products_by_categories=products_by_categories
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_pages)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
