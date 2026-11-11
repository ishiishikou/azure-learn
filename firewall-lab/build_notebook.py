"""Build two notebooks: transparent CLI learning and Voilà touch dashboard."""
from pathlib import Path
import nbformat as nb

folder = Path(__file__).resolve().parent
learning = nb.v4.new_notebook()
learning.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
learning.metadata["language_info"] = {"name": "python"}

def section(title, detail):
    learning.cells.append(nb.v4.new_markdown_cell("## " + title + "\n\n" + detail))
def step(title, purpose, command=None, *, paid=False, code=None):
    statement = ("このセルはAzure CLIの実行ではなく、Notebook内の準備や選択を行います。"
                 if code is not None and "session.run(" not in code and "session.login()" not in code
                 else "次のセルは、記載のAzure CLIコマンドを1つだけ実行し、結果を同じセルに表示します。")
    learning.cells.append(nb.v4.new_markdown_cell(
        "### " + title + "\n\n" + purpose + "\n\n" + statement
    ))
    if code is None:
        code = "session.run(" + repr(command) + (", paid=True" if paid else "") + ")"
    learning.cells.append(nb.v4.new_code_cell(code))

section("Azure Firewall Basic — 1操作ずつ学ぶ実機ハンズオン",
"""**iPhone版:** [スマートフォン向け学習画面を開く](/voila/render/mobile_learning.ipynb)。コマンドと結果を1操作ずつ確認できます。

操作の中身を隠さない学習用Notebookです。原則1コードセルにつき1つのAzure CLIコマンドを実行します。
コマンドは実行直前に、指定したサブスクリプションIDを含めて表示されます。

- 無料の準備: リソースグループ・VNet・Firewall Policy
- **有料:** Public IP、Azure Firewall Basic、Ubuntu VM
- 通信経路: ルートテーブルをVMサブネットに適用
- 通信の検査: GoogleとMicrosoftへのHTTPSを比較
- 最後に必ず学習リソースを削除

**警告:** Notebookを閉じてもAzure料金は止まりません。Notebookの「すべて実行」は使わないでください。
変更・削除コマンドの直前には、共通の安全ガードがAzure CLIでRGの管理タグと最新リソース一覧を確認し、
実行した追加の読み取りコマンドも出力します。これらは学習上の1操作に対する事前確認です。""")
step("0-1. Notebookの実行セッションを用意",
     "Python補助機能を読み込むだけでAzure操作は行いません。",
     code="from notebook_helpers import LearningSession\nsession = LearningSession()\nprint('Azure CLIをまだ実行していません')")
step("0-2. Azureにサインイン",
     "デバイスコード認証用のコードとURLが表示されます。iPhone Safariで認証します。",
     code="session.login()")
step("0-3. Azureサブスクリプション一覧を確認",
     "請求先になる契約名とIDを確認します。",
     code='accounts = session.run("az account list --all", scoped=False)')
step("0-4. Azureサブスクリプションを選択",
     "以降のコマンドにはサブスクリプションIDが自動で付加されます。",
     code="session.select_subscription(accounts)")

section("1. リソースグループ",
"今回の学習は専用のrg-firewall-labを利用します。以前の学習で空のグループが作成済みですが、必ず現在の状態を確認します。")
step("1-1. RGの状態を読む","存在しない場合はエラーになります。その場合のみ次の新規作成を行います。",
     'az group show -n rg-firewall-lab')
step("1-2（存在しない場合のみ）. RGを新規作成","既存のRGがある場合は実行しません。",
     'az group create -n rg-firewall-lab -l japaneast --tags firewallLab=azure-firewall-mobile-handson-v1')
step("1-3. RG内のリソースを確認","空でない場合は、教材外のリソースを変更しないためここで中止します。",
     code='existing = session.run("az resource list -g rg-firewall-lab")\nsession.expect_group_empty(existing)')
