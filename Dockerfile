FROM python:3.9

# コンテナ軽量化のため、Python が .pyc ファイルを生成しないように設定
ENV PYTHONDONTWRITEBYTECODE 1
# ログリアルタイム表示のため、Python の標準出力をバッファリングしないように設定
ENV PYTHONUNBUFFERED 1

# docker内の作業ディレクトリを設定
WORKDIR /app

# ホストのrequirements.txtをコンテナにコピー
COPY requirements.txt .

# docker内にrequirements.txtをインストール
RUN pip install -r requirements.txt

# 新しいユーザーを作成し、必要な権限を付与
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# ローカルディレクトリをdocker内にコピー
# COPY . /app/