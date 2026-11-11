"""Azure Firewall Basic diagram — authoring based on jgraph/drawio-mcp's official skill.

Principles:
- Native, uncompressed .drawio XML
- Azure icons from official shape index; no guessed mxgraph stencil names
- Orthogonal edge routing, no manual waypoints or arbitrary diagonals
- Semantic containers / children with relative coordinates
- Diagram depicts a PROPOSED configuration, not deployed state
"""
from __future__ import annotations
from xml.etree import ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "diagrams" / "azure-firewall-basic.drawio"
OUT.parent.mkdir(parents=True, exist_ok=True)

COL = {
    "ink": "#193550", "muted": "#567087", "blue": "#1473B9",
    "border": "#BFD0DD", "surface": "#F7FAFC", "vnet": "#F0F7FD",
    "softBlue": "#E8F2FA", "orange": "#C87822", "softOrange": "#FFF5EA",
    "green": "#11855C", "softGreen": "#EAF7F0",
    "red": "#C34748", "softRed": "#FFF0F1", "white": "#FFFFFF",
}
W, H = 1760, 950
mx = ET.Element("mxfile", host="app.diagrams.net", agent="jgraph-official-drawio-skill-derived",
                version="26.0.0", type="device")
diagram = ET.SubElement(mx, "diagram", id="azure-fw-basic", name="Azure Firewall Basic - Outbound")
model = ET.SubElement(diagram, "mxGraphModel", dx=str(W),dy=str(H),grid="1",
                      gridSize="10",guides="1",tooltips="1",connect="1",arrows="1",
                      fold="1",page="1",pageScale="1",pageWidth=str(W),
                      pageHeight=str(H),math="0",shadow="0")
root = ET.SubElement(model, "root")
ET.SubElement(root, "mxCell", id="0")
ET.SubElement(root, "mxCell", id="1", parent="0")

VERTICES = {}
ABSOLUTE = {}

def cell(id, value, x, y, w, h, *, fill=None, stroke=None, font=None, fs=17,
         bold=False, align="left", round=10, sw=1.3, extras="", parent="1",
         pad=12, valign="middle"):
    style = (
        f"rounded={1 if round else 0};arcSize={round};"
        "whiteSpace=wrap;html=1;overflow=hidden;glass=0;shadow=0;"
        f"fillColor={fill or 'none'};strokeColor={stroke or 'none'};"
        f"strokeWidth={sw};"
        f"fontColor={font or COL['ink']};fontSize={fs};fontStyle={1 if bold else 0};"
        f"fontFamily=Arial;align={align};verticalAlign={valign};"
        f"spacingLeft={pad};spacingRight={pad};spacingTop=3;spacingBottom=3;"
        + extras
    )
    item = ET.SubElement(root, "mxCell", id=id, value=value, style=style, vertex="1", parent=parent)
    ET.SubElement(item,"mxGeometry",x=str(x),y=str(y),width=str(w),height=str(h),attrib={"as":"geometry"})
    VERTICES[id] = item
    ABSOLUTE[id] = (x,y)
    return item

def label(id, txt,x,y,w,h,*,fs=17,bold=False,color=None,align="left",pad=0):
    return cell(id,txt,x,y,w,h,fs=fs,bold=bold,font=color or COL["ink"],align=align,
                round=0,sw=0,pad=pad,extras="pointerEvents=0;")

def icon(id,x,y,w,h,url):
    return cell(id,"",x,y,w,h,round=0,sw=0,pad=0,
                extras=("shape=image;imageAspect=0;aspect=fixed;"
                        f"image={url};verticalLabelPosition=bottom;"))

def connect(id, src, dst, color, *, width=3, dashed=False,
            exitXY=None, entryXY=None, arrow=True, parent="1"):
    style=(f"edgeStyle=orthogonalEdgeStyle;orthogonalLoop=1;jettySize=auto;html=1;"
           f"rounded=0;curved=0;strokeColor={color};strokeWidth={width};"
           f"endArrow={'block' if arrow else 'none'};endFill=1;"
           f"dashed={1 if dashed else 0};"
           + "defaultLabelBackgroundColor=page;")
    if exitXY is not None:
        style += f"exitX={exitXY[0]};exitY={exitXY[1]};exitPerimeter=0;"
    if entryXY is not None:
        style += f"entryX={entryXY[0]};entryY={entryXY[1]};entryPerimeter=0;"
    e=ET.SubElement(root,"mxCell",id=id,value="",style=style,edge="1",
                    source=src,target=dst,parent=parent)
    ET.SubElement(e,"mxGeometry",relative="1",attrib={"as":"geometry"})
    return e

