#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
command -v codex >/dev/null || { echo "Codex CLIが見つかりません" >&2; exit 1; }
codex login status || { echo "Codex CLIのサインインが必要です。codex login --device-auth を実行してください。" >&2; exit 1; }
MODEL_OPT=()
if [[ -n "${CODEX_MODEL:-}" ]]; then MODEL_OPT=(-m "$CODEX_MODEL"); fi
echo "読み取り専用の独立レビューを開始します。Azure操作やファイル変更は行いません。"
codex -a never exec --sandbox read-only --skip-git-repo-check --ephemeral -C "$PWD" "${MODEL_OPT[@]}" -o /tmp/azure-firewall-review-last-message.md "$(cat REVIEW.md)"
echo "レビュー結果: /tmp/azure-firewall-review-last-message.md"
