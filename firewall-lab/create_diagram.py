"""Create a native, fully editable diagrams.net / draw.io network drawing."""
from __future__ import annotations
from pathlib import Path
from xml.etree import ElementTree as ET
from html import escape

OUTPUT = Path(__file__).resolve().parent / "diagrams"
OUTPUT.mkdir(parents=True, exist_ok=True)
OUT = OUTPUT / "azure-firewall-basic.drawio"

W, H = 1760, 990
COLORS = {
    "ink":"#17324C","muted":"#53687E","azure":"#1373C8",
    "navy":"#164B82","lite":"#F0F7FE","sky":"#DFF0FF",
    "subnet":"#F7FBFF","stroke":"#9BBBD6",
    "green":"#138755","palegreen":"#E9F8EF","red":"#C83E47",
    "palered":"#FFF0F0","orange":"#C87718",
}

mxfile = ET.Element("mxfile", attrib={
    "host":"app.diagrams.net", "agent":"Azure Firewall learning drawio generator",
    "version":"25.0.2", "type":"device"
})
diagram = ET.SubElement(mxfile, "diagram", id="firewall-basic", name="Azure Firewall Basic")
model = ET.SubElement(diagram, "mxGraphModel", attrib={
    "dx":"1760", "dy":"990", "grid":"1", "gridSize":"10", "guides":"1",
    "tooltips":"1", "connect":"1", "arrows":"1", "fold":"1",
    "page":"1","pageScale":"1","pageWidth":str(W),"pageHeight":str(H),
    "math":"0","shadow":"0"
})
root=ET.SubElement(model, "root")
ET.SubElement(root, "mxCell", id="0")
ET.SubElement(root, "mxCell", id="1", parent="0")

def shape(id, value, x,y,w,h, *, fill="#FFFFFF", stroke="#9BBBD6", fg="#17324C",
          size=16, bold=False, round=True, align="left", valign="middle",
          dashed=False, stroke_width=1.5, family="Arial", extras=""):
    style = (
        "rounded="+("1" if round else "0")+";arcSize=12;"
        "whiteSpace=wrap;html=1;overflow=fill;shadow=0;"
        f"fillColor={fill};strokeColor={stroke};strokeWidth={stroke_width};"
        f"fontColor={fg};fontSize={size};fontStyle={1 if bold else 0};"
        f"fontFamily={family};align={align};verticalAlign={valign};"
        "spacingLeft=13;spacingRight=10;spacingTop=7;spacingBottom=7;"
        + ("dashed=1;dashPattern=6 4;" if dashed else "")+extras
    )
    c = ET.SubElement(root, "mxCell", id=id, value=value, style=style, vertex="1", parent="1")
    ET.SubElement(c,"mxGeometry",attrib={"x":str(x),"y":str(y),"width":str(w),"height":str(h),"as":"geometry"})
    return c

def text(id, value, x,y,w,h, *, size=16, fg="#17324C", bold=False,align="left",valign="middle"):
    return shape(id,value,x,y,w,h,fill="none",stroke="none",fg=fg,size=size,bold=bold,round=False,align=align,valign=valign,stroke_width=0,extras="pointerEvents=0;")

def edge(id,x1,y1,x2,y2, *, color="#1373C8",width=3,dashed=False, arrow=True, bends=()):
    style=(f"edgeStyle=none;rounded=0;html=1;strokeColor={color};strokeWidth={width};"
           f"endArrow={'block' if arrow else 'none'};endFill=1;"
           + ("dashed=1;dashPattern=8 5;" if dashed else ""))
    cell=ET.SubElement(root,"mxCell", id=id, value="", style=style, edge="1", parent="1")
    g=ET.SubElement(cell,"mxGeometry",relative="1", attrib={"as":"geometry"})
    ET.SubElement(g,"mxPoint",x=str(x1),y=str(y1),attrib={"as":"sourcePoint"})
    ET.SubElement(g,"mxPoint",x=str(x2),y=str(y2),attrib={"as":"targetPoint"})
    if bends:
        arr=ET.SubElement(g,"Array", attrib={"as":"points"})
        for x,y in bends: ET.SubElement(arr,"mxPoint",x=str(x),y=str(y))
    return cell

