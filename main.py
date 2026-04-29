from collections import defaultdict
import pandas as pd
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('/path/to/work/dir/'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')
YEAR_OF_FOUNDATION = 1920


def generate_correct_year_form(num):
    if (4 < num) and (num < 21):
        return 'лет'
    if (num % 10) == 1:
        return 'год'
    if (1 < (num % 10)) and ((num % 10) < 5):
        return 'года'
    return 'лет'


excel_data_df = pd.read_excel(
    'wine3.xlsx',
    keep_default_na=False,
    na_values='dummy',
    ).to_dict(orient='records')

dict_of_lists = defaultdict(list)

for item in excel_data_df:
    category = item.get('Категория')
    dict_of_lists[category].append(item)

formatted_year = datetime.now().year - YEAR_OF_FOUNDATION

rendered_page = template.render(
    age_of_the_company=formatted_year,
    year_form=generate_correct_year_form(formatted_year),
    data_from_excel=dict_of_lists,
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
