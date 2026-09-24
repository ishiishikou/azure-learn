# AZ-900 Domain 2 問題セット 01

検証日: 2026-09-25

対象: Describe Azure architecture and services

状態: original

この問題セットはMicrosoft公式Study Guide / Training Moduleを根拠に作成した独自問題であり、Practice Assessmentや第三者問題の転載ではありません。

## Q1. Management groups

企業は複数のAzure subscriptionを部門ごとに分けています。複数subscriptionへ共通のガバナンス方針をまとめて適用できる、subscriptionより上位の管理スコープが必要です。最も適切なのはどれですか。

A. Resource group  
B. Management group  
C. Availability zone  
D. Virtual network

**正解: B**

**解説:** Management groupは複数subscriptionを階層化して管理できるスコープです。ポリシーやアクセス管理を上位スコープから継承させる用途に適します。

**誤答理由:**
- A: Resource groupはsubscription内のresourceをまとめる論理コンテナーであり、複数subscriptionの上位スコープではありません。
- C: Availability zoneはリージョン内の物理的に分離されたロケーションであり、管理階層ではありません。
- D: Virtual networkはAzure上のネットワーク境界であり、subscriptionを階層管理する機能ではありません。

**試験で見分けるポイント:** 「複数subscriptionへ共通管理」「subscriptionより上位」はmanagement groupです。

**対応skill:** Describe the core architectural components of Azure / management groups, subscriptions, resource groups  
**公式根拠:** https://learn.microsoft.com/en-us/training/modules/describe-core-architectural-components-of-azure/

## Q2. Availability zones

1つのAzure region内でアプリケーションを運用します。データセンター設備の局所的な障害に備えるため、同一region内の物理的に分離されたロケーションへリソースを配置したい場合、利用すべき概念はどれですか。

A. Availability zones  
B. Management groups  
C. Azure Policy  
D. Resource groups

**正解: A**

**解説:** Availability zoneは、Azure region内にある物理的に分離されたデータセンター群です。対応するサービスを複数zoneへ配置することで、同一region内の局所障害に対する回復性を高められます。

**誤答理由:**
- B: Management groupは管理スコープです。
- C: Azure Policyはresourceの構成やコンプライアンスを評価・制御するガバナンス機能であり、物理配置単位ではありません。
- D: Resource groupはresourceの論理コンテナーで、障害ドメインを表しません。

**試験で見分けるポイント:** 「同一region内」「物理的に分離」「データセンター障害」はavailability zoneの手掛かりです。

**対応skill:** Describe the core architectural components of Azure / availability zones  
**公式根拠:** https://learn.microsoft.com/en-us/training/modules/describe-core-architectural-components-of-azure/

## Q3. Compute choice

処理要求が発生したときだけ短時間のコードを実行したいアプリケーションがあります。ゲストOSを管理せず、イベント駆動で実行し、利用していない時間のサーバー管理を避けたい場合、最も適したAzure compute optionはどれですか。

A. Azure Virtual Machines  
B. Azure Functions  
C. Availability sets  
D. Azure Virtual Desktop

**正解: B**

**解説:** Azure Functionsはイベント駆動のserverless computeです。基盤となるサーバーを利用者が管理せず、イベントに応じてコードを実行する用途に適します。

**誤答理由:**
- A: Virtual MachinesはOSレベルの制御が必要な場合に有効ですが、ゲストOS管理を避けたい今回の要件とは合いません。
- C: Availability setはVMの可用性を高めるための配置概念であり、コード実行サービスではありません。
- D: Azure Virtual Desktopはデスクトップ/アプリ仮想化サービスです。

**試験で見分けるポイント:** 「イベント駆動」「コードだけ実行」「サーバー管理不要」はFunctionsの典型です。

**対応skill:** Describe Azure compute and networking services / Azure Functions, virtual machines, containers  
**公式根拠:** https://learn.microsoft.com/en-us/training/modules/describe-azure-compute-networking-services/

## Q4. Storage redundancy

企業はAzure Storageのデータについて、単一データセンターの障害だけでなく、同一region内のavailability zone障害にも耐えたいと考えています。一方、別regionへの複製までは要件にありません。最も適した冗長化方式はどれですか。

A. LRS  
B. ZRS  
C. GRS  
D. RA-GRS

**正解: B**

**解説:** Zone-redundant storage (ZRS) は、プライマリregion内の複数availability zoneへデータを同期的に複製します。region内のzone障害への耐性が必要で、別regionへの複製が不要という要件に合います。

**誤答理由:**
- A: LRSは単一region内の単一物理ロケーションで複製するため、zone障害への耐性という要件を満たしません。
- C: GRSはセカンダリregionにも複製するため、今回の要件を超えます。
- D: RA-GRSもgeo-redundancyを使い、さらにセカンダリregionの読み取りアクセスを提供する方式です。

**試験で見分けるポイント:** 「同一regionの複数zone」はZRS、「別regionにも複製」はGRS/GZRS系を検討します。

**対応skill:** Describe Azure storage services / redundancy options  
**公式根拠:** https://learn.microsoft.com/en-us/training/modules/describe-azure-storage-services/

## Q5. Azure RBAC

開発者には特定のresource group内だけでAzure resourceを操作する権限を与え、他のresource groupには権限を広げたくありません。認証済みユーザーに対し、Azure resourceへの操作権限をscope付きで割り当てる仕組みとして最も適切なのはどれですか。

A. Azure RBAC  
B. Multi-factor authentication  
C. Single sign-on  
D. Availability zone

**正解: A**

**解説:** Azure role-based access control (Azure RBAC) は、誰が、どのresourceに対して、何を実行できるかをrole assignmentとscopeで制御します。resource groupをscopeとして必要なroleを割り当てることでleast privilegeを実現できます。

**誤答理由:**
- B: MFAは認証時に複数要素を要求する仕組みで、Azure resourceへの操作権限のscopeを定義するものではありません。
- C: SSOは複数アプリ等へのサインイン体験を簡素化する認証関連機能で、resource authorizationのscopeではありません。
- D: Availability zoneは物理的な可用性構成です。

**試験で見分けるポイント:** 「誰に」「どのscopeで」「何を許可するか」はAzure RBACです。MFA/SSOは認証側の論点と区別します。

**対応skill:** Describe Azure identity, access, and security / Azure RBAC  
**公式根拠:** https://learn.microsoft.com/en-us/training/modules/describe-azure-identity-access-security/

## Coverage

| Question | Skill group | 主論点 |
| --- | --- | --- |
| Q1 | Core architectural components | Management groups / hierarchy |
| Q2 | Core architectural components | Availability zones |
| Q3 | Compute and networking | Azure Functions / compute choice |
| Q4 | Storage services | ZRS / redundancy |
| Q5 | Identity, access, security | Azure RBAC / scope / least privilege |

4つのskill groupを初回セットで一巡した。次回はDomain 2の未カバー論点から、network connectivity、storage transfer、Entra ID / Conditional Accessなどを優先して5問追加する。