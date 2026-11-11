"""Official draw.io-skill based architecture-diagram checks."""
from pathlib import Path
from xml.etree import ElementTree as ET
import struct

import nbformat

ROOT = Path(__file__).resolve().parents[1]
DRAWIO = ROOT / "diagrams" / "azure-firewall-basic.drawio"
PNG = ROOT / "diagrams" / "azure-firewall-basic.png"

def cells():
    tree = ET.parse(DRAWIO)
    mxfile = tree.getroot()
    assert mxfile.tag == "mxfile"
    assert mxfile.find(".//mxGraphModel") is not None
    return {c.attrib["id"]: c for c in mxfile.findall(".//mxCell")}

def bounds(c):
    g = c.find("mxGeometry")
    assert g is not None
    return tuple(float(g.attrib[k]) for k in ("x","y","width","height"))

def abs_pos(c_id, records):
    c=records[c_id]
    x,y,w,h=bounds(c)
    if c.get("parent") in records and c.get("parent") not in ("0","1"):
        px,py,_,_=abs_pos(c.get("parent"),records)
        return (px+x,py+y,w,h)
    return (x,y,w,h)

def test_native_drawio_and_nested_membership():
    c=cells()
    assert "0" in c and "1" in c
    assert len(c)>60
    assert c["rg"].get("parent")=="subscription"
    assert c["vnet"].get("parent")=="rg"
    for id in ("azfw_subnet","mgmt_subnet","workload_subnet"):
        assert c[id].get("parent")=="vnet"
    assert c["fw_node"].get("parent")=="azfw_subnet"
    assert c["vm_node"].get("parent")=="workload_subnet"
    for id in ("policy_node","route_node","pip_node"):
        assert c[id].get("parent")=="rg"
    assert "Private IPあり" in c["vm_private"].get("value")
    assert "Public IPなし" in c["vm_private"].get("value")
    assert "構築予定" in c["status_chip"].get("value")

def test_connections_only_represent_real_network_traffic():
    c=cells()
    edges={k:v for k,v in c.items() if v.get("edge")=="1"}
    assert set(edges)=={"vm_outbound","fw_green","fw_red"}
    assert (c["vm_outbound"].get("source"),c["vm_outbound"].get("target"))==("vm_node","fw_node")
    assert (c["fw_green"].get("source"),c["fw_green"].get("target"))==("fw_node","target_google")
    assert (c["fw_red"].get("source"),c["fw_red"].get("target"))==("fw_node","fw_block_marker")
    for edge in edges.values():
        assert edge.get("source") in c and edge.get("target") in c
        assert "edgeStyle=orthogonalEdgeStyle" in edge.get("style","")
        assert edge.find("mxGeometry") is not None
        assert edge.find(".//Array") is None  # no manual waypoints
    assert "転送されません" in c["no_forward"].get("value")

def test_geometry_safe_margins_and_single_row_data_path():
    c=cells()
    for key,item in c.items():
        if item.get("vertex")!="1":
            continue
        x,y,w,h=bounds(item)
        assert w>0 and h>0, key
        parent=item.get("parent")
        if parent not in c or c[parent].get("vertex")!="1":
            continue
        _,_,pw,ph=bounds(c[parent])
        assert x>=-1 and y>=-1, f"{key} left/top escapes {parent}"
        assert x+w<=pw+1.0, f"{key} right escapes {parent}"
        assert y+h<=ph+1.0, f"{key} bottom escapes {parent}"
    vm=abs_pos("vm_node",c)
    fw=abs_pos("fw_node",c)
    google=abs_pos("target_google",c)
    assert vm[0]+vm[2]<fw[0]<google[0]
    assert abs(vm[1]+vm[3]/2-(fw[1]+fw[3]/2))<2
    assert abs(fw[1]+fw[3]/2-(google[1]+google[3]/2))<2
    workload=abs_pos("workload_subnet",c)
    firewall_subnet=abs_pos("azfw_subnet",c)
    mgmt=abs_pos("mgmt_subnet",c)
    assert workload[0]+workload[2]<firewall_subnet[0]
    assert mgmt[0]>firewall_subnet[0]+firewall_subnet[2]

def test_png_dimensions_and_notebook_reference():
    data=PNG.read_bytes()
    assert data[:8]==b"\x89PNG\r\n\x1a\n"
    width,height=struct.unpack(">II",data[16:24])
    assert width>=2000 and height>=1250
    book=nbformat.read(ROOT/"firewall_hands_on.ipynb",as_version=4)
    nbformat.validate(book)
    assert "diagrams/azure-firewall-basic.png" in book.cells[1].source
    assert "diagrams/azure-firewall-basic.drawio" in book.cells[1].source

def test_png_has_embedded_diagram_metadata():
    # draw.io's editable PNG uses a tEXt chunk with keyword mxfile,
    # containing encodeURIComponent(<mxfile>), before the first IDAT.
    import urllib.parse
    data=PNG.read_bytes()
    pos=8
    found=False
    while pos+12<=len(data):
        length=struct.unpack(">I",data[pos:pos+4])[0]
        typ=data[pos+4:pos+8]
        chunk=data[pos+8:pos+8+length]
        pos+=12+length
        if typ==b"tEXt":
            key,sep,payload=chunk.partition(b"\0")
            if key==b"mxfile":
                decoded=urllib.parse.unquote(payload.decode("latin-1"))
                root=ET.fromstring(decoded)
                assert root.tag=="mxfile"
                assert root.find(".//mxGraphModel/root/mxCell[@id='0']") is not None
                assert root.find(".//mxGraphModel/root/mxCell[@id='1']") is not None
                found=True
                break
        if typ==b"IDAT": break
    assert found, "Draw.io編集用mxfile XMLがPNG内に含まれません"