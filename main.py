from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas


excel_data_df = pandas.read_excel('wine.xlsx')
titles = excel_data_df['Название'].tolist()
varietys = excel_data_df['Сорт'].tolist()
prices = excel_data_df['Цена'].tolist()
images = excel_data_df['Картинка'].tolist()


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')


def count_age():
    today = datetime.datetime.now()
    test = today.year
    delta = test - 1920
    return delta


wines = []

for title in titles:
    wines.append({
        "title": f"{}",
        "variety": f"{}",
        "price": f"{}",
        "image": f"{}"
    }
)


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
    wines=wines
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_pages)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
