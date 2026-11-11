"""Small RDC-local Azure CLI runtime adapter.

On some Alpine containers the resolver returns AAAA records even without an IPv6
default route. A local, ignored sitecustomize may force urllib3 to IPv4.
No DNS/IP hardcoding, system routing changes, or persistent network exposure.
"""
from __future__ import annotations
import os
from pathlib import Path


def azure_cli_env() -> dict[str, str]:
    env = os.environ.copy()
    local = Path(__file__).resolve().parent / ".state" / "ipv4only"
    if (local / "sitecustomize.py").is_file():
        old = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = str(local) + (os.pathsep + old if old else "")
    return env