step("1-4. RGに教材用タグを付ける","操作画面でも同じタグを使い、安全のため教材のRGを識別します。",
     'az group update -n rg-firewall-lab --set tags.firewallLab=azure-firewall-mobile-handson-v1')
step("1-5. タグが反映されたか再取得","単に更新コマンドが成功しただけでなく、実際のタグを読みます。",
     code='group = session.run("az group show -n rg-firewall-lab")\nassert group["tags"]["firewallLab"] == "azure-firewall-mobile-handson-v1"')

section("2. ネットワーク — VNetと3サブネット",
"""VNetは10.0.0.0/16です。次の3サブネットを別の操作として作ります。

- AzureFirewallSubnet：10.0.0.0/26 （Firewall本体）
- AzureFirewallManagementSubnet：10.0.1.0/26 （管理）
- WorkloadSubnet：10.0.2.0/24 （VM）

※ VNetの最初の作成コマンドでは、最初のサブネットも同時に作られます。""")
step("2-1. VNet + Firewallサブネットを作成","最初のAzureFirewallSubnetはFirewall本体の配置先です。",
     'az network vnet create -g rg-firewall-lab -n vnet-firewall-lab -l japaneast --address-prefix 10.0.0.0/16 --subnet-name AzureFirewallSubnet --subnet-prefix 10.0.0.0/26')
step("2-2. 管理サブネットを追加","Basic SKUで必要な管理用の独立したサブネットです。",
     'az network vnet subnet create -g rg-firewall-lab --vnet-name vnet-firewall-lab -n AzureFirewallManagementSubnet --address-prefix 10.0.1.0/26')
step("2-3. VMサブネットを追加","通信制御の対象になるVMを配置します。",
     'az network vnet subnet create -g rg-firewall-lab --vnet-name vnet-firewall-lab -n WorkloadSubnet --address-prefix 10.0.2.0/24')
step("2-4. サブネットを確認","3つの名前とIPアドレス範囲が期待どおりか見ます。",
     'az network vnet subnet list -g rg-firewall-lab --vnet-name vnet-firewall-lab')

section("3. Firewall Policy Basic",
"Policyはルールを管理する独立したリソースです。Firewall本体をまだ作っていないため、これだけでは通信制御されません。")
step("3-1. Policyを作成","Firewall PolicyのSKUをBasicにします。",
     'az network firewall policy create -g rg-firewall-lab -n policy-firewall-lab -l japaneast --sku Basic')
step("3-2. Policyを確認","AzureからBasic SKUの実際の設定を読み返します。",
     'az network firewall policy show -g rg-firewall-lab -n policy-firewall-lab')

section("4. 有料リソース — Firewall本体",
"""以下は課金を伴います。Public IPとAzure Firewallは、作成後に削除するまで課金されます。
課金に関するチェックと確認文言を入れるまで、有料コマンドは実行しません。""")
step("4-0. 課金の確認","画面でチェックを入れ、CREATE BILLABLEと入力します。まだAzure変更はありません。",
     code="session.approvals()")
step("4-1. 通信用Public IPを作る","Firewall本体のデータプレーン用Standard Public IPです。",
     'az network public-ip create -g rg-firewall-lab -n pip-firewall-lab -l japaneast --sku Standard --allocation-method Static',paid=True)
step("4-2. 管理用Public IPを作る","Firewall Basicの管理通信を別のIPで扱います。",
     'az network public-ip create -g rg-firewall-lab -n pip-firewall-mgmt-lab -l japaneast --sku Standard --allocation-method Static',paid=True)
step("4-3. Public IPを確認","2つのStandard Public IPが作成されたか確認します。",
     'az network public-ip list -g rg-firewall-lab')
step("4-4. Firewall Basicを作成","VNet、2つのPublic IP、Policyを関連付けます。Firewallの時間課金が始まります。",
     'az network firewall create -g rg-firewall-lab -n fw-firewall-lab -l japaneast --sku AZFW_VNet --tier Basic --vnet-name vnet-firewall-lab --conf-name fw-ipconfig --public-ip pip-firewall-lab --m-conf-name fw-mgmtconfig --m-public-ip pip-firewall-mgmt-lab --firewall-policy policy-firewall-lab',paid=True)
