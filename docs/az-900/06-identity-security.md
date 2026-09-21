# 06. Identity & Security

## Microsoft Entra ID

旧Azure Active Directoryです。

User、Group、Application、Sign-inなどを扱うCloud Identity Platformです。

~~~text
Microsoft Entra ID
├─ Azure
├─ Microsoft 365
├─ SaaS
└─ Custom App
~~~

Azure専用のUser Directoryではありません。

## Microsoft Entra Domain Services

従来型Active Directory Domain Servicesに近い機能をManaged Serviceとして提供します。

代表的な機能:

- Domain Join
- LDAP
- Kerberos
- NTLM
- Group Policy

~~~text
Entra ID
   ↓
Entra Domain Services
   ↓
Domain JoinしたVM
~~~

覚え方:

- Entra ID = Cloud Identity。
- Entra Domain Services = Legacy AD互換機能をManagedに提供。

## Authentication / Authorization

~~~text
Authentication
→ あなたは誰？

Authorization
→ 何をしてよい？
~~~

認証してIdentityを確認し、その後にRBACなどでAuthorizationを判断します。

## SSO

Single Sign-On。

一度Sign-inすれば、複数Applicationへ再度Credentialを入力せずAccessしやすくする仕組みです。

## MFA

Multi-Factor Authentication。

異なる種類の認証要素を組み合わせます。

- Knowledge: Passwordなど。
- Possession: Smartphone / Security Keyなど。
- Inherence: Face / Fingerprintなど。

Password + Authenticator承認は代表例です。

## Passwordless

Passwordに依存せずSign-inする方法です。

例:

- Windows Hello。
- Microsoft Authenticator。
- FIDO2 Security Key。

~~~text
MFA
→ 複数要素

Passwordless
→ Password自体を使わない
~~~

## Conditional Access

条件に応じてAccess判断を行う仕組みです。

~~~text
IF
  海外からSign-in

THEN
  MFAを要求
~~~

ConditionとしてUser、Location、Device、Riskなどを利用し、Allow / Block / MFA Requirementなどにつなげます。

覚え方:

- MFA = 認証方法。
- Conditional Access = どの状況で何を要求するかというRule。

## Azure RBAC

Role-Based Access Control。

Azure Resourceに対して「誰が何をできるか」を管理します。

代表Role:

- Owner: Resource管理 + Access管理。
- Contributor: Resourceを管理できるが、Access管理は基本不可。
- Reader: Read only。

Scope:

~~~text
Management Group
   ↓
Subscription
   ↓
Resource Group
   ↓
Resource
~~~

## Entra Role / Azure RBAC Role

~~~text
Entra Role
→ User / Group / ApplicationなどIdentity Platformを管理

Azure RBAC Role
→ VM / StorageなどAzure Resourceを管理
~~~

Global AdministratorやUser AdministratorはEntra Role、Owner / Contributor / ReaderはAzure RBAC Roleです。

## Managed Identity

Azure Resource自身にEntra IDのIdentityを持たせます。

~~~text
VM
 ↓ Managed Identity
Entra ID
 ↓ Authentication
Storage
 ↓ RBAC
Access
~~~

PasswordやClient SecretをApplicationへ埋め込まず、AzureにCredential Lifecycleを管理させられます。

- System-assigned: ResourceとLifecycleが連動。
- User-assigned: Resourceから独立し、複数Resourceでも利用可能。

覚え方:

~~~text
Managed Identity
→ 誰なのか

RBAC
→ 何をしてよいか
~~~

## External Identities

自社外のUserと安全に協業したり、Customer向けIdentityを扱う仕組みです。

B2B CollaborationではPartnerをGuestとして招待し、相手側Identityを利用して自社ResourceへAccessさせられます。

## Zero Trust

Service名ではなくSecurity Principleです。

3つの中心原則:

- Verify explicitly。
- Use least privilege access。
- Assume breach。

~~~text
社内Networkだから信用
        ×

User / Device / Contextを確認
        ○
~~~

MFA、Conditional Access、RBAC、Network Segmentationなどが実装要素になります。

## Defense in Depth

1つの防御が破られても次のLayerで防ぐ、多層防御の考え方です。

~~~text
Internet
  ↓
WAF
  ↓
Network Control
  ↓
Identity
  ↓
Authorization
  ↓
Data Encryption
~~~

~~~text
Zero Trust
→ 信用せず検証する考え方

Defense in Depth
→ 防御を何層も重ねる考え方
~~~

## Microsoft Defender for Cloud

AzureなどのCloud EnvironmentのSecurity PostureとWorkload Protectionを扱います。

代表イメージ:

- Secure Score。
- Security Recommendations。
- Regulatory Compliance。
- Servers / Storage / Databases / ContainersなどのProtection。

~~~text
Azure Environment
      ↓
Defender for Cloud
      ↓
「この設定を改善してください」
「この脅威を検出しました」
~~~

## 一問一答

| キーワード | 答え |
|---|---|
| Cloud Identity | Microsoft Entra ID |
| LDAP/Kerberos/Domain JoinをManaged化 | Entra Domain Services |
| 1回のSign-inで複数App | SSO |
| 複数種類の認証要素 | MFA |
| Passwordなし | Passwordless |
| 場所・DeviceなどでAccess条件を変える | Conditional Access |
| Azure Resource権限 | Azure RBAC |
| Azure ResourceへIdentityを付与 | Managed Identity |
| 外部Partner/Customer Identity | External Identities |
| 信用せず毎回検証 | Zero Trust |
| 多層防御 | Defense in Depth |
| Cloud Security Posture / Threat Protection | Defender for Cloud |
