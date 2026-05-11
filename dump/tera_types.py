import json
import os
from sqlalchemy.dialects.sqlite import insert
from database.connection import engine
from database.schema import types
from utils.helpers import kata_to_hira


tera_type_data = {
    'image': {
        'path': 'https://storage.googleapis.com/pocket-square/tera-type/',
        'extension': '.png',
        'size': [26, 36],
        'style': {
            'padding': '5px 0'
        }
    },
    'list': []
}

for file in os.listdir('static/image/tera-type'):
    name = file.rstrip('.png')
    tera_type_data['list'].append({
        'label': name,
        'keywords': list({name, kata_to_hira(name)}),
    })

with open('static/json/tera_types.json', 'w', encoding='utf-8') as f:
    json.dump(tera_type_data, f, ensure_ascii=False, indent=4)

stmt = insert(types).on_conflict_do_nothing(index_elements=['name'])

with engine.begin() as conn:
    conn.execute(stmt, [{'name': tera_type['label']} for tera_type in tera_type_data['list']])
