from collections import defaultdict
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape



def generate_correct_year_form(num):
        if (4 < num) and (num < 21):
            return 'лет'
        if (num % 10) == 1:
            return 'год'
        if (1 < (num % 10)) and ((num % 10) < 5):
            return 'года'
        return 'лет'


def main():
    load_dotenv()
    env = Environment(
        loader=FileSystemLoader(os.path.dirname(os.path.abspath(__file__))),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')
    company_foundation_year = 1920

    excel_data_df = pd.read_excel(
        os.environ['EXCEL_FILE'],
        keep_default_na=False,
        na_values='dummy',
        ).to_dict(orient='records')

    group_by_category_products = defaultdict(list)

    for item in excel_data_df:
        category = item.get('Категория')
        group_by_category_products[category].append(item)

    company_age = datetime.now().year - company_foundation_year

    rendered_page = template.render(
        company_age=company_age,
        correct_year_form=generate_correct_year_form(company_age),
        data_from_excel=group_by_category_products,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()
