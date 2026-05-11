import json
from sqlalchemy.dialects.sqlite import insert
from database.connection import engine
from database.schema import moves
from utils.helpers import kata_to_hira


move_data = {
    'list': []
}

with open('static/txt/moves.txt', 'r', encoding='utf-8') as f:
    rows = [line.rstrip('\n') for line in f if line != '\n']

for row in rows:
    name, _, pp = row.split(',')
    move_data['list'].append({
        'label': name,
        'keywords': list({name, kata_to_hira(name)}),
        'pp': pp
    })

with open('static/json/moves.json', 'w', encoding='utf-8') as f:
    json.dump(move_data, f, ensure_ascii=False, indent=4)

stmt = insert(moves).on_conflict_do_nothing(index_elements=['name'])

with engine.begin() as conn:
    conn.execute(stmt, [{'name': move['label']} for move in move_data['list']])
