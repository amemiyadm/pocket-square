from database.connection import engine
from utils.consts import ALL_RANGES, ALL_RULES, ALL_SORTS, NATURE_TABLE
from utils.helpers import get_all_regulations, get_all_seasons, get_all_tags


class SearchForm:
    def __init__(self, params):
        with engine.connect() as conn:
            modifier_options = [''] + list(NATURE_TABLE['increased'].keys())
            rule_options = [''] + list(ALL_RULES)
            sort_options = [''] + list(ALL_SORTS)
            tag_options = [''] + [tag['name'] for tag in get_all_tags(conn)]
            season_options = [''] + [season['name'] for season in get_all_seasons(conn)]
            regulation_options = [''] + [regulation['name'] for regulation in get_all_regulations(conn)]

        for i in range(1, 13):
            setattr(self, f'not{i}', CheckboxField(f'not{i}', 'NOT', params))
            setattr(self, f'pokemon{i}', SearchField(f'pokemon{i}', 'ポケモン', params, {'class': 'abyss', 'data-abyss-type': 'pokemon'}))
            setattr(self, f'item{i}', SearchField(f'item{i}', '持ち物', params, {'class': 'abyss', 'data-abyss-type': 'item'}))
            setattr(self, f'tera_type{i}', SearchField(f'tera_type{i}', 'テラスタイプ', params, {'class': 'abyss', 'data-abyss-type': 'tera-type'}))
            setattr(self, f'ability{i}', SearchField(f'ability{i}', '特性', params, {'class': 'abyss', 'data-abyss-type': 'ability'}))
            setattr(self, f'increased_st{i}', SelectField(f'increased_st{i}', '上昇補正', params, modifier_options))
            setattr(self, f'decreased_st{i}', SelectField(f'decreased_st{i}', '下降補正', params, modifier_options))
            setattr(self, f'ev_h{i}', NumberField(f'ev_h{i}', 'HP努力値', params))
            setattr(self, f'ev_h_range{i}', SelectField(f'ev_h_range{i}', 'HP範囲', params, ALL_RANGES))
            setattr(self, f'ev_a{i}', NumberField(f'ev_a{i}', 'こうげき努力値', params))
            setattr(self, f'ev_a_range{i}', SelectField(f'ev_a_range{i}', 'こうげき範囲', params, ALL_RANGES))
            setattr(self, f'ev_b{i}', NumberField(f'ev_b{i}', 'ぼうぎょ努力値', params))
            setattr(self, f'ev_b_range{i}', SelectField(f'ev_b_range{i}', 'ぼうぎょ範囲', params, ALL_RANGES))
            setattr(self, f'ev_c{i}', NumberField(f'ev_c{i}', 'とくこう努力値', params))
            setattr(self, f'ev_c_range{i}', SelectField(f'ev_c_range{i}', 'とくこう範囲', params, ALL_RANGES))
            setattr(self, f'ev_d{i}', NumberField(f'ev_d{i}', 'とくぼう努力値', params))
            setattr(self, f'ev_d_range{i}', SelectField(f'ev_d_range{i}', 'とくぼう範囲', params, ALL_RANGES))
            setattr(self, f'ev_s{i}', NumberField(f'ev_s{i}', 'すばやさ努力値', params))
            setattr(self, f'ev_s_range{i}', SelectField(f'ev_s_range{i}', 'すばやさ範囲', params, ALL_RANGES))

            for j in range(1, 5):
                setattr(self, f'move{j}_{i}', SearchField(f'move{j}_{i}', f'技{j}', params, {'class': 'abyss', 'data-abyss-type': 'move'}))

        for i in range(1, 7):
            setattr(self, f'or{i}', CheckboxField(f'or{i}', 'OR', params, {'class': 'iroha-trigger', 'data-iroha-target': f'pokemon-status{i + 6}'}))
            setattr(self, f'nature{i}', SearchField(f'nature{i}', '性格', params, {'class': 'abyss', 'data-abyss-type': 'nature'}))

        self.read_later = CheckboxField('read_later', '"後で読む"のみを表示', params)
        self.keyword = SearchField('keyword', 'フリーワード検索', params)
        self.tag = SelectField('tag', 'タグ', params, tag_options)
        self.rule = SelectField('rule', 'ルール', params, rule_options)
        self.sort = SelectField('sort', '並び順', params, sort_options)
        self.season_start = SelectField('season_start', 'シーズン開始', params, season_options, {'id': 'season-start', 'data-pair': 'season-end'})
        self.season_end = SelectField('season_end', 'シーズン終了', params, season_options, {'id': 'season-end', 'data-pair': 'season-start'})
        self.regulation_start = SelectField('regulation_start', 'レギュ開始', params, regulation_options)
        self.regulation_end = SelectField('regulation_end', 'レギュ終了', params, regulation_options)
        self.pokemon_slots = HiddenField('pokemon_slots', '', params, {'id': 'pokemon-slots'})
        self.url = UrlField('url', 'URL', params)
        self.title = TextareaField('title', 'タイトル', params)
        self.text = TextareaField('text', 'テキスト', params)
        self.trainer_name = SearchField('trainer_name', 'トレーナー名', params)
        self.season = SelectField('season', 'シーズン', params, season_options)
        self.regulation = SelectField('regulation', 'レギュレーション', params, regulation_options)
        self.rank = NumberField('rank', '順位', params)
        self.rate = NumberField('rate', 'レート', params, {'step': '0.001'})

    def admin_fields1(self):
        return (
            self.url,
            self.trainer_name,
            self.title,
            self.text,
            self.rule,
            self.season,
            self.regulation,
            self.rank,
            self.rate
        )

    def admin_fields2(self, i):
        return (
            getattr(self, f'pokemon{i}'),
            getattr(self, f'item{i}'),
            getattr(self, f'tera_type{i}'),
            getattr(self, f'move1_{i}'),
            getattr(self, f'move2_{i}'),
            getattr(self, f'move3_{i}'),
            getattr(self, f'move4_{i}'),
            getattr(self, f'ability{i}'),
            getattr(self, f'ev_h{i}'),
            getattr(self, f'ev_a{i}'),
            getattr(self, f'ev_b{i}'),
            getattr(self, f'ev_c{i}'),
            getattr(self, f'ev_d{i}'),
            getattr(self, f'ev_s{i}'),
            getattr(self, f'nature{i}')
        )

    def default_fields(self, i):
        return (
            getattr(self, f'pokemon{i}'),
            getattr(self, f'item{i}'),
            getattr(self, f'tera_type{i}'),
            getattr(self, f'move1_{i}')
        )

    def detail_fields(self):
        return (
            self.read_later,
            self.keyword,
            self.tag,
            self.rule,
            self.sort,
            self.season_start,
            self.season_end,
            self.regulation_start,
            self.regulation_end
        )

    def hidden_fields(self):
        return [self.pokemon_slots]

    def is_detail_open(self):
        return any(field.value for field in self.detail_fields())

    def is_pokemon_detail_open(self, i):
        return any(field.value for field in self.pokemon_detail_fields(i))

    def operator_fields(self, i):
        return tuple(getattr(self, f'{f}{i}') for f in (['not', 'or'] if i <= 6 else ['not']))

    def pokemon_detail_fields(self, i):
        return (
            getattr(self, f'move2_{i}'),
            getattr(self, f'move3_{i}'),
            getattr(self, f'move4_{i}'),
            getattr(self, f'ability{i}'),
            getattr(self, f'increased_st{i}'),
            getattr(self, f'decreased_st{i}'),
            getattr(self, f'ev_h{i}'),
            getattr(self, f'ev_h_range{i}'),
            getattr(self, f'ev_a{i}'),
            getattr(self, f'ev_a_range{i}'),
            getattr(self, f'ev_b{i}'),
            getattr(self, f'ev_b_range{i}'),
            getattr(self, f'ev_c{i}'),
            getattr(self, f'ev_c_range{i}'),
            getattr(self, f'ev_d{i}'),
            getattr(self, f'ev_d_range{i}'),
            getattr(self, f'ev_s{i}'),
            getattr(self, f'ev_s_range{i}')
        )


