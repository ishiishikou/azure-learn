"""One visible Azure CLI invocation per learning-notebook cell."""
from __future__ import annotations
import json
import os
import shlex
import subprocess
import ipywidgets as widgets
from IPython.display import display


class LearningSession:
    def __init__(self):
        self.subscription = ""
        self.locked_subscription = None
        self.paid_checkbox = None
        self.paid_phrase = None
        self.delete_phrase = None
        self.picker = None

    def login(self):
        command = ["az", "login", "--use-device-code"]
        print("$", shlex.join(command), flush=True)
        print("表示される https://microsoft.com/devicelogin にアクセスしてコードを入力してください。", flush=True)
        # Forward the device code to the notebook cell in real time.
        # A child process writing directly to its parent's fd may not reach
        # Jupyter's IOPub channel, so explicitly stream it through print.
        proc = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, bufsize=1
        )
        try:
            for line in proc.stdout:
                print(line.rstrip(), flush=True)
            ret = proc.wait(timeout=900)
        except Exception:
            proc.kill()
            proc.wait()
            raise
        if ret:
            raise RuntimeError("Azure CLI認証に失敗しました。")
        return ret

    def select_subscription(self, subscriptions):
        if self.locked_subscription:
            raise RuntimeError("この学習セッションはサブスクリプションが固定されています。切り替えは新しいカーネルで開始してください。")
        if not isinstance(subscriptions, list):
            raise RuntimeError("サブスクリプション一覧の形式が不正です。")
        enabled = [(f"{a['name']} ({a['id']})", a["id"]) for a in subscriptions
                   if isinstance(a, dict) and a.get("state") == "Enabled" and a.get("id")]
        self.picker = widgets.Dropdown(
            options=[("サブスクリプションを選択", "")] + enabled,
            description="Azure契約:",
            layout=widgets.Layout(width="98%"),
            style={"description_width": "initial"}
        )
        display(self.picker)
        print("この欄で対象のAzureサブスクリプションを選びます。以降のコマンドに --subscription が自動追加されます。")
        return self.picker

    def approvals(self):
        self.paid_checkbox = widgets.Checkbox(
            description="Firewall・VM・Public IPの課金と削除の必要性を理解しました",
            indent=False, layout=widgets.Layout(width="98%")
        )
        self.paid_phrase = widgets.Text(
            description="有料操作の確認:", placeholder="CREATE BILLABLE",
            layout=widgets.Layout(width="98%"),
            style={"description_width": "initial"}
        )
        display(self.paid_checkbox, self.paid_phrase)
        return self.paid_checkbox

    def cleanup_approval(self):
        self.delete_phrase = widgets.Text(
            description="削除確認:", placeholder="DELETE rg-firewall-lab",
            layout=widgets.Layout(width="98%"),
            style={"description_width": "initial"}
        )
        display(self.delete_phrase)

    def run(self, command: str, *, paid=False, delete=False, scoped=True):
        if not isinstance(command, str):
            raise TypeError("コマンドは文字列で指定してください。")
        args = shlex.split(command)
        if not args or args[0] != "az":
            raise ValueError("Azure CLIのコマンドを1つだけ指定してください。")
        if scoped:
            if self.picker is None or not self.picker.value:
                raise RuntimeError("先にサブスクリプションを選択してください。")
            choice = self.picker.value
            if self.locked_subscription is None:
                self.locked_subscription = choice
                print("サブスクリプションを固定しました:", choice, flush=True)
            elif self.locked_subscription != choice:
                raise RuntimeError("サブスクリプションが途中で変更されました。安全のため操作を中断します。元の契約に戻すかカーネルを再起動してください。")
            args += ["--subscription", self.locked_subscription]
            self.subscription = self.locked_subscription
        if paid and not (self.paid_checkbox is not None and self.paid_checkbox.value
                         and self.paid_phrase is not None
                         and self.paid_phrase.value.strip() == "CREATE BILLABLE"):
            raise RuntimeError("有料操作の確認欄にチェックし、CREATE BILLABLE を入力してください。")
        if delete and not (self.delete_phrase is not None
                           and self.delete_phrase.value.strip() == "DELETE rg-firewall-lab"):
            raise RuntimeError("削除するには DELETE rg-firewall-lab を入力してください。")
        if "--output" not in args and "-o" not in args:
            args += ["--output", "json"]
        args += ["--only-show-errors"]
        print("$", shlex.join(args), flush=True)
        result = subprocess.run(args, capture_output=True, text=True,
                                check=False, timeout=1200)
        if result.returncode:
            print("失敗:\n", result.stderr[-2500:], flush=True)
            raise RuntimeError("Azure CLI失敗: 終了コード " + str(result.returncode))
        if result.stderr.strip():
            print("Azure CLI警告:\n" + result.stderr[-1400:], flush=True)
        output = result.stdout.strip()
        try:
            parsed = json.loads(output) if output else None
        except json.JSONDecodeError:
            parsed = output
        if parsed is None:
            print("コマンドは完了しました（標準出力なし）。")
        elif isinstance(parsed, str):
            print(parsed[:5000])
        else:
            print(json.dumps(parsed, indent=2, ensure_ascii=False)[:12000])
        return parsed

    @staticmethod
    def expect_group_empty(resources):
        if resources != []:
            raise RuntimeError("学習グループ内に既存リソースがあります。次の作成手順を実行せず確認してください。")
        print("確認: リソースグループ内は空です。")

    @staticmethod
    def verify_deleted(state):
        if state is not False:
            raise RuntimeError("Azure側でリソースグループの不存在を確認できませんでした。")
        print("確認: リソースグループは存在しません。")