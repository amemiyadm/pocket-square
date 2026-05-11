# pocket-square

## 環境構築

 `.env` を作成。
```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```
仮想環境を作成。
```bash
python -m venv .venv
```
必要なライブラリをインストール。
```bash
pip install -r requirements.txt
```
`run.bat`ファイルを作成。
```bat
call .venv\Scripts\activate
flask run --debug -p 5000
```

## マイグレーション
データベース定義（`schema.py`）を変更後、Alembicを使用してマイグレーション。

### 1. マイグレーションファイルの生成
```bash
alembic -c database/alembic.ini revision --autogenerate -m '変更内容'
```

### 2. マイグレーションの適用
```bash
alembic -c database/alembic.ini upgrade head
```

## requirements.txt
push前に更新する。
```bash
pip freeze > requirements.txt
```
