from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections
import argparse


def count_age():
    today = datetime.datetime.now()
    year_now = today.year
    year_of_foundation = 1920
    delta = year_now - year_of_foundation
    return delta


def get_year():
    calculated_year = count_age()
    year = 'лет'
    if (calculated_year // 10) % 10 != 1:
        if calculated_year % 10 == 1:
            year = 'год'
        elif calculated_year % 10 in (2, 3, 4):
            year = 'года'
    return year


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    parser = argparse.ArgumentParser(
        description='Сайт магазина авторского вина "Новое русское вино"'
    )
    parser.add_argument('-d', default='default.xlsx', help='Введите название вашего .xlsx файла')
    parser = parser.parse_args()

    products = pandas.read_excel(f'{parser.d}', keep_default_na=False).to_dict(orient='records')

    products_by_categories = collections.defaultdict(list)

    for product in products:
        products_by_categories[product['Категория']].append(product)

    rendered_pages = template.render(
        age=f"Уже {count_age()} {get_year()} с вами",
        products_by_categories=products_by_categories
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_pages)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