# Global header
cell("title_rule","",47,38,7,80,fill=COL["blue"],round=0,sw=0)
label("title","Azure Firewall Basic｜学習用ネットワーク構成図",76,36,1240,51,
      fs=30,bold=True)
label("subtitle","アウトバウンド通信：VM → Azure Firewall → インターネット",77,88,1130,34,
      fs=17,color=COL["muted"])
cell("status_chip","構築予定・実機未検証",1394,56,294,38,
     fill=COL["softBlue"],stroke="#D7E6F2",font=COL["muted"],fs=15,
     align="center",round=14,sw=1)
cell("header_divider","",47,140,1665,2,fill="#DCE7EF",round=0,sw=0)

# Azure vs Internet high-level regions
cell("subscription","",46,166,1236,701,fill="#F8FBFE",stroke="#B3CCDE",sw=1.8,round=12)
label("subscription_title","Azure サブスクリプション",72,184,740,37,fs=22,bold=True)
cell("region_chip","Japan East",1055,187,190,34,fill=COL["softBlue"],
     stroke="#CAE2F4",fs=15,font=COL["blue"],bold=True,align="center")
cell("rg","",72,233,1184,601,fill=COL["white"],stroke="#C6DAE8",sw=1.6,round=12)
label("rg_label","Resource Group　rg-firewall-lab",96,250,905,36,fs=20,bold=True)

cell("vnet","",97,306,1133,373,fill=COL["vnet"],stroke="#91BAD9",sw=1.7,round=12)
icon("vnet_icon",119,321,45,32,"https://app.diagrams.net/img/lib/azure2/networking/Virtual_Networks.svg")
label("vnet_label","Virtual Network　vnet-firewall-lab",172,316,775,43,fs=19,bold=True)
cell("vnet_range","10.0.0.0/16",1006,323,190,35,fill=COL["white"],
     stroke="#CFDFEB",fs=15,bold=True,align="center")

# Workload subnet, with a generous framed resource card
cell("workload_subnet","",129,376,341,248,fill=COL["white"],stroke="#91BBDB",sw=1.6)
label("workload_title","WorkloadSubnet",148,388,289,34,fs=18,bold=True)
label("workload_range","10.0.2.0/24",148,417,260,25,fs=14,color=COL["muted"])
cell("vm_node","",151,462,294,105,fill=COL["white"],stroke="#CBDCE8",sw=1.4)
icon("vm_icon",168,481,53,52,"https://app.diagrams.net/img/lib/azure2/compute/Virtual_Machine.svg")
label("vm_title","Ubuntu VM",232,471,200,27,fs=19,bold=True)
label("vm_name","vm-firewall-lab",232,502,202,24,fs=15,color=COL["muted"])
label("vm_private","Standard_B1s ｜ Private IPあり / Public IPなし",164,534,270,28,fs=12,color=COL["muted"])
cell("workload_udr","UDR適用：0.0.0.0/0 → Firewall",151,581,294,27,
     fill=COL["softBlue"],stroke="none",round=8,sw=0,
     font="#25678E",fs=12,align="center")

# Firewall subnet
cell("azfw_subnet","",530,376,342,248,fill=COL["white"],stroke="#91BBDB",sw=1.6)
label("azfw_subnet_title","AzureFirewallSubnet",549,388,298,34,fs=18,bold=True)
label("azfw_range","10.0.0.0/26",549,417,291,25,fs=14,color=COL["muted"])
cell("fw_node","",552,462,296,105,fill="#FFFBF5",stroke="#E5B774",sw=1.6)
icon("fw_icon",569,480,52,52,"https://icons.diagrams.net/assets/azure/1/Azure_Firewall.svg")
label("fw_title","Azure Firewall Basic",637,467,210,28,fs=19,bold=True)
label("fw_name","fw-firewall-lab",637,501,201,25,fs=15,color=COL["muted"])
label("fw_private","Private IP：デプロイ後に決定",637,530,200,24,fs=12,color=COL["muted"])
cell("fw_block_marker","×",661,580,38,38,fill=COL["softRed"],
     stroke="#DCA2A5",font=COL["red"],fs=26,bold=True,align="center")
