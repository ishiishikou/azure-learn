"""Security preflight tests for the *shared* Jupyter and Voilà execution path.

All Azure calls are simulated. These tests must never contact Azure.
"""
from __future__ import annotations

import subprocess
import sys

import ipywidgets as w
import pytest

import lab
import notebook_helpers
from notebook_helpers import LearningSession
from test_lab import FakeAzureCLI


def mock_preflight(monkeypatch, fake: FakeAzureCLI):
    original = lab.AzureLab
    monkeypatch.setattr(lab, "AzureLab", lambda subscription: original(subscription, executor=fake))
    # The final mutating CLI command must not be called unless a test explicitly
    # provides a harmless stub.
    def forbidden(*a, **kw):
        raise AssertionError("Unexpected real Azure CLI subprocess")
    monkeypatch.setattr(notebook_helpers.subprocess, "run", forbidden)


def learning_session() -> LearningSession:
    session = LearningSession()
    session.picker = w.Dropdown(options=[("Study", "sub-test")], value="sub-test")
    session.paid_checkbox = w.Checkbox(value=True)
    session.paid_phrase = w.Text(value="CREATE BILLABLE")
    session.delete_phrase = w.Text(value="DELETE rg-firewall-lab")
    return session


def test_reject_unmanaged_group_before_network_create(monkeypatch):
    fake = FakeAzureCLI()
    fake.group = True
    fake.tagged = False
    mock_preflight(monkeypatch, fake)
    s = learning_session()
    with pytest.raises(RuntimeError, match="管理タグ"):
        s.run("az network vnet create -g rg-firewall-lab -n vnet-firewall-lab")
    assert not fake.vnet


def test_reject_existing_group_before_group_create(monkeypatch):
    fake = FakeAzureCLI()
    fake.group = True
    mock_preflight(monkeypatch, fake)
    s = learning_session()
    with pytest.raises(RuntimeError, match="すでに存在"):
        s.run("az group create -n rg-firewall-lab -l japaneast")


def test_reject_tag_takeover_of_populated_group(monkeypatch):
    fake = FakeAzureCLI()
    fake.group = True
    fake.resources["customer"] = {"name": "customer", "type": "Microsoft.Storage/storageAccounts"}
    mock_preflight(monkeypatch, fake)
    s = learning_session()
    with pytest.raises(RuntimeError, match="既存リソース"):
        s.run("az group update -n rg-firewall-lab --set tags.firewallLab=azure-firewall-mobile-handson-v1")
    assert not fake.tagged


def test_reject_unsafe_resource_type_even_with_known_name(monkeypatch):
    fake = FakeAzureCLI()
    fake.group = fake.tagged = True
    fake.resources[lab.VNET] = {"name": lab.VNET, "type": "Microsoft.Compute/virtualMachines"}
    mock_preflight(monkeypatch, fake)
    s = learning_session()
    with pytest.raises(RuntimeError, match="教材外"):
        s.run("az network vnet subnet create -g rg-firewall-lab --vnet-name vnet-firewall-lab -n WorkloadSubnet")


def test_recheck_group_before_delete_not_stale_inventory(monkeypatch):
    fake = FakeAzureCLI()
    fake.group = fake.tagged = True
    fake.resources["changed-after-check"] = {"name": "changed-after-check", "type": "Microsoft.Storage/storageAccounts"}
    mock_preflight(monkeypatch, fake)
    s = learning_session()
    with pytest.raises(RuntimeError, match="教材外"):
        s.run("az group delete -n rg-firewall-lab --yes", delete=True)
    assert fake.group


def test_managed_group_allows_only_read_only_safety_queries(monkeypatch):
    fake = FakeAzureCLI()
    fake.group = fake.tagged = True
    mock_preflight(monkeypatch, fake)
    s = learning_session()
    s.locked_subscription = "sub-test"
    # Preflight is permitted, but no mutation is actually invoked by this test.
    s._preflight(["az", "network", "vnet", "create", "-g", lab.RG, "-n", lab.VNET])
    operations = [argv[1:3] for argv in fake.calls]
    assert ["group", "exists"] in operations
    assert ["group", "show"] in operations
    assert ["resource", "list"] in operations
    assert not any("create" in cmd or "delete" in cmd for cmd in operations)


def test_reject_unscoped_changes_and_other_groups():
    s = learning_session()
    with pytest.raises(RuntimeError, match="scoped=False"):
        s.run("az group delete -n rg-firewall-lab --yes", delete=True, scoped=False)
    s.locked_subscription = "sub-test"
    with pytest.raises(RuntimeError, match="学習用リソースグループ"):
        s._preflight(["az", "network", "vnet", "create", "-g", "rg-other", "-n", "other"])


def test_shared_login_watchdog_terminates_silent_child(monkeypatch):
    original_popen = subprocess.Popen
    real_code = [sys.executable, "-c", "import time; time.sleep(6)"]
    def fake_popen(cmd, *args, **kwargs):
        return original_popen(real_code, *args, **kwargs)
    monkeypatch.setattr(notebook_helpers.subprocess, "Popen", fake_popen)
    monkeypatch.setattr(notebook_helpers, "LOGIN_TIMEOUT_SECONDS", 0.15)
    with pytest.raises(TimeoutError, match="期限内"):
        LearningSession().login()