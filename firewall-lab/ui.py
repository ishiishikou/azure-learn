"""ipywidgets front-end. Importing this module never changes Azure resources."""
import html
import subprocess
import threading
import ipywidgets as w
from IPython.display import display, HTML
from lab import AzureLab, LabError, RG

def make_app():
    display(HTML("<style>.widget-button{min-height:45px!important;border-radius:8px!important}"
                 ".widget-label{white-space:normal!important}</style>"))
    log = w.Output(layout=w.Layout(width="100%", height="310px", overflow="auto", border="1px solid #a8b3bf", padding="8px"))
    state = w.HTML("<b>状態:</b> 未実行。画面を開いただけではAzureに変更しません。")
    account = w.Dropdown(options=[("未選択", "")], description="Azure契約:",
                         style={"description_width": "initial"}, layout=w.Layout(width="98%"))
    login_btn = w.Button(description="デバイスコードでログイン", icon="sign-in")
    refresh_btn = w.Button(description="契約一覧を更新", icon="refresh")
    ack = w.Checkbox(value=False, description="有料リソースは削除するまで課金されると理解しました",
                     indent=False, layout=w.Layout(width="98%"))
    paid_text = w.Text(placeholder="CREATE BILLABLE", description="有料操作:",
                       style={"description_width": "initial"}, layout=w.Layout(width="98%"))
    delete_text = w.Text(placeholder="DELETE rg-firewall-lab", description="削除確認:",
                         style={"description_width": "initial"}, layout=w.Layout(width="98%"))
    busy = threading.Lock()
    buttons = []
    def output(message):
        with log:
            print(str(message))
    lab = AzureLab(log=output)

    def refresh(_=None):
        try:
            entries = lab.accounts()
            previous = account.value
            account.options = [("選択してください", "")] + [
                (str(a.get("name")) + " (" + str(a.get("id"))[:8] + "…)", a.get("id"))
                for a in entries
            ]
            ids = [a.get("id") for a in entries]
            if previous in ids:
                account.value = previous
            elif len(ids) == 1:
                account.value = ids[0]
            output("接続可能なAzureサブスクリプション: " + str(len(entries)) + " 件")
        except Exception as e:
            output("契約一覧の取得に失敗: " + str(e))

    def login(_):
        if not busy.acquire(blocking=False):
            output("他の処理が実行中です。")
            return
        def work():
            try:
                state.value = "<b>状態:</b> ログイン中"
                output("表示されたコードを https://microsoft.com/devicelogin で入力してください。")
                p = subprocess.Popen(["az", "login", "--use-device-code", "--only-show-errors"],
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
                for line in p.stdout:
                    if "accessToken" not in line and "refreshToken" not in line:
                        output(line.rstrip()[:900])
                rc = p.wait(timeout=700)
                if rc:
                    raise LabError("ログインに失敗しました。終了コード: " + str(rc))
                refresh()
                state.value = "<b>状態:</b> ログイン済み"
            except Exception as e:
                state.value = "<b>状態:</b> ログイン未完了"
                output(str(e))
            finally:
                busy.release()
        threading.Thread(target=work, daemon=True).start()
    login_btn.on_click(login)
    refresh_btn.on_click(refresh)

    def act(command, billable=False, destructive=False):
        if not account.value:
            output("最初に契約一覧を読み込み、対象サブスクリプションを選択してください。")
            return
        if billable and not (ack.value and paid_text.value.strip() == "CREATE BILLABLE"):
            output("料金確認にチェックし、CREATE BILLABLE と入力してください。")
            return
        if destructive and delete_text.value.strip() != "DELETE " + RG:
            output("削除するには DELETE " + RG + " と入力してください。")
            return
        if not busy.acquire(blocking=False):
            output("他の処理が実行中です。")
            return
        def work():
            try:
                for b in buttons:
                    b.disabled = True
                state.value = "<b>状態:</b> " + html.escape(command) + " 実行中"
                lab.choose(account.value)
                result = lab.run_named(command)
                output(result)
                state.value = "<b>状態:</b> " + html.escape(command) + " 完了"
            except Exception as e:
                output("エラー: " + str(e))
                state.value = "<b>状態:</b> エラー。ログを確認してください。"
            finally:
                for b in buttons:
                    b.disabled = False
                busy.release()
        threading.Thread(target=work, daemon=True).start()

    def button(title, command, *, paid=False, delete=False):
        b = w.Button(description=title, layout=w.Layout(width="98%", margin="4px 0"),
                     button_style="danger" if delete else ("warning" if paid else ""))
        b.on_click(lambda _: act(command, billable=paid, destructive=delete))
        buttons.append(b)
        return b

    def section(title, body=""):
        return w.HTML("<h3>" + html.escape(title) + "</h3><p>" + body + "</p>")

    display(w.VBox([
        section("Azure Firewall Basic 実機ハンズオン", "iPhone Safariからタップで実行。操作結果は下部に追記されます。"),
        section("0. Azureアカウント確認", "認証時のデバイスコードは画面のログに表示されます。"),
        w.HBox([login_btn, refresh_btn]),
        account,
        button("現在のリソースを確認（読み取りのみ）", "status"),
        section("1〜3. 無料の準備", "リソースグループ、VNet、Firewall Policy Basicを準備します。"),
        button("1. 学習用リソースグループを準備", "group"),
        button("2. VNetと3サブネットを作成", "vnet"),
        button("3. Firewall Policy Basicを作成", "policy"),
        section("4〜6. 有料リソース",
                "<b>注意:</b> Firewall・Public IP・VMはブラウザを閉じても料金がかかります。"
                "無料クレジットや予算アラートは自動停止の保証ではありません。"),
        ack, paid_text,
        button("4. Public IPとFirewall Basicを作成", "firewall", paid=True),
        button("5. Ubuntu VMを作成", "vm", paid=True),
        button("6. VMの通信経路をFirewallへ（UDR）", "route"),
        section("7〜9. Firewallの許可・拒否",
                "最初にGoogleとMicrosoftへの通信を試し、Googleだけを許可して再実行します。"),
        button("7. 許可ルールなしでcurlを実行", "deny_test"),
        button("8. GoogleへのHTTPSだけを許可", "allow"),
        button("9. もう一度curlを実行", "allow_test"),
        section("終了. 学習環境の削除",
                "学習用リソースグループ内のリソースを全部削除します。管理タグと対象名を確認し、教材外のリソースがあれば停止します。"),
        delete_text,
        button("学習用リソースグループを削除", "cleanup", delete=True),
        section("実行ログ"), state, log,
    ], layout=w.Layout(width="100%", max_width="760px")))
