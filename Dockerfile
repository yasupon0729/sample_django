FROM python:3.9

# コンテナ軽量化のため、Python が .pyc ファイルを生成しないように設定
ENV PYTHONDONTWRITEBYTECODE 1
# ログリアルタイム表示のため、Python の標準出力をバッファリングしないように設定
ENV PYTHONUNBUFFERED 1

ENV DOCKER_UID=${DOCKER_UID}
ENV DOCKER_GID=${DOCKER_GID}


# docker内の作業ディレクトリを設定
WORKDIR /app

# ホストのrequirements.txtをコンテナにコピー
COPY requirements.txt .

# docker内にrequirements.txtをインストール
RUN pip install -r requirements.txt

# 新しいユーザーを作成する。
RUN useradd -m appuser 
# 所有者を変更する。 /app以下をappuserに変更する 
RUN chown -R appuser:appuser /app 
# appuser:appuser は「ユーザー名:グループ名」の形式で、ファイルやディレクトリの所有者とグループ所有者の両方を指定しています。
# 補足説明
# Linuxシステムでは、通常、ユーザーを作成すると同じ名前のグループも自動的に作成されます。

#ディレクトリ作成
RUN mkdir -p /home/appuser/.ssh 
# 所有者を変更する。 /home/appuser/.ssh以下をappuserに変更する 
RUN chown -R appuser:appuser /home/appuser/.ssh 
# ディレクトリのパーミッションを設定する。 
# 700は、ディレクトリのパーミッションを700に設定する。
RUN chmod 700 /home/appuser/.ssh

# GitHubのホストキーをコンテナ内に追加
RUN ssh-keyscan github.com >> /home/appuser/.ssh/known_hosts
# ユーザーを変更する。 appuserに変更する
USER appuser

