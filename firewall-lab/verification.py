"""Strict validation of Azure states and network observations.

This module must fail closed on malformed/incomplete API responses.
"""
from __future__ import annotations

import ipaddress
import re
from typing import Any


class ValidationError(ValueError):
    """An Azure response did not prove the expected state."""


def obj(value: Any, what: str) -> dict:
    if not isinstance(value, dict):
        raise ValidationError(f"{what}: Azureから不正な形式の応答を受け取りました。")
    return value


def arr(value: Any, what: str) -> list:
    if not isinstance(value, list) or any(not isinstance(x, dict) for x in value):
        raise ValidationError(f"{what}: Azureから不正な一覧応答を受け取りました。")
    return value


def group_exists(value: Any) -> bool:
    if type(value) is not bool:
        raise ValidationError("リソースグループの存在応答がtrue/falseではありません。")
    return value


def azure_ref(value: Any, suffix: str, what: str):
    ref = obj(value, what)
    rid = ref.get("id")
    if not isinstance(rid, str) or not rid.lower().endswith(suffix.lower()):
        raise ValidationError(f"{what}: 紐付けられたAzureリソースが想定と違います。")


def firewall(fw: Any, policy_id: str, public_ips: tuple[str, str]):
    data = obj(fw, "Firewall")
    sku = obj(data.get("sku"), "Firewall SKU")
    if sku.get("tier") != "Basic" or sku.get("name") != "AZFW_VNet":
        raise ValidationError("Firewall SKUがBasic/AZFW_VNetではありません。")
    if data.get("provisioningState") != "Succeeded":
        raise ValidationError("Firewallのプロビジョニングが完了していません。")
    linked = obj(data.get("firewallPolicy"), "Firewall Policy")
    if str(linked.get("id", "")).lower() != policy_id.lower():
        raise ValidationError("FirewallとPolicyの関連付けが違います。")
    conf = arr(data.get("ipConfigurations"), "Firewall IP構成")
    if len(conf) != 1 or not conf[0].get("privateIPAddress"):
        raise ValidationError("FirewallのプライベートIPが確定していません。")
    ipaddress.ip_address(conf[0]["privateIPAddress"])
    azure_ref(conf[0].get("publicIPAddress"), "/publicIPAddresses/" + public_ips[0], "Firewall通信用Public IP")
    management = obj(data.get("managementIpConfiguration"), "Firewall管理IP構成")
    azure_ref(management.get("publicIPAddress"), "/publicIPAddresses/" + public_ips[1], "Firewall管理Public IP")
    return conf[0]["privateIPAddress"]


def nic(nic_data: Any, name: str, subnet: str):
    data = obj(nic_data, "VM NIC")
    configs = arr(data.get("ipConfigurations"), "NIC IP構成")
    if len(configs) != 1:
        raise ValidationError("NICに予期しないIP構成が含まれます。")
    ip_config = configs[0]
    azure_ref(ip_config.get("subnet"), "/subnets/" + subnet, "NIC接続サブネット")
    if ip_config.get("publicIPAddress"):
        raise ValidationError("NICにPublic IPが関連付いています。")
    if data.get("name") != name:
        raise ValidationError("VM NICの名前が違います。")


def vm(data: Any, name: str, expected_nic: str):
    data = obj(data, "VM")
    if data.get("name") != name:
        raise ValidationError("VMの名前が一致しません。")
    if obj(data.get("hardwareProfile"), "VMハードウェア").get("vmSize") != "Standard_B1s":
        raise ValidationError("VMサイズが想定と違います。")
    iface = arr(obj(data.get("networkProfile"), "VMネットワーク").get("networkInterfaces"), "VM NIC")
    if len(iface) != 1:
        raise ValidationError("VMに想定外のNICが接続されています。")
    azure_ref(iface[0], "/networkInterfaces/" + expected_nic, "VM NIC")
    if data.get("provisioningState") != "Succeeded":
        raise ValidationError("VM作成が完了していません。")


def route(data: Any, target_ip: str):
    data = obj(data, "UDR")
    if (data.get("addressPrefix"), data.get("nextHopType"), data.get("nextHopIpAddress")) != (
        "0.0.0.0/0", "VirtualAppliance", target_ip
    ):
        raise ValidationError("UDRがFirewallへの既定経路ではありません。")


