# AZ-900 Domain 1 公式ソースマップ

検証日: 2026-09-24

対象: `Describe cloud concepts`（現行Study Guideで25–30%）

目的: 第三者dumpを転載せず、Microsoft公式情報だけから独自問題を作成・検証できる根拠を固定する。

## 正本と練習問題

- Study Guide: https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/az-900
  - 2026-07-20版のDomain 1は `Describe cloud computing` / `Describe the benefits of using cloud services` / `Describe cloud service types` の3 skill group。
- Practice Assessments: https://learn.microsoft.com/ja-jp/credentials/certifications/practice-assessments-for-microsoft-certifications
  - AZ-900が現行Practice Assessment対象に含まれる。
  - 無料で繰り返し受験でき、各問の正解・根拠・追加学習リンクを確認できる。
  - Microsoftは「本試験と同じ問題ではなく、試験全体の長さ・複雑さを表すものでもない」と明記しているため、問題文の転載元ではなく、出題スタイル・論点・根拠リンクの探索元として扱う。

## Skill group 1: Describe cloud computing

公式Module: https://learn.microsoft.com/en-us/training/modules/describe-cloud-compute/

Study Guideとの対応論点:

- cloud computingの定義
- shared responsibility model
- public / private / hybrid cloud
- 各cloud modelの適切なuse case
- consumption-based model
- cloud pricing models
- serverless

独自問題候補:

1. オンプレミス / IaaS / PaaS / SaaSで、利用者とproviderの責任境界を判定するscenario。
2. 規制・既存資産・拡張性などの要件からpublic/private/hybridを選択するscenario。
3. CapExとOpEx、従量課金、需要変動を組み合わせたcost model判定。
4. インフラ管理を最小化しイベント駆動で実行したい要件からserverlessの特徴を識別する問題。

注意: Moduleのlearning objectivesにはpricing model比較が明示されない版があるため、問題coverageの正本はあくまでStudy Guideとする。

## Skill group 2: Describe the benefits of using cloud services

公式Module: https://learn.microsoft.com/en-us/training/modules/describe-benefits-use-cloud-services/

Study Guideとの対応論点:

- high availability / scalability
- reliability / predictability
- security / governance
- manageability

独自問題候補:

1. scale up/downとscale out/inをscenarioから区別する問題。
2. 可用性・信頼性・予測可能性のどのbenefitを説明しているか判定する問題。
3. cloud governanceによる標準化・compliance enforcementと、security機能そのものを区別する問題。
4. portal / CLI / API / template等による管理性を、単なる可用性向上と混同しない問題。

注意: 現行Training Moduleには`sustainability considerations`も含まれるが、2026-07-20版AZ-900 Study GuideのDomain 1 sub-skillには明記されていない。問題集では必須coverageに追加せず、Study Guideを優先する。

## Skill group 3: Describe cloud service types

公式Module: https://learn.microsoft.com/en-us/training/modules/describe-cloud-service-types/

Study Guideとの対応論点:

- IaaS
- PaaS
- SaaS
- IaaS / PaaS / SaaSの適切なuse case

独自問題候補:

1. OSを利用者が管理したい要件からIaaSを選ぶscenario。
2. application codeに集中しOS/runtime管理をproviderへ寄せたい要件からPaaSを選ぶscenario。
3. 完成済みapplicationを利用する要件からSaaSを選ぶscenario。
4. service typeごとの利用者/provider責任範囲をshared responsibilityと横断して問う問題。

## 問題作成時の運用

- 第三者の過去問・dumpは根拠にしない。
- Microsoft Practice Assessmentは出題スタイルと論点確認に使い、問題文・選択肢をそのまま転載しない。
- 正解根拠はStudy Guideまたは上記Training Moduleへ紐付ける。
- 公式教材とStudy Guideのcoverageがずれる場合、試験範囲判定はStudy Guideを優先する。
- 次のcheckpointでは、このsource mapからDomain 1の独自問題を5問作り、正解・誤答理由・公式根拠URLを付ける。
