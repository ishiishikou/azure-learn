#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
if ! command -v az >/dev/null 2>&1; then
  echo "Azure CLIがありません。先にAzure CLIをインストールしてください。" >&2
  exit 1
fi
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
.venv/bin/python -m pip install -q -r requirements.txt
.venv/bin/python build_notebook.py
echo "Listening at http://${VOILA_IP:-127.0.0.1}:${VOILA_PORT:-8866}"
exec .venv/bin/voila mobile_dashboard.ipynb --no-browser --Voila.ip="${VOILA_IP:-127.0.0.1}" --Voila.port="${VOILA_PORT:-8866}" --Voila.root_dir="$(pwd)"