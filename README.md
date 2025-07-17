### Devin

- [Devin's Machine](https://app.devin.ai/workspace) でリポジトリ追加

#### 1.Git Pull
- そのまま

#### 2.Configure Secrets
```sh
# 環境変数用のファイル作成
$ touch .envrc

# .envrc に下記を入力. xxx は適宜更新

export DJANGO_SUPERUSER_USERNAME=xxx
export DJANGO_SUPERUSER_EMAIL=xxx@xxx.com
export DJANGO_SUPERUSER_PASSWORD=xxx
export DJANGO_SECRET_KEY=hogehoge
export POSTGRES_DB=hogehoge
export POSTGRES_USER=hogehoge
export POSTGRES_PASSWORD=hogehoge

# SMS送信・音声通話機能用の環境変数
export TWILIO_ACCOUNT_SID=your_twilio_account_sid
export TWILIO_AUTH_TOKEN=your_twilio_auth_token
export TWILIO_FROM_NUMBER=your_twilio_phone_number

# 環境変数を読み込む
$ direnv allow
```

- ローカル用
```sh
$ brew install direnv
```
#### 4.Maintain Dependencies
```sh
$ docker compose up -d

# コンテナ作り直し
$ ./remake-container.sh
```

#### 5.SetUp Lint
```sh
$ docker compose run --rm backend uv run ruff check .
```

#### 6.SetUp Tests
- no tests ran in 0.00s だと Devin の Verify が通らないっぽい
```sh
$ docker compose run --rm backend uv run pytest
```

### 7.Setup Local App

```sh
$ http://localhost:8000/ がアプリケーションのURL
```

#### SMS送信・音声通話機能の利用

SMS送信機能と音声通話機能を利用するには、以下のURLにアクセスしてください：

- SMS送信フォーム: http://localhost:8000/communication/sms/
- 音声通話フォーム: http://localhost:8000/communication/voice/

**注意**: 実際にSMSや音声通話を行うには、上記の環境変数にTwilio認証情報を設定する必要があります。

#### 8.Additional Notes
- 必ず日本語で回答してください
- Python, Django を利用する
- データベースは Postgres
- テストは pytest を利用する
を入力

### OPENAI-API で PR-Review
- [Qodo Merge](https://qodo-merge-docs.qodo.ai/installation/github/)
  - GPT-4.1利用
  - 日本語の回答をするようプロンプト設定
- GitHub の Repository >> Settings >> Secretes and variables >> Actions の Repository secrets の New repository secret を登録
  - OPENAI_KEY という名称で OPENAI API keys の SECRET KEY を登録
    - [OPENAI API keys](https://platform.openai.com/settings/organization/api-keys) 
```sh
--- .github/
           |- workflows/
                        |-- pr_agent.yml
```
