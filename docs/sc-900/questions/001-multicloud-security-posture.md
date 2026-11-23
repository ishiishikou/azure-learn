---
id: SC900-Q001
exam: SC-900
status: original
review: user_approved
approved_on: 2026-11-23
verified_on: 2026-11-23
difficulty: fundamental
type: single_choice
domain: Microsoft セキュリティ ソリューションの機能について説明する
skill: Azure のセキュリティ管理機能について説明する
topic: Microsoft Defender for Cloud / CSPM / Secure Score / regulatory compliance
answer: C
source_type: original_question
---

# SC-900 第1問：マルチクラウド環境のセキュリティ態勢管理

## 問題

ある企業では、AzureとAWSの両方でクラウドリソースを運用しています。セキュリティ担当者は、以下の要件を満たしたいと考えています。

- リソースの構成上のセキュリティリスクを継続的に評価する。
- セキュリティスコアで改善状況を把握する。
- セキュリティ基準への準拠状況を確認する。

**この要件に最も適したソリューションはどれですか？**

A. Microsoft Sentinel  
B. Microsoft Entra ID  
C. Microsoft Defender for Cloud  
D. Azure Key Vault  

## 正解

**C. Microsoft Defender for Cloud**

## 解説

Microsoft Defender for Cloudは、AzureやAWSなどのマルチクラウド環境を対象に、クラウド セキュリティ態勢管理（CSPM）を提供します。セキュリティ構成を評価して推奨事項を提示し、Secure Scoreで態勢を可視化し、規制コンプライアンス ダッシュボードでセキュリティ基準への準拠状況を確認できます。

Microsoft Learnの機能説明によれば、CSPMの基本機能は無料でも利用できる一方、高度な規制コンプライアンス等の一部機能には有料プランなどの条件があります。また、すべての準拠事項が自動評価されるわけではなく、サービスが法令準拠を保証するものでもありません。

### 他の選択肢

- **A. Microsoft Sentinel**：SIEM/SOARとしてログやイベントを収集・分析し、脅威の検出・調査・対応を支援します。継続監視は可能ですが、クラウド構成のセキュリティ態勢評価とSecure Scoreが主目的ではありません。
- **B. Microsoft Entra ID**：認証、認可、ユーザー/アプリケーションのIDとアクセスの管理が主目的です。
- **D. Azure Key Vault**：キー、シークレット、証明書の安全な保管・管理が主目的です。

## 試験で見分けるポイント

- クラウドの**構成リスク、推奨事項、Secure Score、規制コンプライアンス** → **Microsoft Defender for Cloud（CSPM）**
- セキュリティログ/イベントの**分析、脅威検出、インシデント対応** → **Microsoft Sentinel（SIEM/SOAR）**
- **認証、認可、アクセス管理** → **Microsoft Entra ID**
- **秘密鍵、シークレット、証明書の保管** → **Azure Key Vault**

## Microsoft Learn公式根拠

- SC-900 Study Guide（2026年10月21日時点のskills measured）：https://learn.microsoft.com/ja-jp/credentials/certifications/resources/study-guides/sc-900
- Defender for Cloud Overview（CSPM、マルチクラウド、Secure Score）：https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-cloud-introduction
- Secure score in Defender for Cloud：https://learn.microsoft.com/en-us/azure/defender-for-cloud/secure-score-security-controls
- Regulatory compliance in Defender for Cloud：https://learn.microsoft.com/en-us/azure/defender-for-cloud/concept-regulatory-compliance-standards
- Microsoft Sentinel SIEM：https://learn.microsoft.com/en-us/azure/sentinel/overview
- Microsoft Entra ID：https://learn.microsoft.com/en-us/entra/fundamentals/whatis
- Azure Key Vault：https://learn.microsoft.com/en-us/azure/key-vault/general/overview

## 出題・レビュー履歴

- 2026-11-23：ChatGPTによる独自作成問題を出題。ユーザーがCと回答し、正答・解説を確認したうえで採用・GitHub登録・Muse共有を明示承認。
- 問題品質：基礎問題として適切。消去法で解きやすいため難易度は低め。
