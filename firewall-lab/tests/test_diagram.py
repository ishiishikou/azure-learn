"""Editable draw.io file and notebook diagram asset validation."""
from pathlib import Path
from xml.etree import ElementTree as ET
import struct

import nbformat


ROOT = Path(__file__).resolve().parents[1]
DRAWIO = ROOT / "diagrams" / "azure-firewall-basic.drawio"
PNG = ROOT / "diagrams" / "azure-firewall-basic.png"


def cell_map():
    r = ET.parse(DRAWIO).getroot()
    assert r.tag == "mxfile"
    model = r.find(".//mxGraphModel")
    assert model is not None
    return {c.get("id"): c for c in model.findall(".//mxCell")}


def test_native_drawio_editable_and_hierarchical():
    cells = cell_map()
    assert len(cells) > 60
    assert cells["rg"].get("parent") == "subscription"
    assert cells["vnet"].get("parent") == "rg"
    assert cells["azfw_subnet"].get("parent") == "vnet"
    assert cells["mgmt_subnet"].get("parent") == "vnet"
    assert cells["workload_subnet"].get("parent") == "vnet"
    assert cells["fw_node"].get("parent") == "azfw_subnet"
    assert cells["vm_node"].get("parent") == "workload_subnet"
    assert cells["policy_node"].get("parent") == "rg"
    assert cells["pip_data"].get("parent") == "rg"
    assert cells["route_node"].get("parent") == "rg"
    assert cells["vm"].get("parent") == "vm_node"
    assert cells["vm_node"].get("vertex") == "1"
    assert "Public IPなし" in cells["vm_private"].get("value")
    assert "Private IPあり" in cells["vm_private"].get("value")


def test_arrows_are_attached_and_blocked_flow_stops_at_firewall():
    c = cell_map()
    for id in ("fw_green", "fw_red", "vm_outbound", "route_to_workload", "pip_connect", "mgmt_connect"):
        assert c[id].get("source") in c
        assert c[id].get("target") in c
    assert c["fw_green"].get("source") == "fw_node"
    assert c["fw_green"].get("target") == "target_google"
    assert c["fw_red"].get("source") == "fw_node"
    assert c["fw_red"].get("target") == "fw_block_marker"
    assert c["fw_red"].get("target") != "target_ms"
    assert "転送されない" in c["no_forward"].get("value")


def test_actual_png_export_and_notebook_reference():
    raw = PNG.read_bytes()
    assert raw[:8] == b"\x89PNG\r\n\x1a\n"
    width, height = struct.unpack(">II", raw[16:24])
    assert width >= 2000 and height >= 1300
    notebook = nbformat.read(ROOT / "firewall_hands_on.ipynb", as_version=4)
    nbformat.validate(notebook)
    image_markdown = notebook.cells[1].source
    assert "diagrams/azure-firewall-basic.png" in image_markdown
    assert "diagrams/azure-firewall-basic.drawio" in image_markdown