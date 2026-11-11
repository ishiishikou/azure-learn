"""Offline end-to-end tests. No calls reach Azure."""
import json
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lab import AzureLab, CLIResult, LabError, RG, TAG_KEY, TAG_VALUE, POLICY, FW, VNET, NIC, VM, DISK


class FakeAzureCLI:
    def __init__(self):
        self.group = False
        self.tagged = False
        self.resources = {}
        self.vnet = False
        self.subnets = {}
        self.policy = False
        self.firewall = False
        self.public_ips = set()
        self.nic = False
        self.vm = False
        self.table = False
        self.routes = {}
        self.route_attached = False
        self.rule_group = False
        self.allowed = False
        self.calls = []

    def __call__(self, argv):
        self.calls.append(argv)
        tokens = argv[1:]
        if "--subscription" in tokens:
            tokens = tokens[:tokens.index("--subscription")]
        if "--only-show-errors" in tokens:
            tokens = tokens[:tokens.index("--only-show-errors")]
        cmd = tokens[:]
        def opt(name, default=""):
            return cmd[cmd.index(name) + 1] if name in cmd else default
        def res(value):
            return CLIResult(argv, json.dumps(value, ensure_ascii=False), "", 0)
        def add(name, kind):
            self.resources[name] = {"name": name, "type": kind}
        if cmd[:2] == ["account", "list"]:
            return res([{"id": "sub-test", "name": "Study", "state": "Enabled"}])
        if cmd[:2] == ["account", "show"]:
            return res({"id": "sub-test", "name": "Study"})
        if cmd[:2] == ["extension", "list"]:
            return res([{"name": "azure-firewall"}])
        if cmd[:2] == ["extension", "add"]:
            return res({"name": "azure-firewall"})
        if cmd[:2] == ["group", "exists"]:
            return res(self.group)
        if cmd[:2] == ["group", "show"]:
            return res({"tags": {TAG_KEY: TAG_VALUE} if self.tagged else {}, "name": RG})
        if cmd[:2] == ["group", "create"]:
            self.group = self.tagged = True
            return res({"name": RG})
        if cmd[:2] == ["group", "update"]:
            self.tagged = True
            return res({"name": RG})
        if cmd[:2] == ["group", "delete"]:
            self.group = False
            self.resources.clear()
            return res(None)
        if cmd[:2] == ["resource", "list"]:
            return res(list(self.resources.values()))
        if cmd[:3] == ["network", "vnet", "list"]:
            return res([{"name": VNET, "addressSpace": {"addressPrefixes": ["10.0.0.0/16"]}}] if self.vnet else [])
        if cmd[:3] == ["network", "vnet", "create"]:
            self.vnet = True
            add(VNET, "Microsoft.Network/virtualNetworks")
            self.subnets["AzureFirewallSubnet"] = "10.0.0.0/26"
            return res({"newVNet": {"name": VNET}})
        if cmd[:4] == ["network", "vnet", "subnet", "list"]:
            return res([{"name": n, "addressPrefix": p} for n,p in self.subnets.items()])
        if cmd[:4] == ["network", "vnet", "subnet", "create"]:
            self.subnets[opt("-n")] = opt("--address-prefix")
            return res({"name": opt("-n")})
        if cmd[:4] == ["network", "vnet", "subnet", "show"]:
            return res({"routeTable": {"id": "/rt/lab"} if self.route_attached else None})
        if cmd[:4] == ["network", "vnet", "subnet", "update"]:
            self.route_attached = True
            return res({"name": "WorkloadSubnet"})
        if cmd[:4] == ["network", "firewall", "policy", "list"]:
            return res([{"name": POLICY}] if self.policy else [])
        if cmd[:4] == ["network", "firewall", "policy", "create"]:
            self.policy = True
            add(POLICY, "Microsoft.Network/firewallPolicies")
            return res({"sku": {"tier": "Basic"}})
        if cmd[:4] == ["network", "firewall", "policy", "show"]:
            return res({"sku": {"tier": "Basic"}, "id": "/policies/lab"})
        if cmd[:3] == ["network", "public-ip", "list"]:
            return res([{"name": n} for n in self.public_ips])
        if cmd[:3] == ["network", "public-ip", "create"]:
            name = opt("-n")
            self.public_ips.add(name)
            add(name, "Microsoft.Network/publicIPAddresses")
            return res({"name": name})
        if cmd[:3] == ["network", "public-ip", "show"]:
            return res({"name": opt("-n"), "sku": {"name": "Standard"},
                        "publicIPAllocationMethod": "Static"})
        if cmd[:3] == ["network", "firewall", "list"]:
            return res([{"name": FW}] if self.firewall else [])
        if cmd[:3] == ["network", "firewall", "create"]:
            self.firewall = True
            add(FW, "Microsoft.Network/azureFirewalls")
            return res({"name": FW})
        if cmd[:3] == ["network", "firewall", "show"]:
            return res({"sku": {"tier": "Basic", "name": "AZFW_VNet"},
                        "provisioningState": "Succeeded",
                        "firewallPolicy": {"id": "/policies/lab"},
                        "ipConfigurations": [{
                            "privateIPAddress": "10.0.0.4",
                            "publicIPAddress": {"id": "/publicIPAddresses/pip-firewall-lab"}}],
                        "managementIpConfiguration": {
                            "publicIPAddress": {"id": "/publicIPAddresses/pip-firewall-mgmt-lab"}}})
        if cmd[:3] == ["network", "nic", "list"]:
            return res([{"name": NIC}] if self.nic else [])
        if cmd[:3] == ["network", "nic", "create"]:
            self.nic = True
            add(NIC, "Microsoft.Network/networkInterfaces")
            return res({"name": NIC})
        if cmd[:3] == ["network", "nic", "show"]:
            return res({"name": NIC, "ipConfigurations": [{
                "name": "ipconfig1", "subnet": {"id": "/subnets/WorkloadSubnet"},
                "publicIPAddress": None
            }]})
        if cmd[:3] == ["network", "nic", "show-effective-route-table"]:
            return res({"value": [{
                "addressPrefix": ["0.0.0.0/0"], "nextHopType": "VirtualAppliance",
                "nextHopIpAddress": ["10.0.0.4"], "state": "Active"}]})
        if cmd[:2] == ["vm", "list"]:
            return res([{"name": VM}] if self.vm else [])
        if cmd[:2] == ["vm", "create"]:
            self.vm = True
            add(VM, "Microsoft.Compute/virtualMachines")
            add(DISK, "Microsoft.Compute/disks")
            return res({"name": VM})
        if cmd[:2] == ["vm", "show"]:
            return res({"name": VM, "provisioningState": "Succeeded",
                        "hardwareProfile": {"vmSize": "Standard_B1s"},
                        "networkProfile": {"networkInterfaces": [{"id": "/networkInterfaces/nic-firewall-lab"}]}})
        if cmd[:3] == ["network", "route-table", "list"]:
            return res([{"name": "rt-firewall-lab"}] if self.table else [])
        if cmd[:3] == ["network", "route-table", "create"]:
            self.table = True
            add("rt-firewall-lab", "Microsoft.Network/routeTables")
            return res({"name": "rt-firewall-lab"})
        if cmd[:3] == ["network", "route-table", "show"]:
            return res({"id": "/rt/lab"})
        if cmd[:4] == ["network", "route-table", "route", "list"]:
            return res(list(self.routes.values()))
        if cmd[:4] == ["network", "route-table", "route", "create"]:
            self.routes["default-via-firewall"] = {
                "name": "default-via-firewall", "nextHopIpAddress": "10.0.0.4",
                "nextHopType": "VirtualAppliance", "addressPrefix": "0.0.0.0/0"}
            return res(self.routes["default-via-firewall"])
        if cmd[:4] == ["network", "route-table", "route", "show"]:
            return res(self.routes["default-via-firewall"])
        if cmd[:5] == ["network", "firewall", "policy", "rule-collection-group", "list"]:
            return res([{"name": "rcg-web-lab"}] if self.rule_group else [])
        if cmd[:5] == ["network", "firewall", "policy", "rule-collection-group", "create"]:
            self.rule_group = True
            return res({"name": "rcg-web-lab"})
        if cmd[:5] == ["network", "firewall", "policy", "rule-collection-group", "show"]:
            return res({"ruleCollections": [{
                "name": "allow-google", "action": {"type": "Allow"},
                "rules": [{"ruleType": "ApplicationRule", "name": "google-https",
                           "sourceAddresses": ["10.0.2.0/24"],
                           "targetFqdns": ["www.google.com"],
                           "protocols": [{"protocolType": "Https", "port": 443}]}]
            }] if self.allowed else []})
        if cmd[:5] == ["network", "firewall", "policy", "rule-collection-group", "collection"]:
            self.allowed = True
            return res({"name": "allow-google"})
        if cmd[:3] == ["vm", "run-command", "invoke"]:
            google = "exit=0 http=200" if self.allowed else "exit=28 http=000"
            return res({"value": [{"message": "RESULT host=www.google.com dns=ok " + google
                                               + "\nRESULT host=www.microsoft.com dns=ok exit=28 http=000"}]})
        raise AssertionError("Unknown mock command: " + " ".join(cmd))


