import json
import os
from sqlalchemy.dialects.sqlite import insert
from database.connection import engine
from database.schema import items
from utils.helpers import kata_to_hira


item_data = {
    'image': {
        'path': 'https://storage.googleapis.com/pocket-square/item/',
        'extension': '.png',
        'size': [26, 36],
        'style': {
            'padding': '5px 0'
        }
    },
    'list': []
}

for file in os.listdir('static/image/item'):
    name = file.rstrip('.png')
    item_data['list'].append({
        'label': name,
        'keywords': list({name, kata_to_hira(name)}),
    })

with open('static/json/items.json', 'w', encoding='utf-8') as f:
    json.dump(item_data, f, ensure_ascii=False, indent=4)

stmt = insert(items).on_conflict_do_nothing(index_elements=['name'])

with engine.begin() as conn:
    conn.execute(stmt, [{'name': item['label']} for item in item_data['list']])