step("4-5. Firewallの状態とPrivate IPを確認","Private IPはUDRに使うため控えます。SKU・Policy・IPを画面で確認します。",
     code='fw = session.run("az network firewall show -g rg-firewall-lab -n fw-firewall-lab")\nfw_ip = fw["ipConfigurations"][0]["privateIPAddress"]\nprint("Firewall Private IP:", fw_ip)')

section("5. Ubuntu VM",
"VMはWorkloadSubnet内に置き、Public IPは割り当てません。Run CommandでVM内部からcurlを実行します。")
step("5-1. VM用NICを作成","NICとサブネットの関係がVMの通信経路に関係します。",
     'az network nic create -g rg-firewall-lab -n nic-firewall-lab -l japaneast --vnet-name vnet-firewall-lab --subnet WorkloadSubnet',paid=True)
step("5-2. NICにPublic IPが付いていないことを確認","NICのIP構成とsubnet参照を読み取ります。",
     'az network nic show -g rg-firewall-lab -n nic-firewall-lab')
step("5-3. Ubuntu VMを作成","Standard_B1sのUbuntu 22.04 VMを作ります。ディスクも課金対象です。",
     'az vm create -g rg-firewall-lab -n vm-firewall-lab -l japaneast --nics nic-firewall-lab --image Ubuntu2204 --size Standard_B1s --storage-sku Standard_LRS --os-disk-name osdisk-firewall-lab --admin-username azureuser --generate-ssh-keys',paid=True)
step("5-4. VMを確認","Azureに記録されたVMのサイズとネットワーク参照を確認します。",
     'az vm show -g rg-firewall-lab -n vm-firewall-lab')

section("6. UDR — なぜFirewallへ通信が流れるのか",
"Firewallが存在するだけではVMの通信は通りません。ルートテーブル・既定ルート・サブネット関連付けの3つの変更を分けます。")
step("6-1. ルートテーブルを作る","まだどのサブネットにも適用されない入れ物を作成します。",
     'az network route-table create -g rg-firewall-lab -n rt-firewall-lab -l japaneast',paid=True)
step("6-2. 既定ルートを作る","0.0.0.0/0の転送先をFirewallのPrivate IPに指定します。",
     code='assert fw_ip\nsession.run(f"az network route-table route create -g rg-firewall-lab --route-table-name rt-firewall-lab -n default-via-firewall --address-prefix 0.0.0.0/0 --next-hop-type VirtualAppliance --next-hop-ip-address {fw_ip}", paid=True)')
step("6-3. ルートを読み返す","nextHopTypeとIPを確認します。",
     'az network route-table route show -g rg-firewall-lab --route-table-name rt-firewall-lab -n default-via-firewall')
step("6-4. VMサブネットへルートテーブルを関連付ける",
     "**この操作から**WorkloadSubnetの外向き通信がFirewallへ向かいます。",
     'az network vnet subnet update -g rg-firewall-lab --vnet-name vnet-firewall-lab -n WorkloadSubnet --route-table rt-firewall-lab',paid=True)
step("6-5. サブネットの設定を読み返す","関連付けたルートテーブルのIDを確認します。",
     'az network vnet subnet show -g rg-firewall-lab --vnet-name vnet-firewall-lab -n WorkloadSubnet')
step("6-6. NICの有効経路を確認","NICから見て0.0.0.0/0がVirtualApplianceへ向いていることを調べます。",
     'az network nic show-effective-route-table -g rg-firewall-lab -n nic-firewall-lab')

