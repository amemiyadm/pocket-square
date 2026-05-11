from sqlalchemy import asc, desc, func, or_, select
from database.schema import abilities, articles, article_tags, tags, article_pokemons, article_pokemon_moves, moves, pokemons, items, types, seasons, regulations, natures
from utils.consts import NATURE_TABLE


def create_snippet(text, keyword, radius=30):
    ellipsis = '...'
    keyword_start = text.find(keyword)

    if keyword_start == -1:
        return (text[:radius * 2] + ellipsis), ''

    keyword_end = keyword_start + len(keyword)
    snippet_start = max(0, keyword_start - radius)
    snippet_end = min(len(text), keyword_end + radius)
    prefix = text[snippet_start:keyword_start]
    suffix = text[keyword_end:snippet_end]

    if snippet_start > 0:
        prefix = ellipsis + prefix

    if snippet_end < len(text):
        suffix = suffix + ellipsis

    return prefix, suffix


def get_all_regulations(conn):
    return tuple(
        {'name': row.name, 'sort_order': row.sort_order}
        for row in conn.execute(
            select(regulations.c.name, regulations.c.sort_order).order_by(desc(regulations.c.sort_order))
        )
    )


def get_all_tags(conn):
    return tuple(
        {'name': row.name, 'is_category': row.is_category}
        for row in conn.execute(
            select(tags.c.name, tags.c.is_category).order_by(asc(tags.c.id))
        )
    )


