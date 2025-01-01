# プロダクトのバックエンド
## セットアップ
### 依存ライブラリインストール
```
# 仮想環境の作成とactivate
poetry shell
# 依存ライブラリのインストール
poetry install
```

### DBのセットアップ
```
# マイグレーションファイルの作成
python manage.py makemigrations
# DBの作成
python manage.py migrate
```

### 管理ユーザーの作成
```
python manage.py createsuperuser
```

### ローカルサーバーの起動
```
# debug用の証明書の発行
cd プロジェクトのディレクトリ
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes
# ローカルサーバーの起動
python manage.py runsslserver --certificate cert.pem --key key.pem
```