def test_full_lifecycle_and_repeatable():
    fake = FakeAzureCLI()
    lab = AzureLab("sub-test", executor=fake)
    assert "なし" in lab.status()
    for step in ("group", "vnet", "policy", "firewall", "vm", "route", "deny_test", "allow", "allow_test"):
        message = lab.run_named(step)
        assert message
    assert fake.tagged and fake.vm and fake.firewall and fake.route_attached and fake.allowed
    assert fake.routes["default-via-firewall"]["nextHopIpAddress"] == "10.0.0.4"
    assert "exit=0 http=200" in lab.run_named("allow_test")
    prev = len([x for x in fake.calls if x[1:4] == ["network", "firewall", "create"]])
    lab.run_named("firewall")
    assert len([x for x in fake.calls if x[1:4] == ["network", "firewall", "create"]]) == prev
    assert "不存在" in lab.run_named("cleanup")
    assert not fake.group


def test_unknown_resources_prevent_cleanup():
    fake = FakeAzureCLI()
    lab = AzureLab("sub-test", executor=fake)
    lab.prepare_group()
    fake.resources["customer-resource"] = {"name": "customer-resource", "type": "Microsoft.Storage/storageAccounts"}
    with pytest.raises(LabError, match="教材外"):
        lab.cleanup()
    assert fake.group


def test_untagged_nonempty_group_rejected():
    fake = FakeAzureCLI()
    fake.group = True
    fake.resources["important"] = {"name": "important"}
    lab = AzureLab("sub-test", executor=fake)
    with pytest.raises(LabError, match="既存リソース"):
        lab.prepare_group()
    assert not fake.tagged


def test_subscription_is_required_for_scoped_commands():
    fake = FakeAzureCLI()
    lab = AzureLab(executor=fake)
    with pytest.raises(LabError, match="未選択"):
        lab.status()
    with pytest.raises(LabError, match="許可されていない"):
        lab.run_named("arbitrary")


def test_select_only_accessible_subscription():
    fake = FakeAzureCLI()
    lab = AzureLab(executor=fake)
    with pytest.raises(LabError, match="アクセスできません"):
        lab.choose("another")
    lab.choose("sub-test")
    assert lab.subscription == "sub-test"


def test_import_and_status_do_not_write():
    fake = FakeAzureCLI()
    lab = AzureLab("sub-test", executor=fake)
    lab.status()
    assert not any("create" in cmd or "delete" in cmd or "update" in cmd for args in fake.calls for cmd in args[:5])