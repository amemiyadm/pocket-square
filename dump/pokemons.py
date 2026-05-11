import json
import os
from sqlalchemy.dialects.sqlite import insert
from database.connection import engine
from database.schema import pokemons
from utils.helpers import kata_to_hira

pokemon_data = {
    'image': {
        'path': 'https://storage.googleapis.com/pocket-square/pokemon/',
        'extension': '.png',
        'size': [36, 36]
    },
    'list': []
}

for file in os.listdir('static/image/pokemon'):
    name = file.rstrip('.png')
    pokemon_data['list'].append({
        'label': name,
        'keywords': list({name, kata_to_hira(name)}),
    })

with open('static/json/pokemons.json', 'w', encoding='utf-8') as f:
    json.dump(pokemon_data, f, ensure_ascii=False, indent=4)

stmt = insert(pokemons).on_conflict_do_nothing(index_elements=['name'])

with engine.begin() as conn:
    conn.execute(stmt, [{'name': pokemon['label']} for pokemon in pokemon_data['list']])
