# azure-learn

Azure資格の学習記録・復習ノート・問題集を管理するリポジトリ。

## Issue運用

- [#1 AZ-900 学習進捗](../../issues/1) — 2026-09-25受験向けの学習進捗
- [#2 Azure資格問題集の収集・最新化ルール](../../issues/2) — 全資格共通の問題収集・公式情報照合・解説品質ルール
- [#3 Azure資格コンプリート向け問題集整備](../../issues/3) — Microsoft LearnのAzure資格一覧と資格別Question Bank Issueを管理するMaster

## 問題集の継続整備

資格別の問題集作成は #3 から各子Issueへ分割する。
共有Scheduled Workerでは `service_class: background` / `dispatch_policy: idle_only` として扱い、他リポジトリを含む実行可能な通常作業がない場合だけ進める。

問題の正誤やAzure仕様は最新のMicrosoft Learn / Azure公式ドキュメントで検証し、詳細ルールは #2 を正本とする。
