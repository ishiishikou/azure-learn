# Entra External ID PoC — 認証ファースト構成（Static Web Apps Free）

## 検証目的

ユーザーがアプリを開くとMicrosoft Entra External IDのサインインへ自動遷移し、SPAが取得した **API用アクセストークン** をAzure Functionsでサーバー側検証する。
**成功（HTTP 200）を確認してからのみアプリ画面を表示する。**
独自のログインフォームは作らない。

## 処理の流れ

1. `/` または `/dashboard.html` に未認証でアクセスする。
2. MSAL Browser v5がEntra External IDのログイン画面にリダイレクトする。
3. Microsoftでサインインし、`api://def986c6-008f-426e-9ec9-21074cbdaf62/api.read` スコープを取得する。
4. SPAは `GET /api/protected` の `X-Authorization: Bearer <access_token>` でアクセストークンを送信する。
5. APIはMicrosoftのJWKSによる署名、issuer、audience、tenant、期限、`api.read` を検証する。
6. APIが200なら `/dashboard.html` でアプリを表示する。401/403・通信エラーならアプリを表示せずエラーメッセージを表示する。
7. SSO検証モードではログアウト後にMicrosoftのログイン要求を再開する。`prompt=login` は付けず、認証画面が再表示されるかSSOで自動復帰するかを観察する。

MSAL Browser v5のリダイレクトブリッジは `/redirect.html` を使用する。
Entra管理センターのSPAリダイレクトURIも公開サイトの
`https://kind-mushroom-09e25b600.1.azurestaticapps.net/redirect.html` に一致させる。

> Microsoftで既にサインイン済みならSSOでログイン入力を省略することがある。ログイン画面を検証する際はプライベートウィンドウを利用する。

## Static Web Appsのヘッダー注意事項

Managed Functionsの `Authorization` ヘッダーはStatic Web Appsの内部処理により置き換えられることがある。PoCではSPAからAPI用アクセストークンを `X-Authorization` で渡し、APIはこのヘッダーを読む。これは認証の省略ではない。必ずJWKS署名とissuer・audience・tenant・期限・scopeを検証する。APIの内部ヘッダーをログや画面に出さない。

## 構成

- Azure Static Web Apps: Free（静的ファイルは公開ホスティング）
- SPA: Vite + MSAL Browser v5
- 認証: Entra External ID（専用テナント）
- Web API: Static Web Appsに統合したAzure Functions（Node.js 22）
- APIの保護: JWT検証 (`jose`) + `api.read` スコープの承認
- CI/CD: GitHub Actions。信頼できるfeatureブランチへのpushでのみデプロイ。

**セキュリティ境界はAPIです。** `dashboard.html` やJavaScriptは未認証でもダウンロードできる。
画面表示の制御はユーザー体験用であり、機密データを保護できるのはサーバー側の認可だけ。
トークン、パスワード、クライアントシークレットを画面やGitHubに記録しない。

## 動作確認

1. シークレットウィンドウで `https://kind-mushroom-09e25b600.1.azurestaticapps.net/` を開く。
2. アプリ画面が表示されず、Microsoft Entra External IDのログインへリダイレクトされること。
3. 正しいユーザーでログイン後、APIからHTTP 200を受け取りアプリ画面が表示されること。
4. ログアウト後にMicrosoftへ再ログイン要求が送られ、パスワード入力が必要かSSOで自動復帰するかを確認すること。
5. `GET /api/protected` を `X-Authorization` なしで呼んで401、不正トークンを `X-Authorization` に入れて401になること。
6. 期限切れ・別API向け・scope不足はAPIの自動テストで確認する。

## ローカルテスト

```bash
cd external-id-poc
npm ci
npm run build
cd api
npm ci
npm test
```

ローカルのブラウザログインを検証するには、`http://127.0.0.1:5173/redirect.html` をEntraアプリのSPAリダイレクトURIに追加する必要がある。

公式資料: https://learn.microsoft.com/en-us/entra/msal/javascript/browser/redirect-bridge
