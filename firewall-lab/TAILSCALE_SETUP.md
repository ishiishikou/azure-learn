# RDCコンテナ内Tailscale Serve — iPhone Safari用

## 現在の実測（2026-11-11）

- RDC接続先：Alpine Linux 3.24コンテナ
- `tailscale`：**1.98.10をインストール済み**
- `tailscaled`：**userspace-networkingモードで起動済み**
- TUNデバイスなし。WindowsホストのVPNや公開ポートは変更していない
- Tailscaleサインイン：**利用者のブラウザ認証待ち**（CLIで都度URLを表示する。ワンタイムURLはGitHubに記録しない）
- JupyterLab：RDC内の `127.0.0.1:8888` でHTTP応答を確認
- ServeおよびiPhone Safariの実機確認：**認証後に実施**

この文書はリポジトリに保存できる再現手順です。現在のログインコード・認証トークンやTailscale秘密鍵は保存しません。

## 1. Tailscaleインストール（実施済み）

```sh
apk add tailscale
tailscale version
```

Alpineのパッケージを使用。Linuxコンテナ内にVPN用TUNがないため、Tailscaleのuserspaceモードを利用しています。

## 2. tailscaledの起動（実施済み）

コンテナの再起動時に起動していなければ、以下で復旧します。

```sh
cd /workspace/azure-firewall-notebook
mkdir -p .state/tailscale
chmod 700 .state .state/tailscale

tailscaled \
  --tun=userspace-networking \
  --state=/workspace/azure-firewall-notebook/.state/tailscale/tailscaled.state \
  --socket=/tmp/tailscale-lab.sock
```

このコマンドは常駐します。別ターミナルから状態を確認してください。コンテナが再作成されても `.state` の保存が維持されるかはRDCのボリューム構成に依存します。

**重要：** `.state/` は `.gitignore` に含めています。Node認証情報をコミットしないでください。

## 3. tailnet認証（ユーザー操作が必要）

```sh
tailscale --socket=/tmp/tailscale-lab.sock up \
  --hostname=azure-firewall-lab \
  --accept-dns=false
```

表示される `https://login.tailscale.com/a/...` をiPhoneのSafariから開き、Tailscaleへのログインを承認してください。承認後：

```sh
tailscale --socket=/tmp/tailscale-lab.sock status
```

## 4. JupyterLabへのHTTPS接続（認証後に実施）

```sh
curl -I http://127.0.0.1:8888/

tailscale --socket=/tmp/tailscale-lab.sock serve \
  --bg http://127.0.0.1:8888

tailscale --socket=/tmp/tailscale-lab.sock serve status
```

表示された **HTTPS URL** のみをiPhone Safariで使用します。Tailscale管理画面でHTTPS/MagicDNSのセットアップを求められる場合があります。

- **Serve**：認証されたtailnet端末にだけ公開（使用する）
- **Funnel**：インターネット上の誰でもアクセス可能になる機能（**使用禁止**）

JupyterLabのトークン認証も有効のまま使用します。トークンは秘密情報なのでGitHubやチャットに不用意に貼りません。

## 5. iPhone側の操作

1. iPhoneにTailscaleアプリをApp Storeからインストール
2. RDCコンテナのログインに使用したのと同じtailnetへサインイン
3. iOSのVPN構成を許可し、Tailscaleを接続状態にする
4. SafariからServeのHTTPS URLを開く
5. JupyterLabで `firewall_hands_on.ipynb` を開く
6. まず **Azureへの読み取り専用セル** で画面操作・出力確認をテストする

## セキュリティと終了

```sh
tailscale --socket=/tmp/tailscale-lab.sock serve status

# 公開を停止するとき
tailscale --socket=/tmp/tailscale-lab.sock serve reset
tailscale --socket=/tmp/tailscale-lab.sock down
```

Tailscaleはアクセス元を限定する機構であり、**コンテナの侵害時のアクセス権限を無害化しません**。RDCコンテナにWindowsファイル、Dockerソケット、Azure認証キャッシュを共有している場合はそれらが危険になり得ます。tailnetポリシーを最小権限にし、Jupyterトークン認証を維持してください。

公式：
- https://tailscale.com/docs/concepts/userspace-networking
- https://tailscale.com/docs/features/tailscale-serve
- https://tailscale.com/docs/reference/tailscale-cli/serve