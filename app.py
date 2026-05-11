from flask import abort, Flask, jsonify, make_response, render_template, request
from database.connection import engine
from utils.consts import ALL_SORTS, ALL_RULES, SECRET_TOKEN
from utils.forms import SearchForm
from utils.helpers import get_all_seasons, get_all_trends, get_read_later_ids, get_usage_ranking, static_file
from utils.page.search import get_all_regulations, get_all_tags, search_articles


app = Flask(__name__)
app.jinja_env.globals.update(static_file=static_file)


@app.route('/')
def index():
    with engine.connect() as conn:
        return render_template(
            'page/index.jinja',
            title='トップ',
            all_rules=ALL_RULES,
            latest_season=get_all_seasons(conn)[0],
            all_trends=get_all_trends(conn),
            usage_ranking={rule: get_usage_ranking(conn, rule) for rule in ALL_RULES}
        )


@app.route('/search')
def search():
    params = request.args.to_dict()
    params['read_later_ids'] = get_read_later_ids(request)
    params.setdefault('pokemon_slots', 1)
    params.setdefault('page', 1)

    with engine.connect() as conn:
        start_item, end_item, total_count, paginations, total_pages, results = search_articles(conn, params)

        return render_template(
            'page/search.jinja',
            title='検索',
            form=SearchForm(params),
            params=params,
            all_tags=get_all_tags(conn),
            all_rules=ALL_RULES,
            all_sorts=ALL_SORTS,
            all_seasons=get_all_seasons(conn),
            all_regulations=get_all_regulations(conn),
            start_item=start_item,
            end_item=end_item,
            total_count=total_count,
            paginations=paginations,
            total_pages=total_pages,
            results=results,
        )


@app.route('/tools')
def tools():
    return render_template('page/tools.jinja', title='ツールなど')


@app.route('/terms')
def terms():
    return render_template('page/terms.jinja', title='利用規約')


@app.route('/policy')
def policy():
    return render_template('page/policy.jinja', title='ポリシー')


@app.route('/inquiry')
def inquiry():
    return render_template('page/inquiry.jinja', title='お問い合わせ')


@app.route('/toggle-read-later', methods=['POST'])
def toggle_read_later():
    article_id = int(request.form.get('article_id'))
    read_later_ids = get_set_from_cookie(request, 'read_later_ids')
    is_added = False

    if article_id in read_later_ids:
        read_later_ids.remove(article_id)
    else:
        if len(read_later_ids) >= 500:
            return jsonify({'message': '保存できるのは500件までです！'}), 400

        read_later_ids.add(article_id)
        is_added = True

    new_cookie_str = ','.join(map(str, read_later_ids))
    response = make_response(jsonify({'is_added': is_added, 'message': '「後で読む」に保存しました！' if is_added else '「後で読む」から削除しました！'}))
    response.set_cookie('read_later_ids', new_cookie_str, max_age=31536000, path='/')

    return response


@app.route('/insert', methods=['GET', 'POST'])
def insert():    
    if request.args.get('token') != SECRET_TOKEN:
        abort(404)

    params = request.args.to_dict()
    if request.method == 'POST':
        form = request.form
        form_tags = form.getlist('tags')

        with engine.begin() as conn:
            tag_name_id_dict = get_name_id_dict(conn, tags)
            pokemon_name_id_dict = get_name_id_dict(conn, pokemons)
            item_name_id_dict = get_name_id_dict(conn, items)
            type_name_id_dict = get_name_id_dict(conn, types)
            ability_name_id_dict = get_name_id_dict(conn, abilities)
            nature_name_id_dict = get_name_id_dict(conn, natures)
            move_name_id_dict = get_name_id_dict(conn, moves)
            article_id = conn.execute(
                insert(articles).values(
                    url=form.get('url'),
                    title=form.get('title'),
                    text=form.get('text') or None,
                    trainer_name=form.get('trainer-name'),
                    rule=form.get('rule') or None,
                    season=form.get('season') or None,
                    regulation=form.get('regulation') or None,
                    rank=form.get('rank') or None,
                    rate=form.get('rate') or None
                ).returning(articles.c.id)).scalar()

            if form_tags:
                conn.execute(insert(article_tags), [{'article_id': article_id, 'tag_id': tag_name_id_dict[tag]} for tag in form_tags])

            article_pokemon_ids = conn.execute(insert(article_pokemons).returning(article_pokemons.c.id), [{
                'article_id': article_id,
                'pokemon_id': pokemon_name_id_dict.get(form.get(f'pokemon{i}')),
                'item_id': item_name_id_dict.get(form.get(f'item{i}')),
                'tera_type_id': type_name_id_dict.get(form.get(f'tera-type{i}')),
                'ability_id': ability_name_id_dict.get(form.get(f'ability{i}')),
                'nature_id': nature_name_id_dict.get(form.get(f'nature{i}')),
                **{f'ev_{s}': int(form.get(f'ev-{s}{i}') or 0) for s in 'habcds'},
                **{f'st_{s}': int(form.get(f'st-{s}{i}') or 0) for s in 'habcds'}
            } for i in range(1, 7)]).scalars().all()
            conn.execute(insert(article_pokemon_moves), [{
                'article_pokemon_id': article_pokemon_id,
                'move_id': move_name_id_dict.get(form.get(f'move{i}{j}'))
            } for i, article_pokemon_id in enumerate(article_pokemon_ids, 1)for j in range(1, 5)])

        flash('追加しました。', 'success')

        return redirect(url_for('articles_insert'))

    with engine.connect() as conn:
        return render_template(
            'page/insert.jinja',
            title='記事追加',
            all_rules=('シングル', 'ダブル'),
            all_seasons=get_all_seasons(conn),
            all_regulations=get_all_regulations(conn),
            all_tags=get_all_tags(conn),
            form=SearchForm(params)
        )