def effective_route(data: Any, target_ip: str):
    if isinstance(data, dict):
        routes = arr(data.get("value"), "有効経路")
    else:
        routes = arr(data, "有効経路")
    for r in routes:
        prefixes = r.get("addressPrefix")
        if isinstance(prefixes, str):
            prefixes = [prefixes]
        if not isinstance(prefixes, list):
            continue
        next_hops = r.get("nextHopIpAddress")
        if isinstance(next_hops, str):
            next_hops = [next_hops]
        if (
            "0.0.0.0/0" in prefixes and r.get("nextHopType") == "VirtualAppliance"
            and isinstance(next_hops, list) and next_hops == [target_ip]
            and r.get("state", "Active") == "Active"
        ):
            return r
    raise ValidationError("NICの有効経路にFirewallへのActiveな0.0.0.0/0が見つかりません。")


def policy_collection(group: Any, *, allow: bool):
    data = obj(group, "Rule Collection Group")
    collections = arr(data.get("ruleCollections"), "Rule Collections")
    if not allow:
        if collections:
            raise ValidationError("ルールなしの想定ですが、Rule Collectionがすでにあります。")
        return
    if len(collections) != 1:
        raise ValidationError("ルール数が想定外です。")
    collection = collections[0]
    if collection.get("name") != "allow-google" or obj(collection.get("action"), "Action").get("type") != "Allow":
        raise ValidationError("Google許可ルールのコレクションが期待と違います。")
    rules = arr(collection.get("rules"), "Application Rules")
    if len(rules) != 1:
        raise ValidationError("許可ルールが1件ではありません。")
    rule = rules[0]
    if rule.get("ruleType") != "ApplicationRule" or rule.get("name") != "google-https":
        raise ValidationError("アプリケーションルールの種類・名前が違います。")
    if rule.get("sourceAddresses") != ["10.0.2.0/24"] or rule.get("targetFqdns") != ["www.google.com"]:
        raise ValidationError("許可する送信元/宛先が想定と違います。")
    protocols = arr(rule.get("protocols"), "HTTPSプロトコル")
    if len(protocols) != 1 or str(protocols[0].get("protocolType")).lower() != "https" or int(protocols[0].get("port", 0)) != 443:
        raise ValidationError("許可するプロトコルまたはポートが想定と違います。")


_RESULT = re.compile(r"^RESULT host=(www\.(?:google|microsoft)\.com) dns=(ok|fail) exit=(\d+) http=(\d{3})$")


def curl_results(message: str, *, allow: bool) -> dict:
    found = {}
    for line in message.splitlines():
        line = line.strip()
        if "RESULT host=" not in line:
            continue
        match = _RESULT.fullmatch(line)
        if not match:
            raise ValidationError("curl結果の形式が想定外です: " + line[:120])
        name, dns, exit_code, http = match.groups()
        if name in found:
            raise ValidationError("同じホストのcurl結果が複数あります。")
        found[name] = (dns, int(exit_code), int(http))
    hosts = {"www.google.com", "www.microsoft.com"}
    if set(found) != hosts:
        raise ValidationError("2つの対象ホストのcurl結果が揃っていません。")
    if any(dns != "ok" for dns, _, _ in found.values()):
        raise ValidationError("DNS名前解決に失敗したためFirewallによる拒否とは判定できません。")
    google = found["www.google.com"]
    microsoft = found["www.microsoft.com"]
    def connected(result):
        # Any HTTP response means the remote side was reached,
        # even when the remote server returns 403/404/500.
        return result[1] == 0 and 100 <= result[2] <= 599
    def blocked_candidate(result):
        # Only non-HTTP connection failures are plausible blocking observations.
        # This still does not prove the Firewall caused the failure: verify logs.
        return result[2] == 0 and result[1] in (7, 28)
    if allow:
        if not connected(google) or not blocked_candidate(microsoft):
            raise ValidationError("Google HTTPS接続 / Microsoft非HTTP応答の期待観測と一致しません。TLS・接続・FWログを確認してください。")
    else:
        if not blocked_candidate(google) or not blocked_candidate(microsoft):
            raise ValidationError("ルールなしの非HTTP応答と一致しません。サーバー応答やTLSエラーをFirewall拒否として扱いません。")
    return found