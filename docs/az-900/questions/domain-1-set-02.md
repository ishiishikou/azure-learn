# AZ-900 Domain 1 問題セット 02

検証日: 2026-09-24

対象: Describe cloud concepts

状態: original

この問題セットはMicrosoft公式Study Guide / Training Moduleを根拠に作成した独自問題であり、Practice Assessmentや第三者問題の転載ではありません。

## Q1. High availability

あるWebサービスでは、基盤の一部に障害が発生しても利用者がサービスを継続して利用できることを重視しています。この要件に最も直接対応するクラウドの利点はどれですか。

A. High availability  
B. Capital expenditure  
C. Manual provisioning  
D. Private cloud

**正解: A**

**解説:** High availabilityは、障害や中断が発生してもサービスを利用可能な状態に保つことを目指す考え方です。クラウドでは冗長化などを利用して可用性を高められます。

**誤答理由:**
- B: Capital expenditureは設備などへの先行投資を表す費用モデルであり、可用性そのものではありません。
- C: 手動プロビジョニングは障害時の継続利用を直接保証する利点ではありません。
- D: Private cloudは配置モデルであり、高可用性という要件への直接の回答ではありません。

**試験で見分けるポイント:** 「障害があっても使い続けたい」「停止時間を抑えたい」はavailabilityの論点です。

**対応skill:** Describe the benefits of using cloud services / high availability and scalability  
**公式根拠:** https://learn.microsoft.com/en-us/training/modules/describe-benefits-use-cloud-services/

## Q2. Reliability

システム設計で、ある場所の大規模障害が発生しても別の場所で処理を継続できるよう、地理的に分散したリソースを利用することを検討しています。この設計が主に高めるクラウドの利点はどれですか。

A. Reliability  
B. Capital expenditure  
C. SaaS licensing  
D. Vertical scalingのみ

**正解: A**

**解説:** Reliabilityは障害から回復し、システムが機能を継続できる能力に関係します。クラウドでは地理的分散を利用できるため、障害の影響を局所化し、回復性を高める設計が可能です。

**誤答理由:**
- B: 費用分類であり、障害耐性の説明ではありません。
- C: SaaSのライセンス方式は、地理的分散による回復性の論点ではありません。
- D: 単一リソースを大きくするvertical scalingだけでは、地理的な障害への耐性を直接実現しません。

**試験で見分けるポイント:** 「障害から回復」「別の場所で継続」「地理的分散」はreliabilityの手掛かりです。

**対応skill:** Describe the benefits of using cloud services / reliability and predictability  
**公式根拠:** https://learn.microsoft.com/en-us/training/modules/describe-benefits-use-cloud-services/

## Q3. Predictability

企業は新しいサービスについて、需要に応じた性能の見通しを立てやすくし、クラウド利用料金も予測・管理しやすくしたいと考えています。この要件に対応するクラウドの利点はどれですか。

A. Predictability  
B. Hybrid cloud  
C. Shared responsibility  
D. Scale in

**正解: A**

**解説:** Predictabilityは、クラウド環境における性能やコストを予測しやすくする利点です。需要、リソース利用、料金に関する情報やツールを利用して計画できます。

**誤答理由:**
- B: Hybrid cloudは配置モデルであり、性能・コストの予測可能性そのものではありません。
- C: Shared responsibilityはクラウド利用者とプロバイダーの責任分界を示します。
- D: Scale inはインスタンス数を減らす操作であり、predictability全体を表す概念ではありません。

**試験で見分けるポイント:** 「性能の見通し」「コストを予測・計画」はpredictabilityを示します。

**対応skill:** Describe the benefits of using cloud services / reliability and predictability  
**公式根拠:** https://learn.microsoft.com/en-us/training/modules/describe-benefits-use-cloud-services/

## Q4. Governance

企業は複数チームがクラウドリソースを作成する際に、組織で定めた標準へ継続的に従わせ、逸脱を把握しやすくしたいと考えています。この要件と最も関係が深いクラウドの利点はどれですか。

A. Governance  
B. Scale up  
C. SaaS  
D. Public cloudのみ

**正解: A**

**解説:** Governanceは、クラウド資産が組織の標準や要件へ適合するよう管理する考え方です。クラウドではテンプレートや監査などを通じ、標準への適合を支援できます。

**誤答理由:**
- B: Scale upは個々のリソース能力を増やすスケーリング操作です。
- C: SaaSはサービス種別であり、組織標準への適合を管理する概念そのものではありません。
- D: Public cloudは配置モデルです。ガバナンスはpublic cloudかどうかだけで決まる概念ではありません。

**試験で見分けるポイント:** 「組織標準」「コンプライアンス」「監査」「ルールへの適合」はgovernanceの論点です。

**対応skill:** Describe the benefits of using cloud services / governance and manageability  
**公式根拠:** https://learn.microsoft.com/en-us/training/modules/describe-benefits-use-cloud-services/

## Q5. Serverless

開発チームはイベント発生時だけコードを実行し、サーバーのプロビジョニングや管理をできるだけ意識せずに処理を実装したいと考えています。最も適したクラウドの考え方はどれですか。

A. Serverless computing  
B. IaaS VMを常時稼働させる  
C. Private cloudのみを構築する  
D. 物理サーバーを最大需要分購入する

**正解: A**

**解説:** Serverless computingでは、開発者はサーバー基盤の管理を抽象化し、アプリケーションコードやイベント処理へ集中できます。必要に応じて処理を実行する用途に適します。

**誤答理由:**
- B: IaaS VMではゲストOSを含むサーバー管理責任がより多く利用者側に残ります。
- C: Private cloudは配置モデルであり、サーバー管理を抽象化するserverlessの要件とは別軸です。
- D: 最大需要分の物理設備を先行購入する方式は、クラウドのserverless利用とは逆方向です。

**試験で見分けるポイント:** 「イベント駆動」「サーバー管理を意識しない」「コードに集中」はserverlessの代表的な手掛かりです。

**対応skill:** Describe cloud computing / define serverless computing  
**公式根拠:** https://learn.microsoft.com/en-us/training/modules/describe-cloud-compute/

## Coverage

| Question | Skill group | 主論点 |
| --- | --- | --- |
| Q1 | Benefits of cloud services | High availability |
| Q2 | Benefits of cloud services | Reliability |
| Q3 | Benefits of cloud services | Predictability |
| Q4 | Benefits of cloud services | Governance |
| Q5 | Cloud computing | Serverless computing |

次回はDomain 1の残る薄い論点（security、manageability、elasticity、IaaS/SaaSの適切なuse caseなど）を優先します。