section("7. ルールなしで通信試験",
"""Firewall Policyに許可ルールがない状態で、GoogleとMicrosoftへのHTTPS結果を測ります。
curlの失敗だけではFirewall遮断と断定できません。HTTP 403/500でもHTTP応答が届いているため遮断ではありません。
DNS失敗（curl 6）、TLS証明書エラー（60）、タイムアウト（28）、接続失敗（7）を区別します。
また、Firewall経由のAzure宛送信が遮断されるとVM Run Commandが使えなくなる可能性があります。
この場合はFirewallの拒否試験が成功したと判定せず、VMエージェント用通信の許可や別の観測方法を検討してください。""")
step("7-1. ルールグループ一覧を確認","ルールがない前提であることを確かめます。",
     'az network firewall policy rule-collection-group list -g rg-firewall-lab --policy-name policy-firewall-lab')
step("7-2. VM内のcurlで2ホストをテスト","DNS・終了コード・HTTPステータスを分けて表示します。",
     code='''import shlex
probe = "for host in www.google.com www.microsoft.com; do if getent ahostsv4 $host >/dev/null 2>&1; then dns=ok; else dns=fail; fi; code=$(curl -I -sS -o /dev/null -w '%{http_code}' --connect-timeout 10 --max-time 20 https://$host); rc=$?; echo RESULT host=$host dns=$dns exit=$rc http=$code; done"
before = session.run("az vm run-command invoke -g rg-firewall-lab -n vm-firewall-lab --command-id RunShellScript --scripts " + shlex.quote(probe), paid=True)''')

section("8. GoogleへのHTTPS通信だけ許可",
"Rule Collection Groupを作り、その中にApplication Ruleを追加します。2つのAzure CLIコマンドに分けます。")
step("8-1. Rule Collection Groupを作成","ルール集合を置く優先順位200のグループです。",
     'az network firewall policy rule-collection-group create -g rg-firewall-lab --policy-name policy-firewall-lab -n rcg-web-lab --priority 200',paid=True)
step("8-2. Googleだけ許可するルールを追加","WorkloadSubnetからwww.google.comへのHTTPS 443に限定します。",
     'az network firewall policy rule-collection-group collection add-filter-collection -g rg-firewall-lab --policy-name policy-firewall-lab --rule-collection-group-name rcg-web-lab --name allow-google --collection-priority 100 --action Allow --rule-name google-https --rule-type ApplicationRule --source-addresses 10.0.2.0/24 --protocols Https=443 --target-fqdns www.google.com',paid=True)
step("8-3. Policyのルールを再取得","許可する送信元、FQDN、プロトコル、優先順位を確認します。",
     'az network firewall policy rule-collection-group show -g rg-firewall-lab --policy-name policy-firewall-lab -n rcg-web-lab')
step("8-4. curlを再実行して比較","同じコマンドでGoogle成功、Microsoft拒否となることを観察します。",
     code='after = session.run("az vm run-command invoke -g rg-firewall-lab -n vm-firewall-lab --command-id RunShellScript --scripts " + shlex.quote(probe), paid=True)')

section("9. 学習の理解を確認",
"""1. Policyを作成しただけでは、なぜ通信制御が始まらないのでしょうか？
2. 既定ルート0.0.0.0/0とは、何を表しているでしょうか？
3. GoogleとMicrosoftで結果が異なる理由を、Firewall PolicyとApplication Ruleの言葉で説明できますか？

**検証上の注意:** Firewall診断ログは別途Azure Monitorの設定を要します。
このNotebookでは自動構築していないため、単にcurlが失敗しただけではFirewallによる拒否を証明できません。""")

section("10. 学習終了とAzureリソースの削除（必須）",
"Firewall/VM/Public IPは削除完了まで料金が続きます。削除前にグループ内の実際のリソースを確認します。")
step("10-1. 削除対象を一覧表示","教材以外のリソースが混ざった場合は中止してください。",
     code='inventory = session.run("az resource list -g rg-firewall-lab")\nprint("削除候補:", [(r.get("name"), r.get("type")) for r in inventory])')
