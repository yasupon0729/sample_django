## 初回起動
```
docker compose build
docker compose run back django-admin startproject vegeket ./src
```
※2回目以降は、`docker compose up -d` でOK。

back: docker-compose.ymlファイルで定義されているbackサービスを指定しています。
vegeket: 作成するプロジェクトの名前
./src : カレントディレクトリ/srcにプロジェクトを作成することを指定
