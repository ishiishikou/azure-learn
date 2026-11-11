# Azure Firewall Basic — iPhone用ハンズオン

iPhone Safariで使えるAzure Firewall Basicの学習教材です。

**学習の正本は `firewall_hands_on.ipynb` です。** 1操作1セルを基本に、作成とAzureからの再取得を分け、CLIコマンド・その説明・実行結果をセルごとに確認できます。

補助の `mobile_dashboard.ipynb` はVoilàで表示するボタン操作画面です。こちらは自動操作を優先するため、Azureの仕組みを理解したい場合は学習Notebookを先に利用してください。



## 構成図（draw.io + PNG）

- 編集可能なdraw.io: `diagrams/azure-firewall-basic.drawio`
- draw.io編集用XML: `diagrams/azure-firewall-basic.drawio`
- 画像本体に編集用XMLも含むPNG: `diagrams/azure-firewall-basic.png`
- 生成スクリプト: `create_diagram.py`（draw.ioネイティブXML）
- PNG出力スクリプト: `diagrams/export_via_drawio.js`（draw.io公式の `xmlpng` エクスポート）
- 検証: `tests/test_diagram.py`（箱の包含、水平な経路、交差を増やさない接続、画像埋め込みの検査）
- 参考：draw.io公式Codex Skill（https://github.com/jgraph/drawio-mcp/blob/main/plugins/codex/drawio/skills/drawio/SKILL.md）

学習用Notebookの冒頭に画像を表示します。構成図は**予定構成**であり、Googleが許可されMicrosoftが拒否される図はルール適用後の期待動作です。実機での確認は未実施です。

Policy、Public IP、Route TableはVNetのサブネット内に配置するリソースではないため、図ではリソースグループ内のVNet外に分離しています。

> iPhoneからの安全な接続方法は [TAILSCALE_SETUP.md](TAILSCALE_SETUP.md) を参照してください。RDCコンテナへのTailscaleインストール、Serve有効化、iPhone SafariからのJupyterLab表示を確認済みです。

## iPhone向け学習画面（推奨）

**[スマホ学習UIを開く](/voila/render/mobile_learning.ipynb)**

- ファイル：`mobile_learning.ipynb`、表示ロジック：`mobile_learning.py`
- 学習用Notebook `firewall_hands_on.ipynb` から42のコードセルを読み出し、1操作ずつ表示します。
- iPhone幅に合わせた縦長画面で、目的・コマンド・実行ボタン・出力・前へ／次へを表示します。
- Azureサブスクリプションを選択し、途中で変更された場合は操作を拒否します。
- 有料操作と削除には確認文言を要求し、画面を開くだけでAzureを変更することはありません。
- JupyterLabのVoilà拡張を利用するため、**Tailscale Serveは既存の443→8888のままで使えます**。追加の外部公開ポートは不要です。
- 以前の `mobile_dashboard.ipynb` は一括実行用の補助画面であり、学習の中心ではありません。

通常のセル編集を希望する場合は、PC向けの `firewall_hands_on.ipynb` をJupyterLabで開いてください。

## 起動方法

1. **学習用Notebook（推奨）:** `./start-notebook.sh` でJupyterLabを起動し、`firewall_hands_on.ipynb` を開きます。個別のAzure CLIコマンドと結果、補足説明を確認します。
2. **操作補助画面:** `./start.sh` でVoilàを起動し、`mobile_dashboard.ipynb` をボタンUIとして表示します。

いずれもローカルのloopbackにバインドします。Safariからのアクセスには認証済みのHTTPSトンネル／プロキシが必要です。

**Notebookでは「すべて実行」を使わず、セルを順番に実行してください。** 途中から有料操作が含まれ、毎回状態を確認する構成です。

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
- 本リポジトリの firewall-lab フォルダで実行してください。学習用Notebookでは `./start-notebook.sh`、ボタン操作画面は `./start.sh` を使用します。

```sh
./start.sh
```

既存のRDC実行環境では Voilà と Azure CLI の動作を確認済みです。スマホからアクセス可能にするには、**認証された安全なHTTPS経路**が別途必要です。

### iPhoneからのアクセス

- **VS Code Remote Tunnelのポート転送:** 8866番ポートを転送し、iPhoneのSafariで認証済みの転送URLを開きます。統合ターミナルへの貼り付けは不要です。
- **Tailscale Serve（推奨）:** RDCのLinuxコンテナ内のTailscaleからJupyterLabの `127.0.0.1:8888` をHTTPSでtailnet内に公開します。Windows側へのVPN導入やポート開放は不要です。**Tailscale Funnelで一般公開しない**でください。

**Docker内にVoilàを起動した場合:** Dockerのポートをホストのループバックに公開するなど、ホストからそのポートに到達できる設定が別途必要です。コンテナ内の `127.0.0.1:8866` はそのままではiPhone/Windowsからアクセスできません。安全なポート転送が完成するまで、外部の `0.0.0.0` に安易に公開しないでください。

### Notebookとして実行

`./start-notebook.sh` でJupyterLabを起動し、`firewall_hands_on.ipynb` を開きます。JupyterLabが表示するトークン付きURLを、認証済みのトンネル経由で開いてください。

- セルのMarkdownを読んで、なぜその操作が必要なのか確認します。
- 次のコードセルに実際のAzure CLIコマンドが1個記載されています。
- 実行したコマンドとJSON出力が同じセルに表示されます。
- 有料操作は明示のチェックと確認文字列が必要です。
- 削除後はAzureのgroup existsがfalseであることを確認します。

JupyterLabはスマートフォンでのタップ操作について未検証です。Safariの実機で操作できない場合はVoilàの補助画面を利用してください。

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

## 検証範囲（2026-11-11）

- 模擬Azure CLIによるライフサイクルのテストを実施しています。
- 学習NotebookはCLIが1セル1操作を基本とする構造に分解しています。
- 実際のAzureへのデプロイ、Azure Firewall診断ログ、iPhone Safariの実機操作は未検証です。
- Sol 6.1の初回独立レビューでは、通信試験の判定、既存リソースの検証、失敗系テストが不足していると指摘されました。これらを改善していますが、**実Azure・iPhoneの実測が揃うまで終了判定はINCOMPLETE**です。


### VM Run Command の制約（重要）

WorkloadSubnetで既定ルートをFirewallに向け、許可ルールを一切設定しない場合、VMエージェントや拡張機能が必要とするAzure通信まで遮断するおそれがあります。したがって、Run Commandが返答しなかった場合は**FirewallによるHTTPS拒否の成功とは扱いません**。実機検証でAzure VM Agentの要件を確認し、必要なAzure宛アウトバウンドだけを許可したうえで検証手順を調整する必要があります。現在はこの実機検証が未完了です。