import json
from sqlalchemy.dialects.sqlite import insert
from database.connection import engine
from database.schema import natures
from utils.helpers import kata_to_hira


with open('static/txt/natures.txt', 'r', encoding='utf-8') as f:
    rows = list(dict.fromkeys(line.rstrip('\n') for line in f if line != '\n'))

nature_data = {
    'list': [
        {'label': row, 'keywords': list({row, kata_to_hira(row)})}
        for row in rows
    ]
}

with open('static/json/natures.json', 'w', encoding='utf-8') as f:
    json.dump(nature_data, f, ensure_ascii=False, indent=4)

stmt = insert(natures).on_conflict_do_nothing(index_elements=['name'])

with engine.begin() as conn:
    conn.execute(stmt, [{'name': nature['label']} for nature in nature_data['list']])
