"""Account/tenant login configuration and Alpine network fallback tests."""
from pathlib import Path
import os
import pytest

import notebook_helpers
from cli_runtime import azure_cli_env


def test_explicit_tenant_from_environment(monkeypatch):
    tenant = "12345678-1234-1234-1234-123456789012"
    monkeypatch.setenv("AZURE_LAB_TENANT_ID", tenant)
    assert notebook_helpers.configured_tenant() == tenant
    assert notebook_helpers.login_command() == [
        "az", "login", "--use-device-code", "--tenant", tenant
    ]


def test_tenant_config_is_not_embedded_in_repository(monkeypatch, tmp_path):
    private = tmp_path / "azure-tenant-id"
    private.write_text("12345678-1234-1234-1234-123456789012\n")
    monkeypatch.delenv("AZURE_LAB_TENANT_ID", raising=False)
    monkeypatch.setattr(notebook_helpers, "TENANT_PATH", private)
    assert notebook_helpers.configured_tenant() == private.read_text().strip()


def test_invalid_tenant_rejected_before_login(monkeypatch):
    monkeypatch.setenv("AZURE_LAB_TENANT_ID", "../other")
    with pytest.raises(ValueError, match="テナント"):
        notebook_helpers.login_command()


def test_no_tenant_is_backward_compatible(monkeypatch, tmp_path):
    monkeypatch.delenv("AZURE_LAB_TENANT_ID", raising=False)
    monkeypatch.setattr(notebook_helpers, "TENANT_PATH", tmp_path/"missing")
    assert notebook_helpers.login_command() == ["az", "login", "--use-device-code"]


def test_cli_runtime_preserves_existing_pythonpath(monkeypatch):
    monkeypatch.setenv("PYTHONPATH", "/my/normal/modules")
    env = azure_cli_env()
    assert env["PYTHONPATH"].endswith("/my/normal/modules")
    assert env is not os.environ


def test_ipv4_workaround_stays_local():
    config = Path(__file__).resolve().parents[1]/".gitignore"
    assert ".state/" in config.read_text()
    # Never commit local Azure tenant ID or sitecustomize under .state.