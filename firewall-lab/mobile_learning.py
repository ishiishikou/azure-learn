"""Responsive, one-Azure-CLI-action-per-step Voilà front-end for an Azure learning notebook.

The canonical exercise is firewall_hands_on.ipynb. This module presents the same
trusted code cells one at a time, with a visible command, rationale, and output.
No Azure commands run when the app is opened.
"""
from __future__ import annotations

import contextlib
import html
import io
import re
import subprocess
import threading
from pathlib import Path

import ipywidgets as w
import nbformat
from IPython.display import display, HTML
from notebook_helpers import LearningSession

ROOT = Path(__file__).resolve().parent
CANONICAL_NOTEBOOK = ROOT / "firewall_hands_on.ipynb"


def steps_from_notebook(path: Path = CANONICAL_NOTEBOOK) -> list[dict]:
    notebook = nbformat.read(path, as_version=4)
    nbformat.validate(notebook)
    steps = []
    section = "0. はじめに"
    section_note = ""
    opening_note = ""
    for i, cell in enumerate(notebook.cells):
        if cell.cell_type != "markdown":
            continue
        text = cell.source.strip()
        if text.startswith("## "):
            section = text.splitlines()[0].removeprefix("## ").strip()
            section_note = text.split("\n\n", 1)[1].strip() if "\n\n" in text else ""
            if not steps and section.startswith("Azure Firewall Basic"):
                opening_note = section_note
            # Reflection and completion chapters are read-only learning pages.
            if section.startswith("9.") or section.startswith("復習"):
                steps.append({
                    "index": len(steps), "section": section,
                    "section_note": section_note,
                    "title": section, "purpose": section_note,
                    "code": "", "paid": False, "delete": False, "note": True,
                })
        elif text.startswith("### "):
            if i + 1 >= len(notebook.cells) or notebook.cells[i + 1].cell_type != "code":
                raise ValueError(f"Explanatory step {i} has no following code cell")
            title = text.splitlines()[0][4:].strip()
            purpose = text.split("\n\n", 1)[1].strip() if "\n\n" in text else ""
            code = notebook.cells[i + 1].source
            compile(code, f"<learning-step-{i}>", "exec")
            if title.startswith("0-"):
                section = "0. はじめに"
                section_note = opening_note
            steps.append({
                "index": len(steps),
                "section": section,
                "section_note": section_note,
                "title": title,
                "purpose": purpose,
                "code": code,
                "paid": "paid=True" in code,
                "delete": "delete=True" in code,
            })
    if len(steps) < 30:
        raise ValueError("Expected the full 1-command-per-step learning notebook")
    return steps


def _rich(text: str) -> str:
    escaped = html.escape(text, quote=True)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped, flags=re.S)
    escaped = re.sub(r"\`([^\`]+)\`", r"<code>\1</code>", escaped)
    return escaped.replace("\n\n", "</p><p>").replace("\n", "<br>")


class _WidgetStream(io.TextIOBase):
    """Forward stdout to a widget as complete lines; no long-running buffer."""
    def __init__(self, consumer):
        super().__init__()
        self.consumer = consumer
        self.partial = ""

    def write(self, data):
        if not isinstance(data, str):
            data = str(data)
        self.partial += data
        if "\n" in self.partial:
            full, _, self.partial = self.partial.rpartition("\n")
            if full:
                self.consumer(full)
        return len(data)

    def flush(self):
        if self.partial:
            self.consumer(self.partial)
            self.partial = ""


