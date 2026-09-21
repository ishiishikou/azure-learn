# 01. Cloud Concepts

この章はAZ-900の土台です。細かい製品名より「クラウドを使うと責任・コスト・拡張性がどう変わるか」を説明できることを重視します。

## Shared Responsibility Model

クラウドでは、Microsoftと利用者で責任を分担します。

- Microsoftは、物理データセンター、物理ネットワーク、物理ホストなどを管理する。
- 利用者は、データ、ID、アクセス権、アプリケーション設定などを管理する。
- IaaS / PaaS / SaaS の順に、Microsoft側が管理する範囲が増える。

覚え方:

~~~text
IaaS
  利用者がOSまで管理する

PaaS
  OSや実行基盤はAzureが管理し、利用者はアプリとデータ中心

SaaS
  完成したサービスを利用する
~~~

VMはIaaS、App ServiceやAzure SQL DatabaseはPaaS、Microsoft 365はSaaSの代表例です。

## Public / Private / Hybrid Cloud

### Public Cloud

Azureのように、クラウド事業者が提供する共有基盤を利用します。必要なResourceをオンデマンドで作りやすいのが特徴です。

### Private Cloud

1つの組織専用のクラウド環境です。専用性・統制を重視する場合に使われます。

### Hybrid Cloud

オンプレミスとPublic Cloudを組み合わせます。

~~~text
On-premises
     |
     | VPN / ExpressRoute など
     |
Azure
~~~

「すべてAzureへ移行する」のではなく、オンプレに残すシステムとAzureを連携させる構成もクラウド利用です。

## Consumption-based Model

クラウドでは、原則として使った量に応じて料金が発生する従量課金の考え方が中心です。

~~~text
必要な分だけ使う
      ↓
使用量に応じて支払う
~~~

ただし、予約やSavings Planなど、利用を約束して割引を受ける仕組みもあります。

## CapEx / OpEx

- CapEx: Capital Expenditure。サーバーなどを先に購入する設備投資。
- OpEx: Operational Expenditure。利用に応じて継続的に支払う運用費。

オンプレではCapExが大きくなりやすく、クラウドではOpEx中心へ寄せやすい、というのが基本的な理解です。

## Cloudの代表的なメリット

### High Availability

障害が起きてもサービスを継続しやすくする考え方です。Availability Zoneや冗長化とつながります。

### Scalability

負荷に合わせてResource量を増減できる性質です。

- Scale up/down: 1台の性能を上げる・下げる。
- Scale out/in: 台数を増やす・減らす。

### Elasticity

需要の増減に合わせて、Resourceを動的に伸縮させる性質です。Scalabilityより「需要に追随して増減する」ニュアンスが強いです。

### Reliability

障害が起きても回復・継続できるよう設計する性質です。複数Zone・複数Regionなどが関係します。

### Predictability

性能やコストを予測・管理しやすくする考え方です。Pricing Calculator、Cost Management、監視などにつながります。

### Security / Governance / Manageability

クラウドだから自動的に安全になるわけではありませんが、Entra ID、RBAC、Policy、Defender for Cloud、Monitorなど、統制・監視のためのマネージド機能を利用できます。

## SLA

SLAは Service Level Agreement。サービスの可用性などについて、Microsoftが示すサービスレベルの約束です。

重要なのは「SLAが100%なら絶対止まらない」と考えないことです。複数サービスを直列に組み合わせたシステムでは、システム全体の可用性は各要素の影響を受けます。

試験向けには次を押さえます。

- 可用性要件が高いほど、冗長化構成が重要。
- SLAを満たさなかった場合の扱いとしてService Creditが定められている場合がある。
- SLAとバックアップ、DR、可用性設計は同じものではない。

## 一問一答

| キーワード | 答え |
|---|---|
| OSまで自分で管理 | IaaS |
| OS管理を減らしてアプリに集中 | PaaS |
| 完成済みアプリを利用 | SaaS |
| オンプレ + Azure | Hybrid Cloud |
| 使用量に応じて支払う | Consumption-based model |
| 台数を増やす | Scale out |
| 需要に合わせて自動伸縮 | Elasticity |
| サービスレベルの約束 | SLA |
