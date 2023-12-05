# ベースイメージの指定
FROM python:3.9

# 作業ディレクトリの設定
WORKDIR /app

# 依存関係ファイルをコピーし、依存関係をインストール
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースコードをコピー
COPY . .

# アプリケーションがリッスンするポートを指定
EXPOSE 8501

# アプリケーションの実行コマンド
CMD ["streamlit", "run", "app.py"]