label("fw_block_reason","Microsoft宛はここで遮断",705,582,154,30,fs=13,color=COL["red"],bold=True)

# Dedicated management subnet. No workload path touches this.
cell("mgmt_subnet","",904,552,293,107,fill=COL["white"],stroke="#B9D1E1",sw=1.5)
label("mgmt_subnet_title","AzureFirewallManagementSubnet",917,564,267,28,
      fs=15,bold=True)
label("mgmt_cidr","10.0.1.0/26",917,591,262,23,fs=14,color=COL["muted"])
label("mgmt_detail","Basicの管理通信専用",917,616,263,26,fs=13,color=COL["muted"])

# Control plane resources are RG objects, not nested inside subnets.
label("control_caption","VNetの外側で管理されるAzureリソース",105,696,1010,27,fs=14,color=COL["muted"])
cell("route_node","",111,733,337,88,fill="#F7FBFF",stroke="#C4DBEB",sw=1.4)
label("route_title","Route Table (UDR)",130,742,302,25,fs=17,bold=True)
label("route_name","rt-firewall-lab",130,769,299,21,fs=14,color=COL["muted"])
label("route_next","WorkloadSubnet に適用",130,795,299,21,fs=12,color=COL["blue"])
cell("policy_node","",461,733,342,88,fill="#F8F5FE",stroke="#D7C6E8",sw=1.4)
icon("policy_icon",481,752,53,48,"https://app.diagrams.net/img/lib/azure2/networking/Azure_Firewall_Policy.svg")
label("policy_head","Firewall Policy Basic",549,739,244,27,fs=17,bold=True)
label("policy_id","policy-firewall-lab",549,768,244,22,fs=14,color=COL["muted"])
label("rule_cond","www.google.com:443 を許可",549,791,244,24,fs=12,color="#725699")
cell("pip_node","",819,733,400,88,fill="#F9FCFF",stroke="#C6DCEB",sw=1.4)
label("pip_heading","Standard Public IP (Static) ×2",838,742,359,24,fs=16,bold=True)
label("pip_data","通信用：pip-firewall-lab",838,768,357,21,fs=13,color=COL["muted"])
label("pip_mgmt","管理用：pip-firewall-mgmt-lab",838,792,357,20,fs=13,color=COL["muted"])

# Internet destination panel
cell("external_box","",1319,233,403,602,fill=COL["white"],stroke="#C5D4DE",sw=1.6,round=12)
label("external_title","Azureからのアクセス先",1345,257,356,35,fs=21,bold=True)
label("external_sub","通信結果はルール適用後の期待動作",1345,300,352,31,
      fs=14,color=COL["muted"])

cell("target_google","",1357,461,327,106,fill=COL["softGreen"],stroke="#96CDB0",sw=1.8)
cell("google_icon","✓",1372,486,42,42,fill="#D5F0DF",stroke="none",
     font=COL["green"],fs=27,bold=True,align="center",round=20,sw=0)
label("google_name","www.google.com",1432,472,240,30,fs=19,bold=True)
label("google_status","HTTPS 443：許可",1432,513,239,30,fs=16,
      color=COL["green"],bold=True)

cell("target_ms","",1357,607,327,108,fill=COL["softRed"],stroke="#E4B0B3",sw=1.7)
cell("ms_icon","×",1372,635,42,42,fill="#FFE0E2",stroke="none",
     font=COL["red"],fs=27,bold=True,align="center",round=20,sw=0)
label("ms_name","www.microsoft.com",1432,617,240,30,fs=18,bold=True)
label("ms_status","Firewallで既定拒否",1432,657,240,28,fs=15,
      color=COL["red"],bold=True)
