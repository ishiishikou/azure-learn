"""Failure-path tests requested by the independent reviewer."""
import json
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lab import AzureLab, CLIResult, LabError
from verification import ValidationError, curl_results, route, effective_route
from test_lab import FakeAzureCLI


def test_malformed_group_existence_response_fails_closed():
    f = FakeAzureCLI()
    def bad(argv):
        if argv[1:3] == ["group", "exists"]:
            return CLIResult(argv, json.dumps("false"), "", 0)
        return f(argv)
    lab = AzureLab("sub-test", executor=bad)
    with pytest.raises(ValidationError, match="true/false"):
        lab.group_exists()


def test_invalid_resource_list_prevents_cleanup():
    f = FakeAzureCLI()
    f.group = f.tagged = True
    def bad(argv):
        if argv[1:3] == ["resource", "list"]:
            return CLIResult(argv, json.dumps({"unexpected": "object"}), "", 0)
        return f(argv)
    lab = AzureLab("sub-test", executor=bad)
    with pytest.raises(ValidationError, match="リソース一覧"):
        lab.cleanup()
    assert f.group


def test_incorrect_udr_next_hop_rejected():
    with pytest.raises(ValidationError, match="Firewall"):
        route({"addressPrefix": "0.0.0.0/0", "nextHopType": "Internet",
               "nextHopIpAddress": "10.0.0.4"}, "10.0.0.4")


def test_effective_route_missing_rejected():
    with pytest.raises(ValidationError, match="有効経路"):
        effective_route({"value": [{"addressPrefix": ["0.0.0.0/0"],
                                   "nextHopType": "Internet", "state": "Active"}]}, "10.0.0.4")


@pytest.mark.parametrize("message,allowed", [
    ("RESULT host=www.google.com dns=fail exit=6 http=000\nRESULT host=www.microsoft.com dns=ok exit=28 http=000", False),
    ("RESULT host=www.google.com dns=ok exit=0 http=200\nRESULT host=www.microsoft.com dns=ok exit=28 http=000", False),
    ("RESULT host=www.google.com dns=ok exit=28 http=000\nRESULT host=www.microsoft.com dns=ok exit=28 http=000", True),
    ("RESULT host=www.google.com dns=ok exit=0 http=200", True),
])
def test_curl_probes_fail_for_wrong_or_missing_observation(message, allowed):
    with pytest.raises(ValidationError):
        curl_results(message, allow=allowed)


def test_corrupted_az_json_fails_closed():
    f = FakeAzureCLI()
    f.group = True
    f.tagged = True
    def bad(argv):
        if argv[1:3] == ["group", "exists"]:
            return CLIResult(argv, "not valid json", "", 0)
        return f(argv)
    lab = AzureLab("sub-test", executor=bad)
    with pytest.raises(ValidationError):
        lab.group_exists()