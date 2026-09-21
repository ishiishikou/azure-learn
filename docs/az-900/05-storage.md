# 05. Storage

## Storage Account

Blob、Files、Queue、TableなどのAzure Storage Serviceをまとめる基本Resourceです。

一般的にはGeneral-purpose v2 Storage Accountを利用します。

## Blob Storage

Object Storageです。画像、動画、ログ、バックアップ、非構造化データなどに向きます。

AWSで言えばS3に近い位置づけです。

## Azure Files

SMB / NFSなどで利用できるManaged File Shareです。

## Azure Disk Storage

主にVMのBlock Storageです。実際のVM Disk ResourceとしてManaged Diskを利用します。

AZ-900では「Disk Storage = VM用のManaged Disk」とほぼ同じ感覚で構いません。

## Queue Storage

非同期処理で使うMessage Queueです。

~~~text
Producer
   ↓
Queue
   ↓
Consumer
~~~

## Table Storage

Key/Attribute型のシンプルなNoSQL Storeです。

## Blob Access Tiers

| Tier | イメージ |
|---|---|
| Hot | 頻繁にアクセス |
| Cool | アクセス頻度が低い |
| Cold | さらに低頻度 |
| Archive | 長期保管、取り出し制約が大きい |

保管料金とAccess/取り出しCostのTrade-offがあります。

## Redundancy

### LRS

Locally Redundant Storage。

同一Primary Region内の1つの物理Locationで複数Copyを保持します。

### ZRS

Zone-Redundant Storage。

Primary Region内の複数Availability Zoneへ同期的に複製します。

~~~text
Region
├─ Zone 1
├─ Zone 2
└─ Zone 3
~~~

### GRS

Geo-Redundant Storage。

Primary RegionからSecondary RegionへGeo Replicationします。Secondaryへの複製は非同期なので、突然のRegion障害では直近Dataを失う可能性があります。

Primary側はLRS構成です。

### GZRS

Geo-Zone-Redundant Storage。

Primary RegionはZRS、さらにSecondary RegionへGeo Replicationします。

~~~text
Primary Region
  ZRS
   |
   | Async
   v
Secondary Region
~~~

### RA-GRS / RA-GZRS

RA = Read Access。

Failover前でもSecondary ReplicaをReadできる構成です。Write先はPrimaryです。

## AWS S3との感覚差

AWS S3 Standardは複数AZへ自動的に分散されるため、冗長性だけ見ればAzure Blob + ZRSに近い感覚です。

GZRSは、それに加えてSecondary RegionへのGeo Replicationを持つイメージです。

完全な1対1対応ではないので、概念比較として利用します。

## AzCopy

Azure StorageとのData Copyに使うCLIです。

~~~text
Local
  ↓ AzCopy
Blob / Azure Files
~~~

VM上でAzCopyを実行し、BlobからVM File SystemへDownloadすることもできます。

通常のファイルを「Managed Disk Resourceへ直接AzCopyする」と考えるのではなく、VM OS上のFile SystemへCopyすると考えます。

## Azure Storage Explorer

Azure StorageをGUIで操作するToolです。

## Azure File Sync

Windows ServerのFile ServerとAzure Filesを同期します。Cloud Tieringも利用できます。

## Azure Migrate

Server、VM、WorkloadなどのAzure移行を評価・支援します。

## Azure Data Box

大量DataをNetwork転送するのが現実的でない場合に、Physical Deviceを利用してAzureへTransferします。

~~~text
Azure Migrate
→ System / Serverの移行

Azure Data Box
→ 大量Dataの物理転送
~~~

## 一問一答

| 要件 | 答え |
|---|---|
| Object Storage | Blob |
| SMB/NFS File Share | Azure Files |
| VM Disk | Disk Storage / Managed Disk |
| Message Queue | Queue Storage |
| Simple NoSQL | Table Storage |
| 1 Location内で冗長化 | LRS |
| AZ間で冗長化 | ZRS |
| Secondary Regionへ複製 | GRS |
| ZRS + Secondary Region | GZRS |
| CLIでStorageへCopy | AzCopy |
| GUIでStorage操作 | Storage Explorer |
| File ServerとAzure Files同期 | Azure File Sync |
| Server/Workload移行 | Azure Migrate |
| 大量Dataを物理Deviceで移行 | Data Box |
