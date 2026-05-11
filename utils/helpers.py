import os
from flask import current_app, url_for
from sqlalchemy import asc, desc, func, select
from database.schema import articles, article_pokemons, pokemons, regulations, seasons, tags, trends


def get_all_regulations(conn):
    return tuple(
        {'name': row.name, 'sort_order': row.sort_order}
        for row in conn.execute(
            select(regulations.c.name, regulations.c.sort_order).order_by(desc(regulations.c.sort_order))
        )
    )


def get_all_seasons(conn):
    return tuple(
        {'name': row.name, 'sort_order': row.sort_order}
        for row in conn.execute(
            select(seasons.c.name, seasons.c.sort_order).order_by(desc(seasons.c.sort_order))
        )
    )


def get_all_tags(conn):
    return tuple(
        {'name': row.name, 'is_category': row.is_category}
        for row in conn.execute(
            select(tags.c.name, tags.c.is_category).order_by(asc(tags.c.id))
        )
    )


def get_all_trends(conn):
    return tuple(
        {'name': row.name}
        for row in conn.execute(
            select(trends.c.name).order_by(asc(trends.c.id))
        )
    )


def get_read_later_ids(request):
    return {
        int(id)
        for id in request.cookies.get('read_later_ids', '').split(',') if id.isdigit()
    }


def get_usage_ranking(conn, rule):
    return tuple(
        {'name': row.name}
        for row in conn.execute(
            select(pokemons.c.name, func.count(pokemons.c.name).label('count'))
            .join(article_pokemons, pokemons.c.id == article_pokemons.c.pokemon_id)
            .join(articles, articles.c.id == article_pokemons.c.article_id)
            .where(articles.c.rule == rule)
            .group_by(pokemons.c.name, pokemons.c.id)
            .order_by(desc('count'), asc(pokemons.c.id))
            .limit(6)
        )
    )


def kata_to_hira(text):
    return text.translate({i: i - 0x60 for i in range(0x30A1, 0x30F6 + 1)})


def static_file(filename, **values):
    path = os.path.join(current_app.root_path, 'static', filename)
    values['v'] = int(os.stat(path).st_mtime)

    return url_for('static', filename=filename, **values)
