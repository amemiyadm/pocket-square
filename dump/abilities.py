import json
from sqlalchemy.dialects.sqlite import insert
from database.connection import engine
from database.schema import abilities
from utils.helpers import kata_to_hira


with open('static/txt/abilities.txt', 'r', encoding='utf-8') as f:
    rows = list(dict.fromkeys(line.rstrip('\n') for line in f if line != '\n'))

ability_data = {
    'list': [
        {'label': row, 'keywords': list({row, kata_to_hira(row)})}
        for row in rows
    ]
}

with open('static/json/abilities.json', 'w', encoding='utf-8') as f:
    json.dump(ability_data, f, ensure_ascii=False, indent=4)

stmt = insert(abilities).on_conflict_do_nothing(index_elements=['name'])

with engine.begin() as conn:
    conn.execute(stmt, [{'name': ability['label']} for ability in ability_data['list']])
