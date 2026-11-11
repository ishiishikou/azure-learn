"""Azure Firewall Basic hands-on actions (no writes happen on import)."""
from __future__ import annotations

import json
import os
import re
import subprocess
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

RG = "rg-firewall-lab"
LOCATION = "japaneast"
VNET = "vnet-firewall-lab"
POLICY = "policy-firewall-lab"
FW = "fw-firewall-lab"
VM = "vm-firewall-lab"
NIC = "nic-firewall-lab"
DISK = "osdisk-firewall-lab"
PIP_DATA = "pip-firewall-lab"
PIP_MGMT = "pip-firewall-mgmt-lab"
ROUTE_TABLE = "rt-firewall-lab"
RCG = "rcg-web-lab"
TAG_KEY = "firewallLab"
TAG_VALUE = "azure-firewall-mobile-handson-v1"
SUBNETS = {
    "AzureFirewallSubnet": "10.0.0.0/26",
    "AzureFirewallManagementSubnet": "10.0.1.0/26",
    "WorkloadSubnet": "10.0.2.0/24",
}
RESOURCE_TYPES = {
    VNET: "microsoft.network/virtualnetworks",
    POLICY: "microsoft.network/firewallpolicies",
    FW: "microsoft.network/azurefirewalls",
    VM: "microsoft.compute/virtualmachines",
    NIC: "microsoft.network/networkinterfaces",
    DISK: "microsoft.compute/disks",
    PIP_DATA: "microsoft.network/publicipaddresses",
    PIP_MGMT: "microsoft.network/publicipaddresses",
    ROUTE_TABLE: "microsoft.network/routetables",
}
MAX_COMMAND_SECONDS = 1200


class LabError(RuntimeError):
    pass


@dataclass
class CLIResult:
    argv: list[str]
    stdout: str
    stderr: str
    returncode: int


def run_cli(
    args: list[str], *,
    subscription: str | None = None,
    timeout: int = MAX_COMMAND_SECONDS,
    executor: Callable | None = None,
) -> CLIResult:
    argv = ["az", *args]
    if subscription:
        argv += ["--subscription", subscription]
    argv += ["--only-show-errors", "-o", "json"]
    if executor is None:
        try:
            proc = subprocess.run(
                argv, capture_output=True, text=True, timeout=timeout,
                env=os.environ.copy(), check=False,
            )
        except FileNotFoundError as exc:
            raise LabError("Azure CLI (az) が見つかりません。") from exc
        except subprocess.TimeoutExpired as exc:
            raise LabError(f"コマンドが {timeout} 秒でタイムアウトしました: {' '.join(argv[:5])}") from exc
        result = CLIResult(argv, proc.stdout, proc.stderr, proc.returncode)
    else:
        result = executor(argv)
    if result.returncode != 0:
        raise LabError(
            "Azure CLI 実行失敗 (code " + str(result.returncode) + "):\n"
            + " ".join(result.argv[:8]) + "\n"
            + (result.stderr or result.stdout)[-1300:]
        )
    return result


