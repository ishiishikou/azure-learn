# Azure Firewall Basic — iPhone用ハンズオン

iPhone Safariから **ボタンでAzure CLI操作を実行**し、結果を表示する教材です。Notebook (.ipynb) が正本で、同じ教材を Voilà でスマホ向けWeb画面として使います。コードをターミナルへ貼り付ける必要はありません。

## 学習内容

| フェーズ | 操作 | Azureの課金 |
| --- | --- | --- |
| 0 | 認証、サブスクリプション・リソース確認 | なし |
| 1 | rg-firewall-lab の準備 | なし |
| 2 | VNetと3つのサブネットの作成 | VNet自体の時間課金なし |
| 3 | Azure Firewall Policy Basicの作成 | この構成でPolicy自体は原則追加料金なし |
| 4 | 2つのStandard Public IPとAzure Firewall Basicの作成 | **有料** |
| 5 | Ubuntu 22.04 VM Standard_B1sの作成 | **有料** |
| 6 | UDR: VMサブネットの既定経路をFirewallへ | 通信・Firewall課金が継続 |
| 7 | Google / Microsoftへcurl（拒否状態を確認） | 実行中の課金が継続 |
| 8 | Google HTTPSのみ許可するApplication Rule | 実行中の課金が継続 |
| 9 | curlを再実行し比較 | 実行中の課金が継続 |
| 終了 | 学習用リソースグループを削除 | 削除完了後の対象リソース課金が終了 |

**注意:** コストはリージョン・利用量・サブスクリプション条件によって変わります。無料クレジット/予算アラートはハードキャップではありません。Azure Firewallは停止ではなく**削除**するまで課金が続く想定で運用してください。作成エラー後も部分作成済みのリソースが残る場合があります。

## 想定環境と手順

- Windowsホスト上のWSL2またはRDCに接続されたLinux環境（Python 3.10+、Azure CLI 2.75+）。既存のDockerコンテナでも実行できます。
- 本リポジトリの firewall-lab フォルダで実行してください。

```sh
./start.sh
```

既存のRDC実行環境では Voilà と Azure CLI の動作を確認済みです。スマホからアクセス可能にするには、**認証された安全なHTTPS経路**が別途必要です。

### iPhoneからのアクセス

- **VS Code Remote Tunnelのポート転送:** 8866番ポートを転送し、iPhoneのSafariで認証済みの転送URLを開きます。統合ターミナルへの貼り付けは不要です。
- **Tailscale Serve:** iPhoneとWindows/WSL側を同一tailnetに接続し、Windows側のTailscale Serveでローカル8866をHTTPSプロキシします。**Tailscale Funnelで一般公開しない**でください。

**Docker内にVoilàを起動した場合:** Dockerのポートをホストのループバックに公開するなど、ホストからそのポートに到達できる設定が別途必要です。コンテナ内の `127.0.0.1:8866` はそのままではiPhone/Windowsからアクセスできません。安全なポート転送が完成するまで、外部の `0.0.0.0` に安易に公開しないでください。

### Notebookとして実行

Jupyter環境を別途用意した場合は、`firewall_hands_on.ipynb` を開いてセルを順に実行できます。表示される実行パネルは、Voilàと同じ `ui.py` で実装されています。JupyterLab自体はこの教材の必須依存ではありません。

## 認証

1. 「デバイスコードでログイン」をタップ
2. 表示されるコードを `https://microsoft.com/devicelogin` で入力し、Azureアカウントで認証
3. 「契約一覧を更新」で学習用サブスクリプションを選択
4. 状態確認→無料準備の順に進める

Azure CLIの認証キャッシュはRDC環境のローカルに保存されます。**.azureフォルダ、認証結果、キーをGitHubへコミットしない**でください。

## 誤操作防止

- 画面表示だけではAzureリソースを作成しません。
- 操作対象は `rg-firewall-lab` と固定名のリソースに限定。
- 有料操作には明示チェックと `CREATE BILLABLE` の入力が必要。
- 削除には `DELETE rg-firewall-lab` の入力が必要。
- 管理タグとリソース名を検証し、不明なリソースがあると削除を拒否。
- 変更操作は同時実行せず、リソース作成が済んでいるときは原則再利用。
- Azureから確認した結果を表示。CLI操作失敗とネットワーク遮断を混同しない。

## 後片付け

画面最下部の「削除」を使用し、Azureリソースグループが存在しないことを確認してください。アプリが止まったりネットワークが切れたりした場合は、別途Azure PortalやCLIから当該グループの残存リソースを必ず確認してください。

```sh
az group show -n rg-firewall-lab
az group delete -n rg-firewall-lab --yes
az group exists -n rg-firewall-lab
```

最後のコマンドが `false` なら削除済みです。CLIで削除する場合はサブスクリプションを必ず確認し、**教材以外のリソースがないことを先に確認**してください。

## 開発・検証

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python build_notebook.py
.venv/bin/python -m pytest -q
```

`tests/test_lab.py` はAzure CLI呼び出しをモックし、作成→通信検証→削除とガード処理をテストします。**モックの成功は実際のAzureデプロイ成功を保証しません。** 実Azureでの検証には認証・クォータと有料操作が必要です。

## 注意点

- Firewall Basicの検査範囲にIDPSは含まれません。Premium検査機能は別教材の対象です。
- VM Run Commandの拡張機能やゲストエージェントが通信できないと、curlそのものが開始できないことがあります。その場合はFirewallによる拒否が証明されたとは扱いません。
- 検査対象のドメインは www.google.com と www.microsoft.com、送信元は WorkloadSubnet、プロトコルは HTTPS 443 です。
- Azureの提供リージョン、Free TrialのSKU利用可否、VMクォータにより作成が拒否される可能性があります。
- ローカルのVoilà Web画面には、アクセス制御を担保するHTTPSプロキシ/VPNが必須です。

参考: https://learn.microsoft.com/cli/azure/network/firewall および https://learn.microsoft.com/cli/azure/network/firewall/policy/rule-collection-group/collection
