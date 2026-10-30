# Entra External ID PoC (Azure Static Web Apps Free)

Entra External ID のユーザー認証後に `/dashboard.html` を表示する、学習用 JavaScript SPA です。アップロードされたMicrosoftのサンプルを元に作成。

## 構成

- Entra External ID: `externalidpoc2026test.ciamlogin.com`
- SPA client ID: `8fc65eb9-6112-4c8b-acd3-c6a348c36e19`
- MSAL Browser v5 + redirect bridge (Vite)
- 秘密情報は不要。クライアントIDは公開識別子です。

## Static Web Apps Free への配置

1. Azure Portalで **Static Web Apps** → **作成**、既存RG `rg-externalid-poc` / プラン **Free**。
2. ソース **GitHub**、リポジトリ `ishiishikou/azure-learn`、ブランチはデプロイしたいブランチを選択。
3. ビルドプリセット **Custom**、App location `/external-id-poc`、API location 空、Output location `dist`。
4. GitHub Actionsが成功したらAzure Static Web Appsの公開URLを確認。
5. Entra管理センターの **External ID PoC** テナント → **アプリの登録** → 対象SPA → **認証** で、SPAリダイレクトURIとして `https://<YOUR-SITE>.azurestaticapps.net/redirect.html` を追加。**完全一致**が必要です。
6. ブラウザで公開URLへアクセスし「サインイン」を押す。認証後 `/dashboard.html` に遷移すれば成功。

## ローカルビルド

```bash
npm install
npm run build
```

ローカルで認証する場合は `http://127.0.0.1:5173/redirect.html` をSPAリダイレクトURIに追加する必要があります。

## 注意事項

- `dashboard.html` 自体は公開静的ファイルです。**認可されたAPIへのアクセス制御ではありません**。機密情報は配置しないでください。
- 実運用ではAPI側のアクセストークン検証と認可が必要です。
- Static Web Appsの組み込みカスタム認証はStandard向けです。本PoCはFreeの静的ホスティングとMSAL.jsを使います。
- ブラウザにJWT、クライアントシークレット、パスワードを共有しないでください。

公式ドキュメント: https://learn.microsoft.com/en-us/entra/msal/javascript/browser/redirect-bridge

## 保護されたAPIの検証（2026年10月）

- マネージドAzure Functions V4（Node.js 22）: \`external-id-poc/api\`
- APIアプリ（client ID）: \`def986c6-008f-426e-9ec9-21074cbdaf62\`
- Delegated scope: \`api://def986c6-008f-426e-9ec9-21074cbdaf62/api.read\`
- API: \`GET /api/protected\`。Authorization: Bearer <access_token> を要求。
- アクセストークンの署名をテナントのJWKSで検証し、issuer、audience、tenant ID、version、時刻、および \`scp\` を検証する。Microsoft Graphへのリクエスト単位の問い合わせは不要。
- 公開ページ上の3ボタンで、トークンなし→401、正常→200、改ざん→401を比較する。ブラウザでログイン後に正常ボタンを押すと、必要に応じてMSALが追加のトークン取得フローを開始する。
- 権限不足→403、期限切れ→401、他のaudience→401、issuer不一致→401は、署名付きのローカルテスト用JWTで検証する（本物のユーザー用トークンや秘密鍵は保存しない）。
- APIローカルテスト: \`cd external-id-poc/api && npm ci && npm test\`。
- GitHub Actionsの \`api_location\` は \`/external-id-poc/api\` を指定する。Static Web Apps FreeのマネージドAPIを使用する。
- データは認証後にAPIから返し、公開HTML内に秘密情報を配置しない。トークンはAPIで永続保存しない。