class AzureLab:
    def __init__(self, subscription: str = "", executor: Callable | None = None, log: Callable | None = None):
        self.subscription = subscription.strip()
        self.executor = executor
        self.log = log or (lambda msg: None)
        self.lock = threading.Lock()

    def emit(self, message: str):
        self.log(message)

    def az(self, args: list[str], *, scoped: bool = True, timeout: int = MAX_COMMAND_SECONDS):
        if scoped and not self.subscription:
            raise LabError("サブスクリプションが未選択です。")
        result = run_cli(args, subscription=self.subscription if scoped else None, timeout=timeout, executor=self.executor)
        output = result.stdout.strip()
        try:
            return json.loads(output) if output else None
        except json.JSONDecodeError:
            return output

    def accounts(self) -> list[dict]:
        result = self.az(["account", "list", "--all"], scoped=False)
        if not isinstance(result, list):
            raise LabError("Azureのアカウント一覧を取得できません。ログインを確認してください。")
        return [a for a in result if a.get("state") == "Enabled"]

    def choose(self, subscription_id: str):
        match = [x for x in self.accounts() if x.get("id") == subscription_id]
        if not match:
            raise LabError("選択したサブスクリプションにアクセスできません。")
        self.subscription = subscription_id
        self.emit(f"対象サブスクリプション: {match[0].get('name')} ({subscription_id})")

    def group_exists(self):
        return str(self.az(["group", "exists", "-n", RG])).lower() == "true"

    def resources(self) -> list[dict]:
        if not self.group_exists():
            return []
        result = self.az(["resource", "list", "-g", RG])
        return result if isinstance(result, list) else []

    def status(self) -> str:
        account = self.az(["account", "show"])
        lines = [f"サブスクリプション: {account.get('name')} / {account.get('id')}"]
        if not self.group_exists():
            lines.append("学習用リソースグループ: なし（課金リソースなし）")
            return "\n".join(lines)
        group = self.az(["group", "show", "-n", RG])
        resources = self.resources()
        lines.append(f"リソースグループ: {RG} / タグ {group.get('tags', {}).get(TAG_KEY, '(未設定)')}")
        lines.append(f"リソース数: {len(resources)}")
        lines.extend(f"- {x.get('name')} [{x.get('type')}]" for x in resources)
        return "\n".join(lines)

    def require_owned_group(self):
        if not self.group_exists():
            raise LabError("リソースグループがありません。無料準備から始めてください。")
        group = self.az(["group", "show", "-n", RG])
        if (group.get("tags") or {}).get(TAG_KEY) != TAG_VALUE:
            raise LabError("管理タグが一致しません。この教材以外のグループを変更しないため処理を中止しました。")

    def prepare_group(self):
        if not self.group_exists():
            self.emit("学習用リソースグループを作成")
            self.az(["group", "create", "-n", RG, "-l", LOCATION, "--tags", f"{TAG_KEY}={TAG_VALUE}"])
        else:
            group = self.az(["group", "show", "-n", RG])
            tag = (group.get("tags") or {}).get(TAG_KEY)
            if tag != TAG_VALUE:
                if self.resources():
                    raise LabError("既存リソースが入った未管理グループのため変更しません。")
                self.emit("空の既存グループに教材用タグを付与")
                self.az(["group", "update", "-n", RG, "--set", f"tags.{TAG_KEY}={TAG_VALUE}"])
        self.require_owned_group()
        return "リソースグループを確認しました。"

    def names(self, args: list[str]) -> dict[str, dict]:
        records = self.az(args)
        if not isinstance(records, list):
            raise LabError("リソース一覧の形式が不正です。")
        return {r["name"]: r for r in records}

    def prepare_vnet(self):
        self.require_owned_group()
        vnets = self.names(["network", "vnet", "list", "-g", RG])
        if VNET not in vnets:
            self.emit("VNet 10.0.0.0/16 を作成")
            self.az(["network", "vnet", "create", "-g", RG, "-n", VNET, "-l", LOCATION,
                     "--address-prefix", "10.0.0.0/16", "--subnet-name", "AzureFirewallSubnet",
                     "--subnet-prefix", SUBNETS["AzureFirewallSubnet"]])
        else:
            prefixes = vnets[VNET].get("addressSpace", {}).get("addressPrefixes", [])
            if "10.0.0.0/16" not in prefixes:
                raise LabError("同名VNetのアドレス空間が異なります。")
        subnets = self.names(["network", "vnet", "subnet", "list", "-g", RG, "--vnet-name", VNET])
        for name, prefix in SUBNETS.items():
            if name not in subnets:
                self.emit(f"サブネット {name} ({prefix}) を作成")
                self.az(["network", "vnet", "subnet", "create", "-g", RG, "--vnet-name", VNET,
                         "-n", name, "--address-prefix", prefix])
            elif subnets[name].get("addressPrefix") != prefix:
                raise LabError(f"{name} のアドレス範囲が異なります。")
        return "3つのサブネットを確認しました（Firewall / 管理 / VM）。"

    def ensure_firewall_extension(self):
        extensions = self.az(["extension", "list"], scoped=False)
        if not any(x.get("name") == "azure-firewall" for x in extensions):
            self.emit("Azure Firewall CLI拡張機能をインストールします（Azureリソースの料金は発生しません）。")
            self.az(["extension", "add", "--name", "azure-firewall", "--yes"], scoped=False)

    def prepare_policy(self):
        self.require_owned_group()
        self.ensure_firewall_extension()
        policies = self.names(["network", "firewall", "policy", "list", "-g", RG])
        if POLICY not in policies:
            self.emit("Firewall Policy Basic を作成")
            self.az(["network", "firewall", "policy", "create", "-g", RG, "-n", POLICY, "-l", LOCATION, "--sku", "Basic"])
        policy = self.az(["network", "firewall", "policy", "show", "-g", RG, "-n", POLICY])
        if (policy.get("sku") or {}).get("tier") != "Basic":
            raise LabError("Policy のSKUが Basic ではありません。")
        return "Firewall Policy Basic を確認しました（まだFirewall本体はありません）。"

    def create_firewall(self):
        self.require_owned_group()
        self.prepare_vnet()
        self.prepare_policy()
        for name in (PIP_DATA, PIP_MGMT):
            ips = self.names(["network", "public-ip", "list", "-g", RG])
            if name not in ips:
                self.emit(f"課金対象: Public IP {name} を作成")
                self.az(["network", "public-ip", "create", "-g", RG, "-n", name, "-l", LOCATION,
                         "--sku", "Standard", "--allocation-method", "Static"])
        firewalls = self.names(["network", "firewall", "list", "-g", RG])
        if FW not in firewalls:
            self.emit("課金対象: Azure Firewall Basic を作成（数分かかります）")
            self.az([
                "network", "firewall", "create", "-g", RG, "-n", FW, "-l", LOCATION,
                "--sku", "AZFW_VNet", "--tier", "Basic", "--vnet-name", VNET,
                "--conf-name", "fw-ipconfig", "--public-ip", PIP_DATA,
                "--m-conf-name", "fw-mgmtconfig", "--m-public-ip", PIP_MGMT,
                "--firewall-policy", POLICY,
            ])
        fw = self.az(["network", "firewall", "show", "-g", RG, "-n", FW])
        if (fw.get("sku") or {}).get("tier") != "Basic":
            raise LabError("Firewall SKUがBasicではありません。")
        if not fw.get("ipConfigurations"):
            raise LabError("FirewallのIP構成がまだ確立されていません。時間を置いて再確認してください。")
        return "Azure Firewall Basicと2つのPublic IPを確認しました。"

    def create_vm(self):
        self.require_owned_group()
        self.prepare_vnet()
        nics = self.names(["network", "nic", "list", "-g", RG])
        if NIC not in nics:
            self.emit("VM用NICを作成（パブリックIPなし）")
            self.az(["network", "nic", "create", "-g", RG, "-n", NIC, "-l", LOCATION,
                     "--vnet-name", VNET, "--subnet", "WorkloadSubnet"])
        vms = self.names(["vm", "list", "-g", RG])
        if VM not in vms:
            self.emit("課金対象: Ubuntu VM Standard_B1s を作成")
            self.az(["vm", "create", "-g", RG, "-n", VM, "-l", LOCATION,
                     "--nics", NIC, "--image", "Ubuntu2204", "--size", "Standard_B1s",
                     "--storage-sku", "Standard_LRS", "--os-disk-name", DISK,
                     "--admin-username", "azureuser", "--generate-ssh-keys"])
        self.az(["vm", "show", "-g", RG, "-n", VM])
        return "Ubuntu VM（パブリックIPなし）を確認しました。"

    def create_route(self):
        self.require_owned_group()
        fw = self.az(["network", "firewall", "show", "-g", RG, "-n", FW])
        configurations = fw.get("ipConfigurations") or []
        if not configurations or not configurations[0].get("privateIPAddress"):
            raise LabError("FirewallプライベートIPを取得できません。Firewallの準備を確認してください。")
        ip = configurations[0]["privateIPAddress"]
        tables = self.names(["network", "route-table", "list", "-g", RG])
        if ROUTE_TABLE not in tables:
            self.az(["network", "route-table", "create", "-g", RG, "-n", ROUTE_TABLE, "-l", LOCATION])
        routes = self.names(["network", "route-table", "route", "list", "-g", RG, "--route-table-name", ROUTE_TABLE])
        if "default-via-firewall" not in routes:
            self.az(["network", "route-table", "route", "create", "-g", RG, "--route-table-name", ROUTE_TABLE,
                     "-n", "default-via-firewall", "--address-prefix", "0.0.0.0/0",
                     "--next-hop-type", "VirtualAppliance", "--next-hop-ip-address", ip])
        else:
            route = routes["default-via-firewall"]
            if route.get("nextHopIpAddress") != ip or route.get("addressPrefix") != "0.0.0.0/0":
                raise LabError("既存UDRとFirewall IPが一致しません。")
        subnet = self.az(["network", "vnet", "subnet", "show", "-g", RG, "--vnet-name", VNET, "-n", "WorkloadSubnet"])
        table_id = self.az(["network", "route-table", "show", "-g", RG, "-n", ROUTE_TABLE])["id"]
        if (subnet.get("routeTable") or {}).get("id", "").lower() != table_id.lower():
            self.az(["network", "vnet", "subnet", "update", "-g", RG, "--vnet-name", VNET,
                     "-n", "WorkloadSubnet", "--route-table", ROUTE_TABLE])
        return f"0.0.0.0/0 → Firewall {ip} に転送するUDRを適用しました。"

    def test_http(self):
        self.require_owned_group()
        script = (
            "for host in www.google.com www.microsoft.com; do "
            "code=$(curl -I -sS -o /dev/null -w '%{http_code}' --connect-timeout 10 --max-time 20 https://$host); "
            "rc=$?; echo RESULT host=$host exit=$rc http=$code; done"
        )
        self.emit("VM内でcurlを実行（Run Command）。ネットワークの反映には時間がかかる場合があります。")
        result = self.az(["vm", "run-command", "invoke", "-g", RG, "-n", VM,
                          "--command-id", "RunShellScript", "--scripts", script], timeout=700)
        messages = result.get("value") or []
        joined = "\n".join(m.get("message", "") for m in messages)
        self.emit(joined[-3500:] or "結果が空です。Run Commandの状態を確認してください。")
        if "RESULT host=" not in joined:
            raise LabError("curlの結果が読み取れません。VMエージェントやネットワークを確認してください。")
        return joined[-3500:]

    def allow_google(self):
        self.require_owned_group()
        groups = self.names(["network", "firewall", "policy", "rule-collection-group", "list",
                             "-g", RG, "--policy-name", POLICY])
        if RCG not in groups:
            self.emit("Rule Collection Group を作成")
            self.az(["network", "firewall", "policy", "rule-collection-group", "create",
                     "-g", RG, "--policy-name", POLICY, "-n", RCG, "--priority", "200"])
        group = self.az(["network", "firewall", "policy", "rule-collection-group", "show",
                         "-g", RG, "--policy-name", POLICY, "-n", RCG])
        collection_names = [item.get("name") for item in group.get("ruleCollections", [])]
        if "allow-google" not in collection_names:
            self.emit("GoogleへのHTTPSだけを許可するApplication Ruleを作成")
            self.az(["network", "firewall", "policy", "rule-collection-group", "collection",
                     "add-filter-collection", "-g", RG, "--policy-name", POLICY,
                     "--rule-collection-group-name", RCG, "--name", "allow-google",
                     "--collection-priority", "100", "--action", "Allow",
                     "--rule-name", "google-https", "--rule-type", "ApplicationRule",
                     "--source-addresses", "10.0.2.0/24",
                     "--protocols", "Https=443", "--target-fqdns", "www.google.com"])
        group = self.az(["network", "firewall", "policy", "rule-collection-group", "show",
                         "-g", RG, "--policy-name", POLICY, "-n", RCG])
        if "allow-google" not in [item.get("name") for item in group.get("ruleCollections", [])]:
            raise LabError("Rule Collectionが確認できません。")
        return "www.google.com:443の許可ルールを確認しました。"

    def cleanup(self):
        self.require_owned_group()
        resources = self.resources()
        def known_resource(resource):
            name = resource.get("name", "")
            typ = resource.get("type", "").lower()
            if RESOURCE_TYPES.get(name) == typ:
                return True
            # VM Run Command may create a nested extension resource.
            return (typ in {
                "microsoft.compute/virtualmachines/extensions",
                "microsoft.compute/virtualmachines/runcommands",
            } and name.startswith(VM + "/"))
        unexpected = [
            f"{r.get('name')} ({r.get('type')})"
            for r in resources if not known_resource(r)
        ]
        if unexpected:
            raise LabError("教材外の可能性があるリソースを検出したため削除を止めました: " + ", ".join(unexpected))
        self.emit(f"削除対象: {len(resources)} リソース")
        self.az(["group", "delete", "-n", RG, "--yes"], timeout=1200)
        if self.group_exists():
            raise LabError("削除後もリソースグループが存在します。処理状況を確認してください。")
        return "学習用リソースグループを削除し、Azure側で不存在を確認しました。"

    def run_named(self, name: str):
        actions = {
            "group": self.prepare_group, "vnet": self.prepare_vnet, "policy": self.prepare_policy,
            "firewall": self.create_firewall, "vm": self.create_vm, "route": self.create_route,
            "deny_test": self.test_http, "allow": self.allow_google, "allow_test": self.test_http,
            "status": self.status, "cleanup": self.cleanup,
        }
        if name not in actions:
            raise LabError("許可されていない操作です。")
        with self.lock:
            self.emit(f"操作開始: {name}")
            outcome = actions[name]()
            self.emit("操作完了: " + name)
            return outcome
