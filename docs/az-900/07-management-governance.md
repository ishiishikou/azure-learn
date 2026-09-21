# 07. Management & Governance

## Cost factors

Azure Costは、利用Service、Region、使用量、VM Size、Storage容量・Redundancy、Network Transfer、契約・割引などで変化します。

## Pricing Calculator

Azure導入前の料金見積もりに使います。

~~~text
VM x 2
Storage 1 TB
Network Transfer
      ↓
Estimated Cost
~~~

覚え方: 「使う前にいくら？」= Pricing Calculator。

## Cost Management

実際に利用したAzure Costを分析・管理します。

- Cost Analysis。
- Budget。
- Cost Alert。
- Subscription / Resource Group / Tagなどで集計。

覚え方: 「今いくら使っている？」= Cost Management。

## Tags

ResourceへKey/ValueのLabelを付けます。

~~~text
Environment = Production
Project = A
Owner = Yamada
~~~

用途は分類、検索、Cost Allocationなどです。

Tag自体はSecurity Controlではありません。

## Azure Policy

組織のResource Ruleを評価・強制します。

例:

~~~text
Allowed Region
→ Japan East / Japan Westのみ

Required Tag
→ Environment Tag必須

Public Access
→ 禁止
~~~

覚え方:

~~~text
RBAC
→ 誰が何をできる？

Policy
→ どんなResource Configurationを許す？
~~~

## Resource Lock

重要Resourceの誤変更・誤削除を防ぎます。

- CanNotDelete: 変更可、削除不可。
- ReadOnly: Read only。変更・削除不可。

Lockを外す権限があるUserは、Lockを削除してからResourceを操作できます。「OwnerならLockを無視できる」という意味ではありません。

## Microsoft Purview

「マイクロソフト パービュー」。

Data Discovery、Classification、Governance、Complianceなど、組織内Dataを把握・統制するためのService群です。

試験では「Data Governance / Data Classification」が出たらPurviewを連想します。

## Azure Portal / CLI / PowerShell / Cloud Shell

| Tool | 役割 |
|---|---|
| Azure Portal | Web GUI |
| Azure CLI | az commandによるCLI |
| Azure PowerShell | PowerShell Cmdlet |
| Cloud Shell | Browser上でCLI/PowerShellを使えるShell |

## Azure Resource Manager

ARMはAzure Resourceを管理するControl Planeの基盤です。

~~~text
Portal
CLI
PowerShell
ARM Template
Terraform
   ↓
Azure Resource Manager
   ↓
VM / Storage / VNet ...
~~~

## ARM Template / IaC

Infrastructure as Codeにより、Infrastructure ConfigurationをCodeとして定義・再現します。

ARM TemplateはAzure NativeなDeclarative IaCです。

~~~text
Code
 ↓
同じ構成をRepeatableにDeploy
~~~

## Azure Arc

「アジュール アーク」。

On-premisesや他CloudのResourceをAzure Management / Governanceへ接続します。

~~~text
Azure
├─ Azure Resource
├─ On-prem Server
├─ AWS Server
└─ GCP Server
       ↑
    Azure Arc
~~~

覚え方: Hybrid / Multi-cloudをAzureから管理。

## Azure Monitor

AzureのMonitoring Platformです。

~~~text
VM / App / DB / Storage
         ↓
     Azure Monitor
     ├─ Metrics
     ├─ Logs
     ├─ Alerts
     └─ Application Insights
~~~

### Metrics

CPU Usage、Request Countなどの数値Data。

### Logs

Eventや詳細Record。

## Log Analytics

Log Analytics Workspaceへ集めたLogをQuery・Analysisします。

KQLを利用できますが、AZ-900ではSyntax暗記は不要です。

## Azure Monitor Alerts

Conditionを満たしたときにNotificationやActionを実行します。

~~~text
CPU > 90%
   ↓
Alert
   ↓
Notification / Action
~~~

## Application Insights

Application Performance Monitoringに利用します。

代表例:

- Request。
- Response Time。
- Failure。
- Dependency。
- Trace。

## Azure Service Health

Azure Service側のIncident、Planned Maintenanceなど、自分のSubscriptionへ影響するAzure側の状態を確認します。

~~~text
自分のVMのCPUが高い
→ Azure Monitor

Japan EastでAzure Service Incident
→ Service Health
~~~

## Azure Advisor

利用中のAzure Resourceを見て、Cost、Reliability、Security、Performanceなどの改善Recommendationを提示します。

~~~text
Monitor
→ 何が起きている？

Service Health
→ Azure側で問題が起きている？

Advisor
→ どう改善したらよい？
~~~

## 最重要比較

| キーワード | 答え |
|---|---|
| 利用前の料金見積もり | Pricing Calculator |
| 利用中のCost分析 | Cost Management |
| Resource分類 | Tags |
| Configuration Ruleの強制 | Azure Policy |
| 誤削除・変更防止 | Resource Lock |
| Data Governance | Microsoft Purview |
| GUI管理 | Azure Portal |
| Browser上のShell | Cloud Shell |
| Azure Resource管理基盤 | ARM |
| InfrastructureをCode化 | IaC / ARM Template |
| Hybrid / Multi-cloud管理 | Azure Arc |
| Resource監視 | Azure Monitor |
| Log分析 | Log Analytics |
| 条件で通知 | Monitor Alerts |
| Application Monitoring | Application Insights |
| Azure側のIncident | Service Health |
| 改善提案 | Advisor |