def search_articles(conn, params):
    ids_stmt = select(articles.c.id)

    for i in range(1, int(params.get('pokemon_slots')) + 1):
        conditions = []

        for j in (i, i + 6):
            if (j == i + 6) and not params.get(f'or{i}'):
                continue

            filters = (
                (params.get(f'pokemon{j}'), pokemons, (pokemons.c.id == article_pokemons.c.pokemon_id), pokemons.c.name),
                (params.get(f'item{j}'), items, (items.c.id == article_pokemons.c.item_id), items.c.name),
                (params.get(f'tera_type{j}'), types, (types.c.id == article_pokemons.c.tera_type_id), types.c.name),
                (params.get(f'ability{j}'), abilities, (abilities.c.id == article_pokemons.c.ability_id), abilities.c.name),
            )
            move_names = [params.get(f'move{k}_{j}') for k in range(1, 5) if params.get(f'move{k}_{j}')]
            nature = {'increased': params.get(f'increased_st{j}'), 'decreased': params.get(f'decreased_st{j}')}
            evs = {stat: {'value': params.get(f'ev_{stat}{j}'), 'range': params.get(f'ev_{stat}_range{j}')} for stat in 'habcds'}

            if any(value for value, _, _, _ in filters) or move_names or any(nature.values()) or any(ev['value'] for ev in evs.values()):
                subq_from = article_pokemons
                subq = select(1).where(article_pokemons.c.article_id == articles.c.id).correlate(articles)

                for value, table, join_condition, column in filters:
                    if value:
                        subq_from = subq_from.join(table, join_condition)
                        subq = subq.where(column == value)

                for move_name in move_names:
                    subq = subq.where(
                        select(1)
                        .select_from(
                            article_pokemon_moves
                            .join(moves, moves.c.id == article_pokemon_moves.c.move_id)
                        )
                        .where(
                            (article_pokemon_moves.c.article_pokemon_id == article_pokemons.c.id) &
                            (moves.c.name == move_name)
                        )
                        .exists()
                    )

                if any(nature.values()):
                    subq_from = subq_from.join(natures, natures.c.id == article_pokemons.c.nature_id)

                    if nature['increased']:
                        subq = subq.where(natures.c.name.in_(NATURE_TABLE['increased'].get(nature['increased'], [])))
                    if nature['decreased']:
                        subq = subq.where(natures.c.name.in_(NATURE_TABLE['decreased'].get(nature['decreased'], [])))

                for stat, ev_details in evs.items():
                    if ev_details['value']:
                        col = getattr(article_pokemons.c, f'ev_{stat}')

                        if ev_details['range'] == '以上':
                            subq = subq.where(col >= ev_details['value'])
                        elif ev_details['range'] == '以下':
                            subq = subq.where(col <= ev_details['value'])
                        else:
                            subq = subq.where(col == ev_details['value'])

                subq = subq.select_from(subq_from).exists()
                conditions.append(~subq if params.get(f'not{j}') else subq)

        if conditions:
            ids_stmt = ids_stmt.where(conditions[0] if len(conditions) == 1 else or_(*conditions))

    if params.get('read_later'):
        ids_stmt = ids_stmt.where(articles.c.id.in_(params.get('read_later_ids')))

    if params.get('keyword'):
        ids_stmt = ids_stmt.where(articles.c.text.like(f"%{params.get('keyword')}%"))

    if params.get('tag'):
        ids_stmt = ids_stmt.where(
            select(1)
            .select_from(article_tags.join(tags, tags.c.id == article_tags.c.tag_id))
            .where((article_tags.c.article_id == articles.c.id) & (tags.c.name == params.get('tag')))
            .correlate(articles)
            .exists()
        )

    if params.get('rule'):
        ids_stmt = ids_stmt.where(articles.c.rule == params.get('rule'))

    if params.get('season_start') or params.get('season_end'):
        ids_stmt = ids_stmt.join(seasons, seasons.c.name == articles.c.season)

        if params.get('season_start'):
            ids_stmt = ids_stmt.where(seasons.c.sort_order >= params.get('season_start'))

        if params.get('season_end'):
            ids_stmt = ids_stmt.where(seasons.c.sort_order <= params.get('season_end'))

    if params.get('regulation_start') or params.get('regulation_end'):
        ids_stmt = ids_stmt.join(regulations, regulations.c.name == articles.c.regulation)

        if params.get('regulation_start'):
            ids_stmt = ids_stmt.where(regulations.c.sort_order >= params.get('regulation_start'))

        if params.get('regulation_end'):
            ids_stmt = ids_stmt.where(regulations.c.sort_order <= params.get('regulation_end'))

    count_stmt = select(func.count()).select_from(ids_stmt.subquery())
    total_count = conn.execute(count_stmt).scalar()

    if params.get('sort') == '順位順':
        ids_stmt = ids_stmt.order_by(articles.c.rank.asc(), articles.c.id.desc())
    else:
        ids_stmt = ids_stmt.order_by(articles.c.id.desc())

    per_page = 2
    ids_stmt = ids_stmt.limit(per_page).offset((int(params.get('page', 1)) - 1) * per_page)
    article_ids = [row.id for row in conn.execute(ids_stmt)]
    total_pages = (total_count + per_page - 1) // per_page
    start_page = max(1, int(params.get('page', 1)) - 2)
    end_page = min(total_pages, int(params.get('page', 1)) + 2)

    if end_page - start_page < 4:
        if start_page == 1:
            end_page = min(total_pages, start_page + 4)
        elif end_page == total_pages:
            start_page = max(1, end_page - 4)

    paginations = list(range(start_page, end_page + 1))

    if not article_ids:
        return 0, 0, 0, paginations, total_pages, []

    start_item = (int(params.get('page', 1)) - 1) * per_page + 1
    end_item = start_item + len(article_ids) - 1
    detail_stmt = select(
        articles.c.id.label('article_id'),
        articles.c.url,
        articles.c.title,
        articles.c.text,
        articles.c.trainer_name,
        articles.c.rank,
        articles.c.rate,
        article_tags.c.tag_id,
        article_pokemons.c.pokemon_id,
        pokemons.c.name.label('pokemon_name'),
        items.c.name.label('item_name'),
        types.c.name.label('tera_type_name'),
        tags.c.name.label('tag_name')
    ).select_from(
        articles.outerjoin(
            article_tags.join(tags, tags.c.id == article_tags.c.tag_id),
            articles.c.id == article_tags.c.article_id
        )
        .join(article_pokemons, articles.c.id == article_pokemons.c.article_id)
        .outerjoin(pokemons, pokemons.c.id == article_pokemons.c.pokemon_id)
        .outerjoin(items, items.c.id == article_pokemons.c.item_id)
        .outerjoin(types, types.c.id == article_pokemons.c.tera_type_id)
    ).where(articles.c.id.in_(article_ids))

    if params.get('sort') == '順位順':
        detail_stmt = detail_stmt.order_by(articles.c.rank.asc(), articles.c.id.desc(), article_pokemons.c.id.asc())
    else:
        detail_stmt = detail_stmt.order_by(articles.c.id.desc(), article_pokemons.c.id.asc())

    rows = conn.execute(detail_stmt).mappings().all()
    results = {}

    for row in rows:
        article_id = row['article_id']
        if article_id not in results:
            results[article_id] = {
                'article_id': article_id,
                'url': row['url'],
                'title': row['title'],
                'snippet': create_snippet(row['text'], params.get('keyword', '')),
                'trainer_name': row['trainer_name'],
                'rank': row['rank'],
                'rate': row['rate'],
                'tag_names': {},
                'pokemon_names': {},
                'item_names': {},
                'tera_type_names': {},
            }

        result = results[article_id]

        if (row['tag_id'] is not None) and (row['tag_id'] not in result['tag_names']):
            result['tag_names'][row['tag_id']] = row['tag_name']

        if row['pokemon_id'] not in result['pokemon_names']:
            result['pokemon_names'][row['pokemon_id']] = row['pokemon_name']
            result['item_names'][row['pokemon_id']] = row['item_name']
            result['tera_type_names'][row['pokemon_id']] = row['tera_type_name']

    for result in results.values():
        result['tag_names'] = tuple(result['tag_names'].values())
        result['pokemon_names'] = tuple(result['pokemon_names'].values())
        result['item_names'] = tuple(result['item_names'].values())
        result['tera_type_names'] = tuple(result['tera_type_names'].values())

    return start_item, end_item, total_count, paginations, total_pages, results.values()