class Field:
    def __init__(self, name, label, params, attrs=None):
        self.name = name
        self.label = label
        self.value = params.get(self.name, '')
        self.attrs = attrs or {}

    def render_attrs(self):
        return ''.join(f' {key}="{value}"' for key, value in self.attrs.items())

    def render(self):
        raise NotImplementedError()


class CheckboxField(Field):
    def render(self):
        checked = ' checked' if self.value else ''
        return f'''
            <label class="col-span-2 gap-2 inline-flex items-center">
                <input name="{self.name}" type="checkbox"{checked}{self.render_attrs()}>
                <span>{self.label}</span>
            </label>
        '''


class NumberField(Field):
    def render(self):
        return f'''
            <fieldset>
                <legend>{self.label}</legend>
                <input name="{self.name}" type="number" value="{self.value}"{self.render_attrs()}>
            </fieldset>
        '''


class SearchField(Field):
    def render(self):
        return f'''
            <fieldset>
                <legend>{self.label}</legend>
                <input name="{self.name}" type="search" value="{self.value}"{self.render_attrs()}>
            </fieldset>
        '''


class SelectField(Field):
    def __init__(self, name, label, params, options, attrs=None):
        super().__init__(name, label, params, attrs)
        self.options = options

    def render(self):
        return f'''
            <fieldset>
                <legend>{self.label}</legend>
                <select name="{self.name}"{self.render_attrs()}>
                    {''.join(f'<option value="{option if option != 'のみ' else ''}"{' selected' if option == self.value else ''}>{option}</option>' for option in self.options)}
                </select>
            </fieldset>
        '''


class TextareaField(Field):
    def render(self):
        return f'''
            <fieldset>
                <legend>{self.label}</legend>
                <textarea name="{self.name}"{self.render_attrs()}>{self.value}</textarea>
            </fieldset>
        '''


class HiddenField(Field):
    def render(self):
        return f'<input name="{self.name}" type="hidden" value="{self.value}"{self.render_attrs()}>'
    

class UrlField(Field):
    def render(self):
        return f'''
            <fieldset>
                <legend>{self.label}</legend>
                <input name="{self.name}" type="url" value="{self.value}"{self.render_attrs()}>
            </fieldset>
        '''
