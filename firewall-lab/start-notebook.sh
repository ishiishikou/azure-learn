#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
if ! command -v az >/dev/null 2>&1; then
  echo "Azure CLI が必要です。先にインストールしてください。" >&2
  exit 1
fi
if [ ! -d .venv ]; then python3 -m venv .venv; fi
.venv/bin/python -m pip install -q -r requirements.txt
.venv/bin/python build_notebook.py
echo "JupyterLabはローカルの127.0.0.1で待ち受けます。ログイン用トークン付きURLを確認してください。"
exec .venv/bin/jupyter lab --allow-root --no-browser --ip=127.0.0.1 --port="${JUPYTER_PORT:-8888}" --ServerApp.root_dir="$(pwd)"