label("no_forward","宛先に転送されません",1358,738,323,31,fs=14,
      color=COL["red"],bold=True,align="center")
label("initial_note","許可ルールの追加前は両方とも拒否",1354,784,334,28,
      fs=13,color=COL["muted"],align="center")

# ONLY genuine traffic paths. All are perpendicular and source/target-linked.
connect("vm_outbound","vm_node","fw_node",COL["blue"],width=3.5,
        exitXY=(1,0.50),entryXY=(0,0.50),parent="vnet")
connect("fw_green","fw_node","target_google",COL["green"],width=3.8,
        exitXY=(1,0.50),entryXY=(0,0.50),parent="1")
connect("fw_red","fw_node","fw_block_marker",COL["red"],width=2.5,
        dashed=True,exitXY=(0.50,1),entryXY=(0.50,0),arrow=False,parent="azfw_subnet")

# Footer: concise learning cues, no extra fake traffic.
cell("footer","",46,883,1676,47,fill=COL["softBlue"],stroke="#D5E5F0",
     round=9,sw=1)
label("footer_text","学習ポイント：① UDRで経路を指定　　② Policyで通信を制御　　③ 認証・通信を確認後、学習用リソースグループを削除",
      65,890,1632,31,fs=15,bold=True,color="#2C6286")

# Assign correct parent-child structure with relative coordinates.
parents = {
 "subscription_title":"subscription", "region_chip":"subscription", "rg":"subscription",
 "rg_label":"rg", "vnet":"rg", "control_caption":"rg",
 "route_node":"rg", "policy_node":"rg", "pip_node":"rg",
 "vnet_icon":"vnet", "vnet_label":"vnet", "vnet_range":"vnet",
 "workload_subnet":"vnet","azfw_subnet":"vnet","mgmt_subnet":"vnet",
 "workload_title":"workload_subnet","workload_range":"workload_subnet",
 "workload_udr":"workload_subnet","vm_node":"workload_subnet",
 "vm_icon":"vm_node","vm_title":"vm_node","vm_name":"vm_node","vm_private":"vm_node",
 "azfw_subnet_title":"azfw_subnet","azfw_range":"azfw_subnet",
 "fw_node":"azfw_subnet","fw_block_marker":"azfw_subnet","fw_block_reason":"azfw_subnet",
 "fw_icon":"fw_node","fw_title":"fw_node","fw_name":"fw_node","fw_private":"fw_node",
 "mgmt_subnet_title":"mgmt_subnet","mgmt_cidr":"mgmt_subnet","mgmt_detail":"mgmt_subnet",
 "route_title":"route_node","route_name":"route_node","route_next":"route_node",
 "policy_icon":"policy_node","policy_head":"policy_node",
 "policy_id":"policy_node","rule_cond":"policy_node",
 "pip_heading":"pip_node","pip_data":"pip_node","pip_mgmt":"pip_node",
 "external_title":"external_box","external_sub":"external_box",
 "target_google":"external_box","target_ms":"external_box",
 "google_icon":"target_google","google_name":"target_google","google_status":"target_google",
 "ms_icon":"target_ms","ms_name":"target_ms","ms_status":"target_ms",
 "no_forward":"external_box","initial_note":"external_box",
 "footer_text":"footer",
}
for c_id,p_id in parents.items():
    item = VERTICES[c_id]
    px,py=ABSOLUTE[p_id]
    x,y=ABSOLUTE[c_id]
    geometry=item.find("mxGeometry")
    geometry.set("x",str(x-px))
    geometry.set("y",str(y-py))
    item.set("parent",p_id)

for c_id in ["subscription","rg","vnet","workload_subnet","azfw_subnet","mgmt_subnet",
             "vm_node","fw_node","route_node","policy_node","pip_node",
             "external_box","target_google","target_ms","footer"]:
    item=VERTICES[c_id]
    item.set("style",item.get("style")+"container=1;collapsible=0;recursiveResize=0;")

ET.indent(mx)
ET.ElementTree(mx).write(OUT,encoding="utf-8",xml_declaration=True)
print(f"generated: {OUT} ({OUT.stat().st_size} bytes), {len(VERTICES)} vertex shapes")