# Canvas and main hierarchy
shape("canvas","","0","0",W,H, fill="#FFFFFF",stroke="#FFFFFF",round=False)
shape("title_bg","",30,20,1700,80,fill="#134F88",stroke="#134F88",stroke_width=0)
text("title","Azure Firewall Basic　学習用ネットワーク構成図",66,28,1540,54,size=30,fg="#FFFFFF",bold=True)
text("planned","設計・学習用（実機へのデプロイは未検証）",1320,65,365,24,size=12,fg="#D5E7FA",align="right")
shape("subscription","",35,125,1300,800,fill="#F1F8FE",stroke="#4C92CA",stroke_width=2)
shape("sub_head","",47,138,1276,58,fill="#D9EDFF",stroke="#D9EDFF",stroke_width=0)
text("sub_title","AZURE サブスクリプション　|　Japan East",70,147,1040,39,size=23,fg="#173F65",bold=True)
shape("rg","",65,206,1240,693,fill="#FFFFFF",stroke="#669DCC",stroke_width=2)
shape("rg_head","",76,217,1218,54,fill="#E9F3FD",stroke="#E9F3FD",stroke_width=0)
text("rg_title","リソース グループ　 rg-firewall-lab",98,225,960,36,size=22,fg="#1B527F",bold=True)
shape("vnet","",95,288,868,550,fill="#FDFEFF",stroke="#6EA7DB",stroke_width=2)
shape("vnet_head","",107,302,844,53,fill="#DBEEFF",stroke="#DBEEFF",stroke_width=0)
text("vnet_label","仮想ネットワーク　 vnet-firewall-lab",126,310,610,33,size=19,fg="#1F547C",bold=True)
shape("vnet_cidr","10.0.0.0/16",741,310,180,33,fill="#FFFFFF",stroke="#BCD2E3",size=16,bold=True,align="center")

# Subnets, three separate containers
shape("azfw_subnet","",116,370,824,210,fill="#F4FAFF",stroke="#80B3DC",round=True)
shape("azfw_subnet_band","",125,379,806,42,fill="#DCEEFF",stroke="#DCEEFF",round=True,stroke_width=0)
text("azfw_subnet_title","AzureFirewallSubnet　10.0.0.0/26",146,385,745,29,size=18,bold=True)
shape("fw_node","",435,443,380,100,fill="#E6F2FE",stroke="#267DBD",stroke_width=2)
text("fw_icon","▦",460,454,64,65,size=43,fg="#E25C47",bold=True,align="center")
text("fw_name","Azure Firewall Basic",532,449,269,30,size=22,fg="#164976",bold=True)
text("fw_id","fw-firewall-lab",532,482,265,25,size=17,fg="#285470")
text("fw_private","プライベートIP：作成後に取得",532,511,264,23,size=13,fg="#537188")

shape("mgmt_subnet","",116,592,824,74,fill="#EFF6FC",stroke="#84B5D8")
text("mgmt_subnet_title","AzureFirewallManagementSubnet　10.0.1.0/26",137,601,760,31,size=18,bold=True)
text("mgmt_note","Firewall Basicの管理通信専用（通信用サブネットと分離）",144,630,730,23,size=13,fg="#53687E")

shape("workload_subnet","",116,678,824,144,fill="#EFF8FF",stroke="#84B5D8")
text("workload_title","WorkloadSubnet　10.0.2.0/24",137,685,750,28,size=18,bold=True)
shape("vm_node","",155,727,332,76,fill="#FFFFFF",stroke="#4C89C0",stroke_width=1.7)
text("vm","Ubuntu VM　vm-firewall-lab",170,734,305,29,size=18,bold=True)
text("vm_details","Standard_B1s ／ nic-firewall-lab ／ IPなし",170,763,305,30,size=12)

# Policy and IP/Route resources are siblings of VNet, not subnet children.
text("outside_label","VNet外で管理されるAzureリソース",993,285,293,33,size=15,fg="#52748E",bold=True)
shape("policy_node","",989,332,284,162,fill="#F6F1FF",stroke="#8B6CB9",stroke_width=1.7)
text("policy_head","Firewall Policy Basic",1005,344,262,30,size=18,fg="#684494",bold=True)
text("policy_id","policy-firewall-lab",1005,374,261,26,size=15,fg="#684494")
shape("rule_node","",1007,415,247,64,fill="#FFFFFF",stroke="#B7A1D4")
text("rule_name","rcg-web-lab",1023,422,215,22,size=14,bold=True)
text("rule_cond","HTTPS www.google.com:443 のみ許可",1023,448,222,26,size=12)

