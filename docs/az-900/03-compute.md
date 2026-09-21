# 03. Compute

## Virtual Machines

Azure VMはIaaSです。

Azureは物理サーバーなどを管理しますが、利用者はOS、ミドルウェア、アプリケーション、OSパッチなどを管理します。

VMの代表的な構成要素:

- VM Size: CPU・Memoryなど。
- OS Image。
- Managed Disk。
- NIC。
- VNet / Subnet。
- 必要に応じてPublic IP。

Public IPは必須ではありません。

## VM Scale Sets

似た構成のVMを複数台まとめて管理し、台数をScale out / inできる仕組みです。

~~~text
負荷増加
  ↓
VM 2台 → 5台
~~~

覚え方:

- Scale Sets = 台数を増減。
- Availability Set = 一緒に止まりにくくする。

## Containers

コンテナはアプリと依存関係をまとめてパッケージ化します。VMより軽量で、OS全体を各アプリ用に持つ必要がありません。

### Azure Container Instances

比較的シンプルにコンテナを実行したい場合のサービスです。

### Azure Container Apps

コンテナアプリをマネージドに実行し、HTTP、イベント、スケーリングなどを扱いやすくしたPaaS寄りのサービスです。

補足: FunctionsをContainer Apps環境で動作させる構成もありますが、AZ-900では「FunctionsとContainer Appsは目的が違う」と理解できれば十分です。

## Azure Functions

イベント駆動型のServerless Computeです。

~~~text
HTTP Request
Queue Message
Timer
Event
   ↓
Function実行
~~~

利用者は主にコードや設定を管理し、OS管理やサーバー台数管理を大きく減らせます。

「短い処理しかできない」という意味ではなく、中心概念はイベントによってコードを実行することです。

## App Service

WebアプリやWeb APIをホストするPaaSです。

~~~text
User
 ↓ HTTPS
App Service
 ↓
Web App / API
~~~

OSやWeb Serverの管理負担をVMより減らせます。

App ServiceにはAzure管理の既定ホスト名があり、既定URLでHTTPSを利用できます。そのため「HTTPSにしたいだけ」でFront Doorが必須になるわけではありません。

## Azure Virtual Desktop

Azure上からWindows Desktopやアプリケーションをユーザーへ配信するサービスです。

Webサーバーをホストするためのサービスではなく「ユーザーにDesktop環境を提供する」ものです。

## 使い分け

| 要件 | 選択 |
|---|---|
| OSまで自由に管理 | VM |
| 同じVM群を自動スケール | VM Scale Sets |
| VM障害を分散 | Availability Set |
| アプリ + 依存関係をパッケージ化 | Container |
| Web App/APIをPaaSで公開 | App Service |
| イベントでコード実行 | Functions |
| Windows Desktopをユーザーへ配信 | Azure Virtual Desktop |

## 補足: Front Door + WAF + Web backend

会話で深掘りした構成です。

~~~text
Internet
   ↓ HTTPS
Azure Front Door
   └─ WAF Policy
        ↓
 App Service / VM
~~~

Front DoorはHTTPSのためだけの機能ではなく、Global Layer 7 Routing、WAF、CDN/Edge、複数Regionへのルーティングなどを担います。

App ServiceへWAF Policyを直接付けるのではなく、Front DoorまたはApplication Gateway側でWAFを適用します。

VMを使う必然性がなく、Webアプリを公開したいだけなら、VMよりApp Serviceの方がOS管理を減らせる場合があります。

## 補足: Serverless GPU

GPU推論ではScale-to-zeroが常に最適とは限りません。GPU割り当て、Container起動、Runtime起動、モデルロードに時間がかかるためです。

これはAZ-900範囲外ですが、「Serverless = 常に瞬時に0→1」ではないことを理解する例として残します。
