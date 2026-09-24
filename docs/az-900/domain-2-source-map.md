# AZ-900 Domain 2 公式ソースマップ

検証日: 2026-09-24

対象: `Describe Azure architecture and services`（現行Study Guideで35–40%）

目的: 第三者dumpを転載せず、Microsoft公式情報だけから独自問題を作成・検証できる根拠を、2026-07-20版Study Guideのskill group / sub-skillへ対応付ける。

## 正本

- Study Guide: https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/az-900
- Practice Assessments: https://learn.microsoft.com/ja-jp/credentials/certifications/practice-assessments-for-microsoft-certifications

問題coverageの正本はStudy Guideとし、Training Moduleは各sub-skillの事実確認・解説根拠として使う。Practice Assessmentは出題スタイルと論点確認に使い、問題文・選択肢は転載しない。

## Skill group 1: Describe the core architectural components of Azure

公式Module: https://learn.microsoft.com/en-us/training/modules/describe-core-architectural-components-of-azure/

Study Guideとの対応論点:

- Azure regions / region pairs / sovereign regions
- availability zones
- datacenters
- Azure resources / resource groups
- subscriptions / management groups
- resource groups, subscriptions, management groupsのhierarchy

独自問題候補:

1. 障害分離要件からavailability zoneとregionの役割を区別するscenario。
2. 複数subscriptionへ共通governanceを適用する要件からmanagement groupを選ぶ問題。
3. resource groupのライフサイクル境界と、subscriptionの課金・管理境界を区別する問題。

## Skill group 2: Describe Azure compute and networking services

公式Module: https://learn.microsoft.com/en-us/training/modules/describe-azure-compute-networking-services/

Study Guideとの対応論点:

- containers / virtual machines / Azure Functions
- Virtual Machine Scale Sets / availability sets / Azure Virtual Desktop
- VMに必要なresources
- application hosting options
- virtual networks / subnets / peering / Azure DNS
- VPN Gateway / ExpressRoute
- public endpoints / private endpoints

独自問題候補:

1. OS制御、水平スケール、イベント駆動などの要件からVM / container / Functionsを選ぶscenario。
2. VM Scale Setsとavailability setを、目的とスケール特性から区別する問題。
3. VNet peering、VPN Gateway、ExpressRouteを接続要件から選ぶ問題。
4. public endpointとprivate endpointを到達性・private network要件から区別する問題。

注意: このskill groupは2026-07-20 Study Guide change logでMinor変更対象。旧問題を再利用する場合は、サービス名・機能境界・現行推奨を公式Moduleで再検証する。

## Skill group 3: Describe Azure storage services

公式Module: https://learn.microsoft.com/en-us/training/modules/describe-azure-storage-services/

Study Guideとの対応論点:

- Azure Storage servicesの比較
- storage tiers
- redundancy options
- storage accounts / storage types
- AzCopy / Storage Explorer / Azure File Sync
- Azure Migrate / Azure Data Box

独自問題候補:

1. access頻度と保持要件からstorage tierを選ぶ問題。
2. LRS / ZRS / GRS系の冗長化を障害範囲・リージョン要件から選ぶscenario。
3. AzCopy / Storage Explorer / File Syncを転送・管理・同期要件から区別する問題。
4. 大容量オフライン転送と移行評価をData Box / Azure Migrateの役割から区別する問題。

## Skill group 4: Describe Azure identity, access, and security

公式Module: https://learn.microsoft.com/en-us/training/modules/describe-azure-identity-access-security/

Study Guideとの対応論点:

- Microsoft Entra ID / Microsoft Entra Domain Services
- SSO / MFA / passwordless authentication
- external identities
- Conditional Access
- Azure RBAC
- Zero Trust
- defense in depth
- Microsoft Defender for Cloud

独自問題候補:

1. 認証・認可・条件付きアクセスを要件から区別するscenario。
2. SSO / MFA / passwordlessをユーザー体験とsecurity要件から選ぶ問題。
3. Azure RBACのscopeとleast privilegeを問う問題。
4. Zero Trust、defense in depth、Defender for Cloudの役割を混同しない問題。

## 問題作成時の運用

- 第三者の過去問・dumpは根拠にしない。
- 正解根拠はStudy Guideまたは上記Microsoft Learn Moduleへ紐付ける。
- Study GuideとModuleの粒度がずれる場合、試験coverage判定はStudy Guideを優先する。
- Domain 2は試験比率が35–40%で最大のため、4 skill groupへ偏りなく問題を配置する。
- 次のcheckpointでは、このsource mapを使ってDomain 2の最初の独自問題セットを作成し、正解・誤答理由・公式根拠URLを付ける。
