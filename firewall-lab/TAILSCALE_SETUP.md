# iPhone Safari → RDC内のJupyterLab：Tailscale Serve手順

## 対象と前提（2026-11-11時点）

現在のRDC接続先はAlpine Linux 3.24コンテナで、Tailscale未導入・\`/dev/net/tun\`なし・\`apk search -x tailscale\` は \`tailscale-1.98.10-r1\` を返しました。JupyterLabはコンテナ内の \`127.0.0.1:8888\` で起動し、HTTP 302応答を確認しています。

WindowsホストそのものにTailscaleを導入せず、**RDCコンテナに限定**してTailscaleを入れる方針です。Tailscaleの **userspace networking** を使えば、TUNデバイスやNET_ADMINを追加せずにServeでローカルHTTPをHTTPS公開できます。

> これは導入前の手順書です。まだTailscaleのインストール・起動・ログイン・iPhone実測は行っていません。

## Step 1：コンテナでTailscaleパッケージを導入

RDCのAlpine Linuxコンテナで実行（現在root）：

\`\`\`sh
apk add --no-cache tailscale
tailscale version
\`\`\`

同じコンテナでJupyterLabが \`127.0.0.1:8888\` で起動していることを確認：

\`\`\`sh
curl -I http://127.0.0.1:8888/
\`\`\`

JupyterLabがまだ起動していなければ：

\`\`\`sh
cd /workspace/azure-firewall-notebook
./start-notebook.sh
\`\`\`

## Step 2：userspaceモードでdaemonを起動

TUNと特権NET_ADMINを使わない構成です。

\`\`\`sh
mkdir -p /root/.tailscale
chmod 700 /root/.tailscale

tailscaled \
  --tun=userspace-networking \
  --state=/root/.tailscale/tailscaled.state \
  --socket=/tmp/tailscaled.sock \
  > /root/.tailscale/tailscaled.log 2>&1 &
\`\`\`

このコマンドを実行しても、**まだTailscale認証は完了していません**。

## Step 3：tailnetにログイン

\`\`\`sh
tailscale --socket=/tmp/tailscaled.sock up --hostname=azure-firewall-lab
\`\`\`

表示される \`https://login.tailscale.com/a/...\` にiPhone Safariからアクセスして認証します。

\`\`\`sh
tailscale --socket=/tmp/tailscaled.sock status
\`\`\`

## Step 4：Serveを設定（Funnelは禁止）

Tailscale管理画面のDNSでMagicDNSとHTTPS証明書の有効化を求められた場合は、その画面で操作します。

\`\`\`sh
tailscale --socket=/tmp/tailscaled.sock serve --bg http://127.0.0.1:8888
tailscale --socket=/tmp/tailscaled.sock serve status
\`\`\`

表示される \`https://azure-firewall-lab.<your-tailnet>.ts.net/\` のようなURLは**同一tailnet内の端末に限定**されます。

\`tailscale funnel\` はパブリックインターネットへ公開する機能です。**今回は使用しません。**

## Step 5：iPhone側

1. App StoreからTailscaleのiOSアプリをインストール
2. RDCコンテナを参加させたのと同じtailnetにログイン
3. iOSのVPN接続ダイアログで承認
4. SafariからStep 4に表示されたHTTPS URLを開く
5. JupyterLabのトークン認証を行い、\`firewall_hands_on.ipynb\` を開く
6. 最初は**無料の読み取りセル**だけをタップして操作性を確認する

JupyterLabのログイントークンは機密情報です。GitHubやスクリーンショットに公開しないでください。

## 終了と注意点

\`\`\`sh
tailscale --socket=/tmp/tailscaled.sock serve reset
tailscale --socket=/tmp/tailscaled.sock down
\`\`\`

Tailscaleを入れる場所がコンテナ内であるため、WindowsホストのVPN/TUNデバイスやインターネット公開ポートを必要としません。ただしコンテナにWindowsのファイル、Dockerソケット、Azure CLI認証キャッシュがマウントされている場合、コンテナが侵害されるとそれらも危険です。

- Tailscale ServeはtailnetのACLとノード承認を適用
- Jupyterのログイントークンも必ず維持する
- 不要なDocker権限、ホストのボリュームマウントを減らす
- Tailscale状態ファイルをGitHubにコミットしない
- ブラウザからNotebookを実行できる利用者は**Azure操作権限**を持つことに注意

参考：
- https://tailscale.com/docs/concepts/userspace-networking
- https://tailscale.com/docs/features/tailscale-serve
- https://tailscale.com/docs/reference/tailscale-cli/serve
- https://tailscale.com/docs/how-to/set-up-https-certificates