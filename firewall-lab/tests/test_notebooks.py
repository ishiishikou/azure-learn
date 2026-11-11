"""Tests for granularity and guardrails of the learning notebook."""
from __future__ import annotations
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import nbformat
import pytest
import ipywidgets as widgets

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from notebook_helpers import LearningSession


ROOT = Path(__file__).resolve().parents[1]


def test_notebook_has_independent_visible_cli_steps():
    nb = nbformat.read(ROOT / "firewall_hands_on.ipynb", as_version=4)
    nbformat.validate(nb)
    code = [cell.source for cell in nb.cells if cell.cell_type == "code"]
    assert len(code) >= 35
    assert sum("session.run(" in s for s in code) >= 30
    assert any("az network vnet create " in s for s in code)
    assert any("az network vnet subnet create " in s for s in code)
    assert any("az network route-table route create " in s for s in code)
    assert any("az network vnet subnet update " in s for s in code)
    assert any("az group delete " in s for s in code)
    assert not any("make_app()" in s for s in code)
    for source in code:
        compile(source, "<notebook-cell>", "exec")


def test_dashboard_is_separate():
    nb = nbformat.read(ROOT / "mobile_dashboard.ipynb", as_version=4)
    nbformat.validate(nb)
    assert len(nb.cells) == 2
    assert "make_app()" in nb.cells[1].source


def test_paid_command_requires_consent(monkeypatch):
    calls = []
    def fake_run(*args, **kwargs):
        calls.append(args)
        return SimpleNamespace(returncode=0, stdout='{"ok":true}', stderr='')
    monkeypatch.setattr("notebook_helpers.subprocess.run", fake_run)
    s = LearningSession()
    s.picker = widgets.Dropdown(options=[("study", "sub-test")], value="sub-test")
    with pytest.raises(RuntimeError, match="有料操作"):
        s.run("az network firewall create -g rg-firewall-lab", paid=True)
    assert calls == []
    s.paid_checkbox = widgets.Checkbox(value=True)
    s.paid_phrase = widgets.Text(value="CREATE BILLABLE")
    assert s.run("az network firewall create -g rg-firewall-lab", paid=True) == {"ok": True}
    argv = calls[0][0]
    assert argv[0] == "az"
    assert argv.count("--subscription") == 1
    assert argv[argv.index("--subscription") + 1] == "sub-test"


def test_delete_command_requires_exact_text(monkeypatch):
    called = []
    monkeypatch.setattr(
        "notebook_helpers.subprocess.run",
        lambda *a, **kw: called.append(a) or SimpleNamespace(
            returncode=0, stdout="null", stderr="")
    )
    s = LearningSession()
    s.picker = widgets.Dropdown(options=[("study", "sub-test")], value="sub-test")
    s.delete_phrase = widgets.Text(value="DELETE another-group")
    with pytest.raises(RuntimeError, match="削除するには"):
        s.run("az group delete -n rg-firewall-lab --yes", delete=True)
    assert not called


def test_malformed_command_not_executed(monkeypatch):
    called = []
    monkeypatch.setattr("notebook_helpers.subprocess.run", lambda *a, **kw: called.append(a))
    s = LearningSession()
    with pytest.raises(ValueError, match="Azure CLI"):
        s.run("bash -c 'echo unsafe'")
    assert not called


def test_group_delete_check_is_strict():
    s = LearningSession()
    with pytest.raises(RuntimeError):
        s.verify_deleted("false")
    with pytest.raises(RuntimeError):
        s.verify_deleted(None)
    s.verify_deleted(False)