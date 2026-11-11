# Azure Firewall Basic 構成図：Sol 6.1レビュー記録

## 対象

- Repository: \`ishiishikou/azure-learn\`
- Scope: \`firewall-lab/diagrams/azure-firewall-basic.drawio\`、そのPNG、Notebook、生成元、関連テスト
- 最初のレビュー対象: \`3b90fdd722f68a0437c9a957733adde4a0230ba1\` → **REVISE**
- 修正後のレビュー対象: \`df7078098d4bea821f28588963076afc1c272358\` → **PASS（構成図のみ）**
- Reviewer: RDCのCodex CLI v0.167.1にて \`-m gpt-6.1-sol\` を明示指定
- 実行日: 2026-11-11
- レビューの方法: GitHubコネクタ経由で固定コミットのコード・図形XML・PNG・Notebookを確認。ファイルとAzureを変更しない独立レビュー。

## 初回レビューで指摘された3件（すべてMedium）

1. **VMのIP表記**：\`IPなし\` を \`Private IPあり（自動割当）／ Public IPなし\` に修正。
2. **Microsoft宛の拒否経路**：Firewallを通過してMicrosoftに届くような赤破線を廃止し、Firewallの遮断記号で終端。宛先に転送されないことを明記。
3. **編集可能な接続関係**：draw.ioの7エッジに \`source\` / \`target\` を設定。RG → VNet → Subnet → Firewall/VMなど、63個の子形状に親子関係（相対座標）を付与。

## 再レビュー結果

**構成図：PASS**

- 3件とも修正を確認。
- Azure Firewall Basicのサブネット配置、管理サブネット、Public IP、Firewall Policy、UDRの関係はMicrosoft公式構成と概ね整合。
- draw.io XMLとPNGは確認可能で、Notebookの相対参照が正しい。
- 緑の経路・赤の遮断はルール適用後の期待動作として提示され、未デプロイの実測値とは区別されている。
- 新たな重大または高リスクの問題は見つからなかった。

再レビューの実行ログには \`model: gpt-6.1-sol\` と出力されています。ツールがモデルの内部識別子の完全な保証を提供するわけではありません。

## 実装担当の検証（独立レビューと区別）

- diagrams.net公式のembedプロトコルでdraw.ioを読み込み、PNGに書き出した。
- 出力PNGは2688×1533の画像。
- RDCの画像表示で読みやすさを確認した。
- \`pytest\` は30件成功（2026-11-11）。
- NotebookのMarkdownは \`diagrams/azure-firewall-basic.png\` を参照する。

## 未完了（構成図のPASSには含まない）

- 実際のiPhone SafariからのNotebook表示・セル実行
- RDC内Tailscaleのインストール、認証、Serveの検証
- Azure Firewall/VM/UDRの本番Azureでのデプロイ・通信検証・削除
- Firewall診断ログによる遮断理由の確認

**ハンズオン全体の終了判定は引き続き INCOMPLETE です。**

参照：
- https://learn.microsoft.com/en-us/azure/firewall/deploy-firewall-basic-portal-policy
- https://www.drawio.com/docs/reference/embed-mode/

## 2026-11-11 最新図面の再レビュー（公式draw.io Skill準拠）

- 対象コミット: `9b100850f998823ad97e005517dd26ad1ef07e71`
- レビュアー: RDC内Codex CLI `gpt-6.1-sol` を明示指定
- **構成図のみの判定: PASS**
- 直前のREVISE指摘（下段の`route_name`、`policy_id`、`pip_data`、`pip_mgmt`におけるラベルの欠け）を解消したことをPNG目視、draw.io XML、生成コードで確認
- PNGは2688×1563。画像に埋め込まれたdraw.io XMLもレビューされ、図形・接続関係の一致を確認
- 構成図の構造テストは実装側RDCで33件成功
- レビュアー側のローカルsandboxは起動できず、GitHubコネクタでファイルを読み取って検証。レビュー側のローカルテスト実行は未実施
- iPhone Safariの実機操作とAzure実リソースでの構築・通信・削除は**依然未検証**。ハンズオン全体の完了判定はINCOMPLETE