"""Generate a reproducible Jupyter Notebook from the shared UI."""
from pathlib import Path
import nbformat as nbf

folder = Path(__file__).resolve().parent
nb = nbf.v4.new_notebook()
nb.metadata["kernelspec"] = {
    "name": "python3", "display_name": "Python 3", "language": "python"
}
nb.metadata["language_info"] = {"name": "python"}
nb.cells = [
    nbf.v4.new_markdown_cell(
        "# Azure Firewall Basic — iPhoneで実行するハンズオン\n\n"
        "**体験:** 通信を原則拒否し、Firewall Policyにルールを追加してGoogleのみ通過させます。\n\n"
        "このノートブックはWindowsホスト上のWSL2/Dockerで実行できます。"
        "同じノートブックをJupyterでセルごとに、Voilàでスマホ向けボタンUIとして表示します。\n\n"
        "### 進め方\n\n"
        "1. Azureの認証とサブスクリプション確認\n"
        "2. 無料のVNet・サブネット・Firewall Policy Basicの準備\n"
        "3. Azure Firewall Basic / Public IP / Ubuntu VM の作成（**有料**）\n"
        "4. VMサブネットにUDRを設定し、ルールなしで拒否を確認\n"
        "5. Google HTTPSのみ許可するApplication Ruleを設定して結果を比較\n"
        "6. 学習環境を削除して不存在を確認\n\n"
        "> **重要:** Firewall・Public IP・VMは削除するまで料金が発生します。"
        "Notebookを閉じてもAzureの料金は止まりません。"
    ),
    nbf.v4.new_markdown_cell(
        "## 第1章：接続と無料準備\n\n"
        "VNetのアドレス空間は 10.0.0.0/16、Firewallは 10.0.0.0/26、"
        "管理サブネットは 10.0.1.0/26、VMは 10.0.2.0/24 に配置します。"
    ),
    nbf.v4.new_code_cell("from ui import make_app\nmake_app()"),
    nbf.v4.new_markdown_cell(
        "## 第2章：通信制御の仕組み\n\n"
        "**Azure Firewall:** 実際にパケットを転送し、通信を制御するサービス。\n\n"
        "**Azure Firewall Policy:** 許可・拒否ルールの集合。"
        "今回はBasicを使うので、Premium固有のIDPS・TLSインスペクションは対象外。\n\n"
        "**UDR:** VMからインターネット向けの通信をFirewallへ流す経路設定。"
        "Policyを作るだけでは通信はFirewallを経由しません。\n\n"
        "**Application Rule:** HTTP(S)の宛先FQDNを使う許可ルール。"
        "今回は www.google.com:443 を許可し、www.microsoft.com との違いを観察します。\n\n"
        "### 考えてみること\n\n"
        "- Firewallを置くだけでは、なぜVMの通信を制御できないのでしょうか？\n"
        "- Policyのルール変更で結果が変わった場合、何を確認するとFirewallを通ったと判断できるでしょうか？\n"
        "- 今回使っていないPremiumのIDPSを適用するなら、どんな追加検査が必要でしょうか？"
    ),
]
nbf.validate(nb)
nbf.write(nb, folder / "firewall_hands_on.ipynb")
print("Created", folder / "firewall_hands_on.ipynb")
