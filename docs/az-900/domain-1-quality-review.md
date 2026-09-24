# AZ-900 Domain 1 品質レビュー

検証日: 2026-09-24

対象:
- `questions/domain-1-set-01.md`
- `questions/domain-1-set-02.md`
- `questions/domain-1-set-03.md`
- `coverage-matrix.md`
- `domain-1-source-map.md`

正本: Microsoft Learn AZ-900 Study Guide（2026-07-20版）

## 結論

Domain 1は15問で主要論点を一巡しており、次domainへ進める水準に達している。ただし、Study Guideとの厳密な対応という観点で、1件のmetadata修正と2つの薄いcoverageを今後の補完候補として残す。

## Coverage確認

| Study Guide skill group | 論点 | 対応問題 | 判定 |
| --- | --- | --- | --- |
| Describe cloud computing | cloud computing / shared responsibility | set-01 Q1, set-03 Q1 | covered |
| Describe cloud computing | public / private / hybrid cloud | set-01 Q2 | covered |
| Describe cloud computing | cloud model use cases | set-01 Q2 | covered（hybrid中心） |
| Describe cloud computing | consumption-based model / pricing | set-01 Q3 | covered |
| Describe cloud computing | serverless | set-02 Q5 | covered |
| Benefits of cloud services | high availability | set-02 Q1 | covered |
| Benefits of cloud services | scalability | set-01 Q4 | covered |
| Benefits of cloud services | reliability | set-02 Q2 | covered |
| Benefits of cloud services | predictability | set-02 Q3 | covered |
| Benefits of cloud services | security | set-03 Q1 | covered |
| Benefits of cloud services | governance | set-02 Q4 | covered |
| Benefits of cloud services | manageability | set-03 Q2 | covered |
| Cloud service types | IaaS + use case | set-03 Q4 | covered |
| Cloud service types | PaaS + use case | set-01 Q5 | covered |
| Cloud service types | SaaS + use case | set-03 Q5 | covered |

## 品質上の指摘

### 1. serverlessの対応skill metadata

`domain-1-set-02.md` Q5は本文・正解・解説自体は妥当だが、`対応skill` が `Describe cloud service types / serverless computing` となっている。

2026-07-20版Study Guideおよび本リポジトリのsource mapではserverlessは `Describe cloud computing` 側に配置されているため、metadataは次回修正する。

- 現在: `Describe cloud service types / serverless computing`
- 修正候補: `Describe cloud computing / serverless computing`

### 2. cloud model use caseはhybridへ偏っている

public / private / hybridの識別はset-01 Q2で扱っているが、独立したpublic cloud / private cloudの適切なuse caseは直接問えていない。初期15問の必須追加とはしないが、将来Domain 1を増補するときの優先候補とする。

### 3. pricing modelはconsumption-based中心

set-01 Q3で従量課金と先行設備投資の差は扱えているため最低限のcoverageはある。一方、pricing modelを比較する読解問題は1問のみなので、将来の増補候補とする。

### 4. elasticityの位置づけ

set-03 Q3はTraining Moduleに沿った有用な補助問題だが、coverage判定の正本はStudy Guideとする。Study Guide必須論点の代替として数えず、scalability本体はset-01 Q4で別途coveredとしているため問題ない。

## 重複確認

- shared responsibilityはset-01 Q1とset-03 Q1で重なるが、前者はIaaSのOS更新責任、後者はsecurity benefitとの横断問題で目的が異なるため許容。
- IaaS/PaaS/SaaSは複数問に登場するが、PaaS、IaaS、SaaSの各use caseを個別に持つため意図的な反復。
- availability / reliability / predictabilityは混同しやすい概念を別問にしており、重複ではなく識別訓練として維持する。

## 次の最小scope

1. `domain-1-set-02.md` Q5の対応skill metadataをStudy Guideに合わせて修正する。
2. その後はDomain 1の追加問題を優先せず、Domain 2（Azure architecture and services）のsource map / 問題作成へ進む。
3. Domain 1増補時はpublic/private cloud use case、pricing model比較を優先する。
