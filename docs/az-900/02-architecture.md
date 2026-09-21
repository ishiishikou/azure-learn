# 02. Azure Architecture

## Region

Azureの地理的な提供単位です。例としてJapan East、Japan Westがあります。

Resourceを作るとき、多くのサービスではRegionを選択します。

## Availability Zone

1つのRegion内にある、物理的に分離されたデータセンター群です。

~~~text
Japan East
├─ Zone 1
├─ Zone 2
└─ Zone 3
~~~

Zoneを分けてResourceを配置すると、1つのデータセンター群の障害に耐えやすくなります。

## Region Pair

一部のAzure Regionには、地理的に離れたペアRegionがあります。Japan EastとJapan Westが代表例です。

注意点:

- Region Pairだから、すべてのResourceが自動的に複製されるわけではない。
- サービスごとにGeo冗長化やDR機能を設定する必要がある。
- Geoレプリケーションはサービスによって非同期の場合がある。

## Sovereign Region

政府・法規制など特別な要件向けに、通常のAzureとは分離された環境です。

AZ-900では「法令・政府要件のために分離されたAzure環境」と理解すれば十分です。

## Availability Set

主にVMをFault Domain / Update Domainへ分散し、同時停止のリスクを下げる仕組みです。

~~~text
Availability Zone
  → 物理的なZoneを分ける

Availability Set
  → VMを障害・更新単位に分散する
~~~

Availability SetはVMの台数を増やす機能ではありません。

## Management hierarchy

~~~text
Management Group
      ↓
Subscription
      ↓
Resource Group
      ↓
Resource
~~~

### Management Group

複数SubscriptionをまとめてPolicyやアクセス管理を適用するための上位単位です。

### Subscription

Azure利用の主要な課金・アクセス管理・Quotaの境界です。

開発・テスト・本番をどこまでSubscriptionで分けるかは、課金、権限、Policy、Quota、隔離要件によって決めます。

### Resource Group

関連するResourceをまとめる論理コンテナです。

重要:

- Resource Groupは入れ子にできない。
- 1つのResourceは同時に1つのResource Groupへ所属する。
- Resource Group自身にもRegionがあるが、これは主にResource Groupのメタデータを保持する場所。
- Resource Group内の各Resourceは、Resource Groupとは異なるRegionに置ける場合がある。

### Resource

VM、Storage Account、VNetなど、実際に作成して利用するAzureサービスの実体です。

## Scope inheritance

RBACやPolicyは上位Scopeに設定すると、原則として下位へ影響します。

~~~text
Subscription
  └─ Resource Group
       └─ Resource
~~~

SubscriptionにReaderを割り当てれば、その配下を広く閲覧できる、といった考え方です。

## 一問一答

| キーワード | 答え |
|---|---|
| 複数Subscriptionをまとめる | Management Group |
| 課金・Quota・アクセス管理の主要境界 | Subscription |
| 関連Resourceを論理的にまとめる | Resource Group |
| Region内の物理分離 | Availability Zone |
| VMをFault/Update Domainへ分散 | Availability Set |
| 特殊な法規制・政府向け環境 | Sovereign Region |