step("10-2. 教材用タグを確認","教材用のタグがあることを確認します。",
     code='owned = session.run("az group show -n rg-firewall-lab")\nif (owned.get("tags") or {}).get("firewallLab") != "azure-firewall-mobile-handson-v1":\n    raise RuntimeError("管理タグが一致しません")')
step("10-3. 削除承認を入力","DELETE rg-firewall-labと入力するまでは削除できません。Azureの変更はありません。",
     code="session.cleanup_approval()")
step("10-4. リソースグループを削除",
     "元に戻せません。実行直前に**共通の安全確認**として管理タグ・現在のリソース一覧をAzureから再取得し、"
     "教材外のリソースがあれば削除を停止します。実行した確認CLIも出力に表示します。",
     code='session.run("az group delete -n rg-firewall-lab --yes", delete=True)')
step("10-5. 削除完了をAzureから確認","falseならグループが存在しません。",
     code='exists = session.run("az group exists -n rg-firewall-lab")\nsession.verify_deleted(exists)')

section("復習と完了判定",
"各セルで行ったCLI操作とAzureの応答を照合し、どの操作がどんな変更を生んだか振り返ってください。"
"実Azureの動作証拠が揃わなければ、模擬検証や画面表示の成功だけで完了とは判定しません。")

learning.cells.insert(1, nb.v4.new_markdown_cell(
    "## 今回の構成図（draw.ioで編集可能）\n\n"
    "以下は**構築予定の構成**です。"
    "Azure内のリソースとインターネット上の通信先のみを記載しています。\n\n"
    "![Azure Firewall Basic 学習用ネットワーク構成図](diagrams/azure-firewall-basic.png)\n\n"
    "[編集可能なdraw.io図を開く](diagrams/azure-firewall-basic.drawio)\n\n"
    "> Firewall Policy、Public IP、UDRは独立したAzureリソースであり、"
    "サブネットの内部に配置されるものではありません。"
    "緑/赤の経路はGoogle許可ルール適用後の**期待動作**を示します。"
    "実測済みではありません。"
))
nb.validate(learning)
nb.write(learning,folder/"firewall_hands_on.ipynb")

dashboard=nb.v4.new_notebook(cells=[
    nb.v4.new_markdown_cell("# Azure Firewall Basic — モバイル操作補助画面\n\n"
        "ボタン操作で実行する補助ツールです。各CLIと説明を学ぶNotebookは firewall_hands_on.ipynb を開いてください。"
        "有料リソースは削除するまで継続課金されます。"),
    nb.v4.new_code_cell("from ui import make_app\nmake_app()"),
])
dashboard.metadata["kernelspec"] = learning.metadata["kernelspec"]
dashboard.metadata["language_info"] = learning.metadata["language_info"]
nb.validate(dashboard)
nb.write(dashboard,folder/"mobile_dashboard.ipynb")
print("learning notebook",len(learning.cells),"cells")
print("mobile dashboard",len(dashboard.cells),"cells")

# Smartphone-first educational app: every button corresponds to ONE canonical
# learning-notebook cell, with visible code, rationale, and output.
mobile_learning = nb.v4.new_notebook(cells=[
    nb.v4.new_markdown_cell(
        "# Azure Firewall Basic — スマートフォン版\n\n"
        "このページはVoilàによりスマホ向けUIで表示します。"
        "実際の操作内容はfirewall_hands_on.ipynbの各コードセルと共通です。"
        "画面表示だけではAzureのリソースは作成しません。"
    ),
    nb.v4.new_code_cell("from mobile_learning import make_mobile_learning_app\nmake_mobile_learning_app()"),
])
mobile_learning.metadata["kernelspec"] = learning.metadata["kernelspec"]
mobile_learning.metadata["language_info"] = learning.metadata["language_info"]
nb.validate(mobile_learning)
nb.write(mobile_learning, folder / "mobile_learning.ipynb")
print("mobile_learning notebook", len(mobile_learning.cells), "cells")