## 初回起動
```
docker compose build
docker compose run back django-admin startproject config ./src
```
※2回目以降は、`docker compose up -d` でOK。


`django-admin startproject`
Djangoプロジェクト全体の基本構造を作成するコマンド


back: docker-compose.ymlファイルで定義されているbackサービスを指定しています。
config: 作成するプロジェクトの名前
./src : カレントディレクトリ/srcにプロジェクトを作成することを指定("."のみの場合は、直下にconfigというフォルダが作成され、そこで管理)

```bash
python manage.py startapp base
```
Djangoプロジェクト内の固有のアプリを作成するコマンド
