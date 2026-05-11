from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, func, Integer, MetaData, String, Table, Text

metadata = MetaData()

abilities = Table(
    'abilities',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False, unique=True),
)

article_pokemon_moves = Table(
    'article_pokemon_moves',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('article_pokemon_id', Integer, ForeignKey('article_pokemons.id', ondelete='CASCADE'), nullable=False, index=True),
    Column('move_id', Integer, ForeignKey('moves.id'), index=True)
)

article_pokemons = Table(
    'article_pokemons',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('article_id', Integer, ForeignKey('articles.id', ondelete='CASCADE'), nullable=False, index=True),
    Column('pokemon_id', Integer, ForeignKey('pokemons.id'), index=True),
    Column('item_id', Integer, ForeignKey('items.id'), index=True),
    Column('tera_type_id', Integer, ForeignKey('types.id'), index=True),
    Column('ability_id', Integer, ForeignKey('abilities.id'), index=True),
    Column('nature_id', Integer, ForeignKey('natures.id'), index=True),
    Column('ev_h', Integer, index=True),
    Column('ev_a', Integer, index=True),
    Column('ev_b', Integer, index=True),
    Column('ev_c', Integer, index=True),
    Column('ev_d', Integer, index=True),
    Column('ev_s', Integer, index=True)
)

articles = Table(
    'articles',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('url', Text, nullable=False),
    Column('title', Text, nullable=False),
    Column('text', Text),
    Column('trainer_name', String(255), nullable=False),
    Column('rule', String(6), nullable=False, index=True),
    Column('season', String(255), index=True),
    Column('regulation', String(255), index=True),
    Column('rank', Integer, index=True),
    Column('rate', Float, index=True),
    Column('created_at', DateTime, server_default=func.now(), nullable=False, index=True),
    Column('deleted_at', DateTime)
)

article_tags = Table(
    'article_tags',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('article_id', Integer, ForeignKey('articles.id', ondelete='CASCADE'), nullable=False, index=True),
    Column('tag_id', Integer, ForeignKey('tags.id', ondelete='CASCADE'), nullable=False, index=True)
)

items = Table(
    'items',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False, unique=True)
)

moves = Table(
    'moves',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False, unique=True)
)

natures = Table(
    'natures',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False, unique=True)
)

pokemons = Table(
    'pokemons',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False, unique=True)
)

regulations = Table(
    'regulations',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False, unique=True),
    Column('sort_order', Integer, nullable=False, unique=True)
)

seasons = Table(
    'seasons',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False, unique=True),
    Column('sort_order', Integer, nullable=False, unique=True)
)

tags = Table(
    'tags',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False, unique=True),
    Column('is_category', Boolean, nullable=False)
)

trends = Table(
    'trends',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False, unique=True)
)

types = Table(
    'types',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False, unique=True)
)
