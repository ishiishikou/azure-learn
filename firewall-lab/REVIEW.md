# 独立レビュー・終了判定（azure-firewall-lab）

このレビューは実装担当とは独立して行う。実装担当の成功報告を根拠とせず、コード・テスト・実際の実行ログを確認する。

## 目的
iPhone Safariから利用できるAzure Firewall Basicのハンズオン教材について、認証、無料準備、Firewall/VM/UDR、既定拒否、Google HTTPSのみ許可、通信試験、削除確認までの学習体験を安全に実現する。

## 完了条件（すべて満たすこと）
1. GitHub `ishiishikou/azure-learn/firewall-lab` に実装・README・テストが登録され、コミットSHAを確認した。
2. RDCでNotebook生成、Voilà起動、Web画面表示、iPhone相当の画面幅でのタップ操作が機能する。
3. 非認証・誤サブスクリプション・再実行・部分作成・通信失敗・削除失敗のケースがテストされる。
4. 実際のAzureサブスクリプションでVNet、Azure Firewall Policy Basic、Azure Firewall Basic、Public IP、Ubuntu VM、UDRを作成し、Azureから状態を再取得して確認する。
5. HTTPS拒否→`www.google.com`のみ許可→HTTPS接続結果の変化を確認する。ゲストエージェントの通信失敗をFirewallの拒否成功と誤認しない。
6. Azure Firewallを経由した証拠（有効な経路、Firewall診断ログ等）を取得し、単なるcurl失敗だけで成功扱いにしない。
7. 学習用グループを削除し、Azure側でグループと課金対象リソースの不存在を確認する。
8. 利用者のiPhone Safariから認証済みHTTPS経路で接続し、入力・実行・結果確認・削除の操作性を検証する。
9. 重大・高リスク指摘が0件で、残る制約と実測範囲をREADMEへ明記する。

## 独立レビュー手順
- リポジトリの対象ディレクトリ内のコードを読み、潜在的な問題を理由と行番号付きで報告する。
- `python -m pytest` など安全なローカルテストは実行してよい。
- Azure上のリソース作成・変更・削除はレビュー工程では禁止。
- シークレット表示・外部送信、コード改変、GitHubへのpushもレビュー工程では禁止。
- 実Azure未検証やiPhone未検証を、静的レビューやモックテストで代替したと主張しない。
- 指摘は `BLOCKER / HIGH / MEDIUM / LOW` に分け、ファイル・行・再現/理由・修正案を書く。
- 最後に終了判定を `COMPLETE`, `BLOCKED_BY_USER_ACTION`, `INCOMPLETE` のいずれか一つで示す。未検証事項と必要な証拠を添える。
- モデル名とレビュー実行時刻、参照したコミットSHAを明記する。指定モデルを実際に利用できなかった場合はその旨を明記する。

## 現時点の証拠（2026-11-11）
- RDC（Docker / WSL2）上でPython、Azure CLI、Voilàが動作。
- `tests/test_lab.py` の模擬Azure CLIテスト6件成功。
- RDC上のブラウザでVoilàの表示と、未認証時のボタン動作を確認。
- Azure CLIは未ログイン。実Azureでのデプロイ/拒否/許可/削除は未実施。
- iPhone SafariからのHTTPS接続は未検証。
- 独立したSol 6.1レビューは未実施。

この状態での終了判定は **INCOMPLETE**。コードの初期実装と模擬検証完了を、実機ハンズオン完成と取り違えないこと。
