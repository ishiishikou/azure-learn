"""Phone-friendly UI contract tests; never contact Azure."""
from __future__ import annotations
from pathlib import Path

import nbformat
import ipywidgets as w

import mobile_learning


ROOT = Path(__file__).resolve().parents[1]


def test_mobile_ui_reads_exact_canonical_learning_steps():
    steps = mobile_learning.steps_from_notebook()
    book = nbformat.read(ROOT / "firewall_hands_on.ipynb", as_version=4)
    original_code = [
        book.cells[i+1].source for i, c in enumerate(book.cells[:-1])
        if c.cell_type == "markdown" and c.source.startswith("### ")
    ]
    assert len(steps) == len(original_code) == 42
    assert [s["code"] for s in steps] == original_code
    assert sum(s["paid"] for s in steps) >= 10
    assert sum(s["delete"] for s in steps) == 1
    assert "az network vnet create" in " ".join(s["code"] for s in steps)
    assert "az group delete" in steps[-2]["code"]


def test_mobile_ui_open_does_not_execute_azure_cli(monkeypatch):
    items = []
    def forbidden(*args, **kwargs):
        raise AssertionError("Opening the page must not run commands")
    monkeypatch.setattr(mobile_learning.subprocess, "Popen", forbidden)
    monkeypatch.setattr("notebook_helpers.subprocess.run", forbidden)
    monkeypatch.setattr(mobile_learning, "display", items.append)

    assert mobile_learning.make_mobile_learning_app() is None
    assert len(items) == 1
    app = items[0]
    assert isinstance(app, w.VBox)
    visible_buttons = [x for x in app.children if isinstance(x, w.Button)]
    assert any("実行" in b.description for b in visible_buttons)
    assert any(isinstance(x, w.IntProgress) and x.max == 42 for x in app.children)


def test_mobile_ui_does_not_run_code_not_in_the_notebook():
    s = mobile_learning.steps_from_notebook()
    assert len({x["index"] for x in s}) == len(s)
    assert not any("make_app()" in x["code"] for x in s)
    assert not any("make_mobile_learning_app()" in x["code"] for x in s)


def test_html_explanations_are_escaped():
    rendered = mobile_learning._rich("<script>alert(1)</script>\n\n**Azure**")
    assert "<script>" not in rendered
    assert "&lt;script&gt;" in rendered
    assert "<strong>Azure</strong>" in rendered