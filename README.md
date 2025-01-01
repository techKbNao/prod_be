# プロダクトのバックエンド
## セットアップ
### Pythonのバージョンが合わない人向け
```
pyenv install 3.12.5
pyenv local 3.12.5
poetry env use 3.12.5
```
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
# ローカルサーバーの起動
python manage.py runserver_plus --cert-file server.crt --key-file server.key
```


## 接続DBについて
- 本番はRDSを使用したいと考えている
- ローカルではSQLiteを使用している