def make_mobile_learning_app():
    steps = steps_from_notebook()
    session = LearningSession()
    accounts_dropdown = w.Dropdown(
        options=[("Azureの契約一覧を読み込んでください", "")],
        value="", description="対象契約",
        style={"description_width": "initial"},
        layout=w.Layout(width="100%"),
    )
    session.picker = accounts_dropdown
    session.paid_checkbox = w.Checkbox(
        value=False,
        description="Firewall・VM・Public IPの継続課金を理解しました",
        indent=False, layout=w.Layout(width="100%"),
    )
    session.paid_phrase = w.Text(
        placeholder="CREATE BILLABLE",
        description="実行確認",
        style={"description_width": "initial"},
        layout=w.Layout(width="100%"),
    )
    session.delete_phrase = w.Text(
        placeholder="DELETE rg-firewall-lab",
        description="削除確認",
        style={"description_width": "initial"},
        layout=w.Layout(width="100%"),
    )

    # All step variables (fw_ip, inventory, etc.) belong to this one Voilà kernel.
    # Never pull executable Python from a remote URL.
    namespace = {"session": session, "__name__": "__main__"}

    section_names = list(dict.fromkeys(step["section"] for step in steps))
    sections = w.Dropdown(
        options=section_names, value=section_names[0],
        description="章", style={"description_width": "initial"},
        layout=w.Layout(width="100%"),
    )
    step_picker = w.Dropdown(
        description="操作", style={"description_width": "initial"},
        layout=w.Layout(width="100%"),
    )
    title = w.HTML()
    intro = w.HTML()
    command = w.HTML()
    progress = w.IntProgress(min=1, max=len(steps), value=1,
                             layout=w.Layout(width="100%"), bar_style="info")
    result = w.Textarea(
        value="最初の操作を選択してください。ここからAzureの変更は自動実行されません。",
        disabled=True,
        layout=w.Layout(width="100%", height="210px"),
    )
    state = w.HTML("<span class='lab-status'>未実行</span>")
    button_prev = w.Button(description="前へ", icon="arrow-left",
                           layout=w.Layout(width="48%", height="48px"))
    button_next = w.Button(description="次へ", icon="arrow-right",
                           layout=w.Layout(width="48%", height="48px"))
    button_run = w.Button(description="この操作を実行", icon="play",
                          button_style="primary", layout=w.Layout(width="100%", height="54px"))

    account_box = w.VBox([
        w.HTML("<div class='lab-mini-title'>Azure サブスクリプション</div>"
               "<div class='lab-muted'>認証して契約一覧を取得した後に選択します。"
               "一度コマンドを実行すると対象契約は固定されます。</div>"),
        accounts_dropdown,
    ], layout=w.Layout(width="100%"))
    paid_box = w.VBox([
        w.HTML("<div class='lab-alert'><strong>有料の操作です。</strong>"
               "Azure Firewall、Public IP、VMは削除まで課金されます。"
               "実行前に下のチェックと確認文字列が必要です。</div>"),
        session.paid_checkbox, session.paid_phrase,
    ], layout=w.Layout(width="100%"))
    delete_box = w.VBox([
        w.HTML("<div class='lab-alert lab-danger'><strong>削除操作です。</strong>"
               "専用リソースグループ全体を削除します。戻せません。"
               "前のステップで中身と管理タグを確認してください。</div>"),
        session.delete_phrase,
    ], layout=w.Layout(width="100%"))

    nav_lock = threading.Lock()
    active_index = [0]
    completed: set[int] = set()
    changing = [False]
    result_memory: dict[int, str] = {}

    def append_log(text):
        previous = result.value
        new_text = (previous + "\n" + str(text)) if previous else str(text)
        result.value = new_text[-14000:]

    def step_list(section):
        return [(f"{step['title']}", step["index"])
                for step in steps if step["section"] == section]

    def go(index):
        if not 0 <= index < len(steps):
            return
        changing[0] = True
        try:
            step = steps[index]
            active_index[0] = index
            sections.value = step["section"]
            step_picker.options = step_list(step["section"])
            step_picker.value = index
            progress.value = index + 1
            title.value = (
                "<div class='lab-step-badge'>STEP " + str(index + 1) + " / "
                + str(len(steps)) + "</div><div class='lab-heading'>"
                + html.escape(step["title"]) + "</div>"
            )
            section_note = step["section_note"]
            chapter_details = (
                "<details class='lab-muted'><summary>この章の説明・注意点を見る</summary>"
                "<div class='lab-explanation'><p>" + _rich(step["section_note"])
                + "</p></div></details>"
                if step["section_note"] and not step.get("note") else ""
            )
            intro.value = (
                "<div class='lab-subsection'>" + html.escape(step["section"]) + "</div>"
                + ("<div class='lab-explanation'><p>" + _rich(step["purpose"]) + "</p></div>")
                + chapter_details
            )
            command.value = (
                "<div class='lab-mini-title'>このページは説明のみです</div>"
                if step.get("note") else (
                    "<div class='lab-mini-title'>実行するコード / Azure CLI</div>"
                    "<div class='lab-muted'>何が実行されるかを確認してからボタンを押します。</div>"
                    "<pre class='lab-code'><code>" + html.escape(step["code"]) + "</code></pre>"
                    "<div class='lab-muted'>変更・削除時には管理タグなどを確認する読み取りCLIが"
                    "安全のため追加実行されます。出力欄にそのコマンドと結果を表示します。</div>"
                )
            )
            is_paid_step = step["paid"] or step["code"].strip() == "session.approvals()"
            is_delete_step = step["delete"] or step["code"].strip() == "session.cleanup_approval()"
            paid_box.layout.display = "flex" if is_paid_step else "none"
            delete_box.layout.display = "flex" if is_delete_step else "none"
            button_run.button_style = ("danger" if step["delete"] else
                                       "warning" if step["paid"] else "primary")
            button_run.description = ("学習メモ（実行なし）" if step.get("note") else
                                      "削除を実行" if step["delete"] else
                                      "この有料操作を実行" if step["paid"] else
                                      "この操作を実行")
            button_run.disabled = bool(step.get("note"))
            button_prev.disabled = index == 0
            button_next.disabled = index == len(steps) - 1
            result.value = result_memory.get(
                index, "操作はありません。内容を確認し、次へ進んでください。"
                if step.get("note") else "このステップは未実行です.")
            state.value = ("<span class='lab-muted'>読むだけのステップ</span>"
                           if step.get("note") else
                           "<span class='lab-ok'>完了</span>" if index in completed
                           else "<span class='lab-status'>未実行</span>")
        finally:
            changing[0] = False

    def navigate_section(change):
        if changing[0] or change.get("name") != "value" or not change["new"]:
            return
        matches = step_list(change["new"])
        if matches:
            go(matches[0][1])

    def navigate_step(change):
        if changing[0] or change.get("name") != "value" or change["new"] is None:
            return
        go(int(change["new"]))

    sections.observe(navigate_section, names="value")
    step_picker.observe(navigate_step, names="value")
    button_prev.on_click(lambda _: go(active_index[0] - 1))
    button_next.on_click(lambda _: go(active_index[0] + 1))

    def run_login():
        # Reuse the SAME transparent device-login implementation as Jupyter.
        # No separate CLI command or tenant selection is hidden in the phone UI.
        from notebook_helpers import configured_tenant
        if configured_tenant():
            append_log("Azure Portalで確認したテナントを明示してサインインします。")
        stream = _WidgetStream(append_log)
        try:
            with contextlib.redirect_stdout(stream):
                session.login()
        finally:
            stream.flush()

    def run_step(index):
        step = steps[index]
        code = step["code"]
        # Special UI steps from the canonical notebook: these controls must be
        # persistent, not recreated inside temporary output widgets.
        if "from notebook_helpers import LearningSession" in code:
            append_log("Azure CLIの実行準備ができました。Azureリソースは変更していません。")
            return
        if code.strip() == "session.login()":
            run_login()
            return
        if code.startswith('accounts = session.run("az account list --all"'):
            capture = io.StringIO()
            with contextlib.redirect_stdout(capture):
                accounts = session.run("az account list --all", scoped=False)
            if not isinstance(accounts, list):
                raise RuntimeError("Azure CLIから契約一覧を取得できません。")
            append_log(capture.getvalue()[-8000:])
            namespace["accounts"] = accounts
            valid = [(str(item.get("name")) + " / " + str(item.get("id")),
                      item.get("id"))
                     for item in accounts
                     if isinstance(item, dict) and item.get("id") and item.get("state") == "Enabled"]
            if not valid:
                raise RuntimeError("アクセス可能なAzureサブスクリプションが見つかりません。")
            accounts_dropdown.options = [("契約を選択", "")] + valid
            if len(valid) == 1:
                accounts_dropdown.value = valid[0][1]
            append_log(f"{len(valid)}件の利用可能なAzureサブスクリプションを取得しました。"
                       "上の対象契約を確認してください。\n"
                       + "\n".join(name for name, _ in valid))
            return
        if code.strip() == "session.select_subscription(accounts)":
            if not accounts_dropdown.value:
                raise RuntimeError("上の『Azureサブスクリプション』から契約を選択してください。")
            if session.locked_subscription and accounts_dropdown.value != session.locked_subscription:
                raise RuntimeError("途中でサブスクリプションが変更されたため停止しました。")
            append_log("選択済み: " + accounts_dropdown.value
                       + "\n以降のAzure CLIにはサブスクリプションが明示されます。")
            return
        if code.strip() == "session.approvals()":
            if not session.paid_checkbox.value or session.paid_phrase.value.strip() != "CREATE BILLABLE":
                raise RuntimeError("継続課金の確認にチェックし、CREATE BILLABLE を入力してください。")
            append_log("有料操作の確認欄を入力済みです。次のステップも個別に実行してください。")
            return
        if code.strip() == "session.cleanup_approval()":
            if session.delete_phrase.value.strip() != "DELETE rg-firewall-lab":
                raise RuntimeError("DELETE rg-firewall-lab と正確に入力してください。")
            append_log("削除の確認欄を入力済みです。削除処理はまだ実行していません。")
            return
        stream = _WidgetStream(append_log)
        try:
            with contextlib.redirect_stdout(stream):
                exec(compile(code, "<trusted-learning-notebook>", "exec"), namespace)
        finally:
            stream.flush()

    def run_action(_):
        if not nav_lock.acquire(blocking=False):
            append_log("別の操作が実行中です。")
            return
        idx = active_index[0]
        step = steps[idx]
        for widget in (button_run, button_next, button_prev, step_picker, sections):
            widget.disabled = True
        result.value = ""
        state.value = "<span class='lab-running'>実行中（終了までこの画面を閉じないでください）</span>"

        def work():
            succeeded = False
            try:
                run_step(idx)
                succeeded = True
                completed.add(idx)
                append_log("操作完了。結果を確認し、必要なら次へ進んでください。")
            except Exception as exc:
                append_log("エラー：" + str(exc))
            finally:
                result_memory[idx] = result.value
                state.value = ("<span class='lab-ok'>完了</span>" if succeeded
                               else "<span class='lab-error'>失敗 / 要確認</span>")
                button_run.disabled = bool(step.get("note"))
                button_next.disabled = idx == len(steps) - 1
                button_prev.disabled = idx == 0
                step_picker.disabled = False
                sections.disabled = False
                nav_lock.release()
        threading.Thread(target=work, daemon=True).start()

    button_run.on_click(run_action)
    banner = w.HTML("""
        <style>
        body { overflow-x: hidden; }
        .widget-button { font-size:16px!important; border-radius:12px!important; }
        .widget-dropdown select, .widget-text input { font-size:16px!important; min-height:44px!important; }
        .lab-top { background:linear-gradient(125deg,#164d7c,#2276ab);color:#fff;
                   padding:20px 17px;border-radius:16px;box-sizing:border-box; }
        .lab-top h2 { margin:0 0 9px;font-size:21px;line-height:1.4;color:#fff; }
        .lab-top p { margin:0;color:#e4f1fc;font-size:14px;line-height:1.55; }
        .lab-step-badge {font-size:13px;font-weight:700;color:#317bb1;margin:8px 0; }
        .lab-heading {font-size:21px;font-weight:700;line-height:1.35;color:#193550;margin:5px 0 8px;}
        .lab-subsection {font-size:13px;color:#557c9d;margin:6px 0;}
        .lab-explanation {line-height:1.7;font-size:15px;color:#2f4050;}
        .lab-explanation p {margin:8px 0;}
        .lab-mini-title {font-size:15px;font-weight:700;margin:8px 0;color:#17324c;}
        .lab-muted {font-size:13px;color:#62798b;line-height:1.55;}
        .lab-code {box-sizing:border-box;width:100%;max-width:100%;overflow-x:auto;
                  white-space:pre-wrap;overflow-wrap:anywhere;background:#132d44;color:#eef6ff;
                  padding:13px;border-radius:11px;font:12.5px/1.65 monospace;margin:8px 0 12px;}
        .lab-alert {border:1px solid #dfc18c;background:#fff8e9;border-radius:12px;
                   padding:11px;margin:8px 0;line-height:1.5;font-size:14px;}
        .lab-danger {background:#fff0f1;border-color:#e2abab;}
        .lab-ok {color:#148052;font-weight:700;}
        .lab-error {color:#b43242;font-weight:700;}
        .lab-running {color:#a56a17;font-weight:700;}
        .lab-status {color:#5f7487;}
        .lab-image {width:100%;height:auto;border:1px solid #d4e3ed;border-radius:10px;}
        .lab-help {font-size:13px;line-height:1.6;color:#5c7282;}
        .lab-help a{color:#2877ac;}
        .jp-RenderedHTMLCommon {max-width:100%!important;}
        @media(max-width:640px){
          .voila-notebook, .jp-OutputArea-output {max-width:100%!important;}
          .jp-Notebook {padding:0!important;}
          .widget-label {font-size:14px!important;}
        }
        </style>
        <div class='lab-top'>
          <h2>Azure Firewall Basic<br>スマホ実践ハンズオン</h2>
          <p>1つの操作を選ぶ → コマンドを読む → 実行 → 結果を見る。<br>
          画面を開くだけではAzureを変更しません。</p>
        </div>
    """)
    footer = w.HTML("""
      <div class='lab-help'>
       <details><summary>ネットワーク構成図を見る</summary>
       <img class='lab-image' src='/files/diagrams/azure-firewall-basic.png'
            alt='Azure Firewall Basic ネットワーク構成図'>
       </details>
       <p>Notebookのコードや全セルを確認したい場合：
         <a href='/lab/tree/firewall_hands_on.ipynb' target='_blank'
         rel='noopener noreferrer'>PC向けJupyterLabを開く</a></p>
       <p><strong>料金注意：</strong> Firewall/VM/Public IPはブラウザを閉じても課金されます。
       実験後は必ず学習用リソースグループを削除してください。</p>
      </div>
    """)
    app = w.VBox(
        [
            banner,
            footer,
            w.HTML("<div class='lab-mini-title'>学習の章・操作を選択</div>"),
            sections, step_picker, progress,
            title, intro, command,
            account_box, paid_box, delete_box,
            button_run, state,
            w.HTML("<div class='lab-mini-title'>この操作の実行結果</div>"),
            result,
            w.HBox([button_prev, button_next],
                   layout=w.Layout(width="100%", justify_content="space-between")),
        ],
        layout=w.Layout(width="100%", max_width="580px", padding="10px",
                        margin="0 auto"),
    )
    go(0)
    display(app)
    return None