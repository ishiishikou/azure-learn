# 04. Network

まず「何と何をつなぐサービスか」で覚えます。

~~~text
Company / Home
      |
 VPN / ExpressRoute
      |
Azure VNet
├─ Subnet A → Web
└─ Subnet B → DB
~~~

## Virtual Network

VNetはAzure上のPrivate Virtual Networkです。AWSのVPCに近い概念です。

## Subnet

VNetのIP Address Spaceを分割したNetwork Segmentです。

~~~text
VNet 10.0.0.0/16
├─ Web Subnet
└─ DB Subnet
~~~

AZ-900ではCIDRの細かな計算より「IP Address Rangeを表す書き方」と理解すれば十分です。

CIDRは「サイダー」と読みます。

## VNet Peering

VNetとVNetをAzure Backbone上で接続します。

~~~text
VNet A
  |
Peering
  |
VNet B
~~~

## VPN Gateway

On-premisesや外部NetworkとAzure VNetを、Public Internet上の暗号化されたVPN Tunnelで接続します。

## ExpressRoute

On-premisesなどとAzureをPrivate Connectivityで接続します。Public Internetを通常のData Pathとして利用しない専用性の高い接続です。

~~~text
VPN Gateway
  → Internet上の暗号化Tunnel

ExpressRoute
  → Private Connection
~~~

## Azure DNS

DNS NameとIP Addressの名前解決を提供します。

## Public Endpoint

Internetから到達可能なPublic Address側のEndpointです。認証やFirewallなど別のSecurity Controlと組み合わせます。

## Service Endpoint

Azure PaaSサービスはPublic Endpointを持ったまま、特定VNet/Subnetからのアクセスとして識別・制限できるようにします。

イメージ:

~~~text
Publicな入口は残る
      +
このSubnetからの通信を許可
~~~

「人」を制限する仕組みではなく、Network Sourceを制限する仕組みです。

## Private Endpoint

PaaS Resourceへ接続するためのPrivate IPをVNet内に作ります。Private Linkを利用します。

~~~text
VNet
  |
Private IP
  |
Private Endpoint
  |
Storage / SQL / App Service など
~~~

覚え方:

~~~text
Service Endpoint
→ Public Endpointは残る

Private Endpoint
→ VNet内のPrivate IPでアクセス
~~~

## NSG

Network Security GroupはNetwork Trafficを許可・拒否するRule Setです。

~~~text
Inbound
Outbound
Protocol
Port
Source
Destination
~~~

NSG自身がNetwork同士を接続するサービスではありません。

## Azure Bastion

VMへPublic IPを付けずにRDP/SSHで管理しやすくするサービスです。

~~~text
Local PC
   ↓
Azure Bastion
   ↓
Private IPのVM
~~~

補足: Linux VMへの少量ファイル転送ではBastion Tunnel経由のSCPも可能ですが、大量・反復転送ならBlob Storage + AzCopyなどの方が適する場合があります。

## 一問一答

| 要件 | 答え |
|---|---|
| Azure内のPrivate Network | VNet |
| VNetの分割 | Subnet |
| VNet同士を接続 | VNet Peering |
| Internet経由で暗号化接続 | VPN Gateway |
| Private Connectivity | ExpressRoute |
| 名前解決 | Azure DNS |
| PaaSへVNet内Private IPで接続 | Private Endpoint |
| PaaSのPublic EndpointをSubnet単位で制御 | Service Endpoint |
| Traffic Allow/Deny | NSG |
| Public IPなしでVM管理 | Azure Bastion |
