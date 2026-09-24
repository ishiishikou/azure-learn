# AZ-900 Domain 1 問題セット 01

検証日: 2026-09-24

対象: Describe cloud concepts

状態: original

この問題セットはMicrosoft公式Study Guide / Training Moduleを根拠に作成した独自問題であり、Practice Assessmentや第三者問題の転載ではありません。

## Q1. Shared responsibility model

ある企業はAzure Virtual Machines上で業務アプリケーションを稼働させます。仮想マシンのゲストOSに対するセキュリティ更新を適用する責任を負うのは誰ですか。

A. Microsoftのみ  
B. 顧客のみ  
C. Microsoftと顧客が必ず共同で個々の更新を適用する  
D. Azureリージョンを運営する通信事業者

**正解: B**

**解説:** IaaSではMicrosoftが物理データセンター、物理ネットワーク、物理ホストなどを管理しますが、顧客はゲストOSを含む仮想マシン上の構成・管理を担います。そのため、ゲストOSの更新は顧客側の責任です。

**誤答理由:**
- A: Microsoftが管理するのは基盤側であり、IaaSのゲストOS管理まで自動的にMicrosoft責任にはなりません。
- C: 責任境界は共有されますが、個々のゲストOS更新をMicrosoftと顧客が共同実施するという意味ではありません。
- D: 通信事業者はAzure VMのゲストOS管理主体ではありません。

**試験で見分けるポイント:** IaaSはPaaS/SaaSより顧客責任が広く、OS管理が顧客側に残る点を押さえます。

**対応skill:** Describe cloud computing / shared responsibility model  
**公式根拠:** https://learn.microsoft.com/en-us/training/modules/describe-cloud-compute/

## Q2. Cloud model

企業は規制上の理由から一部のシステムを自社データセンターに残す必要があります。一方、需要が急増するWeb処理にはクラウドの拡張性を利用したいと考えています。最も適したクラウドモデルはどれですか。

A. Public cloudのみ  
B. Private cloudのみ  
C. Hybrid cloud  
D. SaaSのみ

**正解: C**

**解説:** Hybrid cloudはprivate/on-premises環境とpublic cloudを組み合わせます。既存または規制対象のワークロードを自社側に残しつつ、必要な部分でpublic cloudの拡張性を利用する要件に適します。

**誤答理由:**
- A: 自社環境に残す必要があるシステムという要件を満たしません。
- B: public cloudの弾力的な拡張性を利用するという要件を十分に満たしません。
- D: SaaSはサービス提供形態であり、ここで問われているpublic/private/hybridという配置モデルの回答ではありません。

**試験で見分けるポイント:** 「一部をオンプレミスに残し、一部をpublic cloudへ」という要件はhybrid cloudの典型です。

**対応skill:** Describe cloud computing / public, private, and hybrid cloud models  
**公式根拠:** https://learn.microsoft.com/en-us/training/modules/describe-cloud-compute/

## Q3. Consumption-based model

季節によって利用量が大きく変動する新サービスを開始します。初期に最大需要分のサーバーを購入せず、実際の利用量に応じて費用を負担したい場合、クラウドのどの特徴が最も直接的に要件へ対応しますか。

A. Consumption-based model  
B. Capital expenditureを最大化するモデル  
C. 物理サーバーを数年分まとめて事前購入するモデル  
D. すべての利用量に関係なく常に同額になるモデル

**正解: A**

**解説:** Consumption-based modelでは、必要なリソースを利用し、その利用に応じて支払う考え方を取れます。最大需要を想定した物理設備を先に購入する方式と比べ、需要変動へ合わせやすい点がクラウドの特徴です。

**誤答理由:**
- B: 最大需要向け設備を先行購入する考え方は、問題の「初期購入を避けたい」という要件と逆です。
- C: 需要変動に応じた利用というクラウドの利点を活かしません。
- D: 従量性という要件を満たしません。

**試験で見分けるポイント:** 「使った分」「需要変動」「事前の大型設備投資を避ける」はconsumption-based modelを示す語です。

**対応skill:** Describe cloud computing / consumption-based model and cloud pricing models  
**公式根拠:** https://learn.microsoft.com/en-us/training/modules/describe-cloud-compute/

## Q4. Scalability

Webアプリケーションのアクセス増加に対応するため、同じ構成のアプリケーションインスタンスを2台から6台へ増やします。この操作はどれに該当しますか。

A. Scale up  
B. Scale down  
C. Scale out  
D. Scale in

**正解: C**

**解説:** インスタンス数を増やして処理能力を拡張するのはscale out（水平スケール）です。個々のマシンのCPUやメモリを増強するscale up（垂直スケール）とは異なります。

**誤答理由:**
- A: scale upは通常、単一リソースのCPU・メモリなどをより大きな構成へ変更することです。
- B: scale downは単一リソースの能力を小さくする方向です。
- D: scale inはインスタンス数を減らす方向です。

**試験で見分けるポイント:** 台数を増減するならout/in、個々の能力を上下させるならup/downと整理します。

**対応skill:** Describe the benefits of using cloud services / scalability  
**公式根拠:** https://learn.microsoft.com/en-us/training/modules/describe-benefits-use-cloud-services/

## Q5. Cloud service type

開発チームはWebアプリケーションのコード開発に集中したく、基盤となるOSのパッチ適用やランタイム基盤の管理をできるだけクラウドプロバイダーに任せたいと考えています。一方、完成済み業務アプリをそのまま利用するのではなく、自社アプリケーションを開発・配置します。最も適したサービス種別はどれですか。

A. IaaS  
B. PaaS  
C. SaaS  
D. Private cloud

**正解: B**

**解説:** PaaSはアプリケーション開発・配置に必要なプラットフォームを提供し、開発者がOSなどの基盤管理よりアプリケーションコードへ集中しやすくします。

**誤答理由:**
- A: IaaSでは顧客がVMのOSなど、より多くの管理責任を負います。
- C: SaaSは完成済みアプリケーションをサービスとして利用する形態であり、自社アプリを開発・配置する今回の要件とは異なります。
- D: Private cloudはクラウド配置モデルであり、IaaS/PaaS/SaaSというサービス種別の回答ではありません。

**試験で見分けるポイント:** 「自社コードは作るがOS管理を減らしたい」はPaaS、「OSまで管理したい」はIaaS、「完成済みアプリを使う」はSaaSが基本です。

**対応skill:** Describe cloud service types / PaaS and appropriate use cases  
**公式根拠:** https://learn.microsoft.com/en-us/training/modules/describe-cloud-service-types/

## Coverage

| Question | Skill group | 主論点 |
| --- | --- | --- |
| Q1 | Describe cloud computing | Shared responsibility |
| Q2 | Describe cloud computing | Public/private/hybrid |
| Q3 | Describe cloud computing | Consumption-based model |
| Q4 | Benefits of cloud services | Scalability |
| Q5 | Cloud service types | PaaS / IaaS / SaaS |

次回は未カバーまたは薄いDomain 1論点（serverless、high availability/reliability/predictability、security/governance/manageability、IaaS/SaaS use case）を優先します。
