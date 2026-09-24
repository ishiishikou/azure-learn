# AZ-900 Domain 1 問題セット 03

検証日: 2026-09-24

対象: Describe cloud concepts

状態: original

この問題セットはMicrosoft公式Training Moduleを根拠に作成した独自問題であり、Practice Assessmentや第三者問題の転載ではありません。

## Q1. Security

企業はオンプレミスだけで運用する場合と比べ、クラウドで利用できるセキュリティ機能や脅威対策を活用しつつ、自社が担当すべきデータやアクセス管理の責任も果たしたいと考えています。最も適切な説明はどれですか。

A. クラウドではセキュリティ責任がすべてプロバイダーへ移る  
B. クラウドはセキュリティ機能を提供するが、利用者にも責任が残る  
C. クラウドを使うとID管理は不要になる  
D. SaaSでは利用者データの保護責任も必ずゼロになる

**正解: B**

**解説:** クラウドではプロバイダーが物理基盤などを保護し、利用者はサービスモデルに応じてデータ、ID、アクセス、構成などの責任を持ちます。クラウドのセキュリティ機能を活用できることと、shared responsibilityは両立します。

**誤答理由:**
- A: shared responsibilityに反します。すべての責任がプロバイダーへ移るわけではありません。
- C: IDとアクセス管理はクラウドでも重要な利用者責任です。
- D: SaaSでも利用者が扱うデータやアカウントに関する責任は残ります。

**試験で見分けるポイント:** 「クラウドなら全部安全」「全部Microsoft責任」という極端な選択肢を避け、サービスモデルごとの責任分担を意識します。

**対応skill:** Describe the benefits of using cloud services / security  
**公式根拠:** https://learn.microsoft.com/en-us/training/modules/describe-benefits-use-cloud-services/

## Q2. Manageability

運用担当者は、WebポータルだけでなくCLIやAPI、テンプレートなど複数の方法を使ってクラウドリソースを作成・管理し、自動化も行いたいと考えています。この特徴を最もよく表すクラウドの利点はどれですか。

A. Manageability  
B. Capital expenditure  
C. Geographic region  
D. Private cloud

**正解: A**

**解説:** Manageabilityは、クラウド環境をポータル、CLI、API、PowerShell、テンプレートなどで管理し、自動化できることに関係します。

**誤答理由:**
- B: Capital expenditureは費用モデルであり、管理手段の柔軟性ではありません。
- C: Regionはリソース配置の地理的単位です。
- D: Private cloudはクラウド配置モデルであり、複数の管理インターフェースを使える利点そのものではありません。

**試験で見分けるポイント:** 「ポータル」「CLI」「API」「自動化」「テンプレート」はmanageabilityの典型的な手掛かりです。

**対応skill:** Describe the benefits of using cloud services / governance and manageability  
**公式根拠:** https://learn.microsoft.com/en-us/training/modules/describe-benefits-use-cloud-services/

## Q3. Elasticity

ECサイトのアクセス数は普段は少ないものの、短時間だけ急増することがあります。需要増加時に自動でリソースを増やし、需要が下がったら余分なリソースを減らしてコストを抑えたい場合、最も関係が深い特性はどれですか。

A. Elasticity  
B. CapEx  
C. Shared responsibility  
D. Hybrid cloud

**正解: A**

**解説:** Elasticityは需要の変化に応じてリソースを動的に増減できる性質です。ピーク時に拡張し、需要低下時に縮小することで必要な容量へ追従できます。

**誤答理由:**
- B: CapExは先行設備投資を表す費用分類です。
- C: Shared responsibilityはセキュリティや運用責任の分担です。
- D: Hybrid cloudはオンプレミスとクラウドなどを組み合わせる配置モデルです。

**試験で見分けるポイント:** 「需要に合わせて増減」「ピーク後に縮小」「動的」はelasticityを示します。単に能力を増やせるというscalabilityより、需要への追従性が強調されています。

**対応skill:** Describe the benefits of using cloud services / scalability and elasticity  
**公式根拠:** https://learn.microsoft.com/en-us/training/modules/describe-benefits-use-cloud-services/

## Q4. IaaS use case

既存の業務アプリケーションをクラウドへ移行します。アプリは特定のOS設定と独自ミドルウェアを必要とし、運用チームはゲストOSを含めて細かく制御したいと考えています。最も適したサービスモデルはどれですか。

A. IaaS  
B. SaaS  
C. 完全マネージドSaaSへの置換が必須  
D. Serverlessのみ

**正解: A**

**解説:** IaaSは仮想マシン、ネットワーク、ストレージなどの基盤をクラウドから利用しつつ、利用者がゲストOSやアプリケーションを管理できます。既存ワークロードのlift-and-shiftやOSレベルの制御が必要な場合に適します。

**誤答理由:**
- B: SaaSでは完成したアプリケーションを利用するため、通常はゲストOSを利用者が制御しません。
- C: 要件上、既存アプリとOS設定を維持したいので、SaaSへの置換が必須とはいえません。
- D: Serverlessは基盤管理を抽象化するため、ゲストOSを細かく制御したい要件とは合いません。

**試験で見分けるポイント:** 「OSを管理したい」「既存サーバーを移行」「最大の制御」はIaaSを示す強い手掛かりです。

**対応skill:** Describe cloud service types / IaaS  
**公式根拠:** https://learn.microsoft.com/en-us/training/modules/describe-cloud-service-types/

## Q5. SaaS use case

企業は従業員向けのメールやコラボレーション機能を導入したいと考えています。サーバー、OS、アプリケーション更新の管理はできるだけサービス提供者へ任せ、利用者は完成したアプリケーションを使うことに集中したい場合、最も適したサービスモデルはどれですか。

A. SaaS  
B. IaaS  
C. オンプレミスのみ  
D. 仮想マシンを自社で構築してアプリも保守する

**正解: A**

**解説:** SaaSでは、サービス提供者が完成したアプリケーションとその基盤を運用し、利用者はアプリケーション機能を利用します。メールやコラボレーションなどの完成サービスに適します。

**誤答理由:**
- B: IaaSでは利用者側にOSやアプリケーション管理が多く残ります。
- C: オンプレミス限定では、管理負荷をサービス提供者へ移すという要件を満たしません。
- D: 自社でVMとアプリを保守する方式は、今回減らしたい管理作業を残します。

**試験で見分けるポイント:** 「完成したアプリを利用」「OSやアプリ更新を提供者へ任せる」はSaaSの典型です。

**対応skill:** Describe cloud service types / SaaS  
**公式根拠:** https://learn.microsoft.com/en-us/training/modules/describe-cloud-service-types/

## Coverage

| Question | Skill group | 主論点 |
| --- | --- | --- |
| Q1 | Benefits of cloud services | Security / shared responsibility |
| Q2 | Benefits of cloud services | Manageability |
| Q3 | Benefits of cloud services | Elasticity |
| Q4 | Cloud service types | IaaS use case |
| Q5 | Cloud service types | SaaS use case |

Domain 1は主要論点を一巡したため、次回は既存15問のcoverageをStudy Guideと照合し、抜けがあれば補完、十分ならDomain 2へ進みます。
