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
