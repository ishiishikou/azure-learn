# AZ-900 一周復習ノート

2026-09-25 の AZ-900 受験に向けて、学習チャットで扱った内容を「後から短時間で思い出せる」形に整理した復習ノートです。

> このノートは学習用の要約です。Microsoft Learn の公式 Study Guide と内容が食い違う場合は公式情報を優先してください。

## 読む順番

1. [Cloud Concepts](./01-cloud-concepts.md)
2. [Azure Architecture](./02-architecture.md)
3. [Compute](./03-compute.md)
4. [Network](./04-network.md)
5. [Storage](./05-storage.md)
6. [Identity & Security](./06-identity-security.md)
7. [Management & Governance](./07-management-governance.md)

## 最終復習で特に区別したい組み合わせ

| 迷いやすい組み合わせ | 覚え方 |
|---|---|
| Authentication / Authorization | 誰なのか / 何をしてよいか |
| Entra ID / Azure RBAC | ID・認証 / Azure Resourceへの権限 |
| RBAC / Policy / Lock / Tag | 誰ができる / 何を許す / 消させない / 分類 |
| Availability Zone / Availability Set | データセンター群の分離 / VMの障害・更新ドメイン分散 |
| VM Scale Sets / Availability Set | 台数を増減 / 一緒に落ちにくくする |
| Service Endpoint / Private Endpoint | 公開エンドポイントをVNetから安全に利用 / VNet内にPrivate IPを作る |
| LRS / ZRS / GRS / GZRS | ローカル / ゾーン / 地理 / ゾーン+地理 |
| Monitor / Service Health / Advisor | 自分のResource監視 / Azure側の状態 / 改善提案 |
| Pricing Calculator / Cost Management | 利用前の見積もり / 利用後のコスト管理 |
| Zero Trust / Defense in Depth | 信用せず検証 / 防御を多層化 |

## 学習上の扱い

本文中の「補足」は、AZ-900の用語理解を超えて会話で深掘りした内容です。試験直前は本筋を優先し、補足は余裕があるときだけ確認します。