shape("pip_data","",989,508,284,72,fill="#FFFFFF",stroke="#6EA7CF")
text("pip_data_name","Public IP（通信用）",1005,512,260,22,size=16,bold=True)
text("pip_data_id","pip-firewall-lab　|　Standard・Static",1005,539,260,32,size=13)

shape("pip_mgmt","",989,594,284,72,fill="#FFFFFF",stroke="#6EA7CF")
text("pip_mgmt_name","Public IP（管理用）",1005,598,260,22,size=16,bold=True)
text("pip_mgmt_id","pip-firewall-mgmt-lab　|　Standard・Static",1005,625,260,30,size=13)

shape("route_node","",989,692,284,105,fill="#EDF7FF",stroke="#6EA7CF")
text("route_head","ルートテーブル（UDR）",1005,698,260,27,size=17,bold=True)
text("route_name","rt-firewall-lab",1005,726,258,24,size=14)
text("route_next","0.0.0.0/0 → Firewall のPrivate IP",1005,750,260,31,size=13)

# Azure external target destinations
shape("external_box","",1360,203,360,552,fill="#FAFCFE",stroke="#94ABC0",stroke_width=2)
shape("external_band","",1371,215,338,59,fill="#DFEDFA",stroke="#DFEDFA",stroke_width=0)
text("external_title","インターネット上のアクセス先",1387,228,305,34,size=18,fg="#194F7B",bold=True)
shape("target_google","",1384,316,307,116,fill="#EAF8EF",stroke="#4CAD80",stroke_width=2)
text("g_icon","✓",1401,333,49,55,size=32,fg="#15925B",bold=True,align="center")
text("google_name","www.google.com",1451,333,226,36,size=18,bold=True)
text("google_status","HTTPS 443：許可",1451,374,226,34,size=15,fg="#168753",bold=True)
shape("target_ms","",1384,491,307,116,fill="#FFF1F1",stroke="#D98B8B",stroke_width=2)
text("m_icon","×",1401,506,49,55,size=34,fg="#B63E42",bold=True,align="center")
text("ms_name","www.microsoft.com",1451,508,229,32,size=17,bold=True)
text("ms_status","HTTPS 443：既定で拒否",1451,546,230,34,size=15,fg="#BA484B",bold=True)
text("target_note","※Google許可ルール適用後の期待動作",1386,629,303,40,size=14,fg="#53687E")
text("initial_note","ルール未設定時：両方とも既定拒否",1386,666,303,35,size=14,fg="#53687E")

# Flow and association edges with explicit labels (geometry is editable)
edge("vm_outbound",487,762,590,544,color=COLORS["azure"],width=4,bends=[(590,762)])
text("vm_outbound_text","VMのインターネット宛送信",508,722,380,24,size=13,fg="#1B6DA3",bold=True)
edge("fw_green",813,449,1384,357,color=COLORS["green"],width=4,bends=[(965,449),(965,283),(1347,283),(1347,357)])
edge("fw_red",813,480,1384,543,color=COLORS["red"],width=3,dashed=True,bends=[(955,480),(955,852),(1350,852),(1350,543)])
edge("policy_attach",989,405,818,465,color="#8B6CB9",width=2,dashed=True,arrow=False,bends=[(947,405),(947,465)])
edge("route_to_workload",990,760,941,749,color="#287DBD",width=2,dashed=True,arrow=False,bends=[(968,760),(968,749)])
edge("pip_connect",989,540,816,532,color="#287DBD",width=2,dashed=True,arrow=False,bends=[(955,540),(955,532)])
edge("mgmt_connect",989,628,941,630,color="#287DBD",width=2,dashed=True,arrow=False)

# Footer notes
shape("footer_bg","",35,937,1685,40,fill="#EAF2FA",stroke="#BED5E9",round=True)
text("footer","学習ポイント　① Firewallを配置するだけでは通信経路は変わらない　② UDRで経路を指定　③ Policyで通信を許可・拒否　④ 実験後にRGを削除",53,941,1640,32,size=15,fg="#285777",bold=True)

ET.indent(mxfile)
tree=ET.ElementTree(mxfile)
tree.write(OUT,encoding="utf-8",xml_declaration=True)
print("DRAWIO_CREATED",OUT,"bytes",OUT.stat().st_size,"elements",len(root))