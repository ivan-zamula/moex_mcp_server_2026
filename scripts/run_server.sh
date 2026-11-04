#!/usr/bin/env bash
set -euo pipefail

if [[ -x ".venv/bin/python" ]]; then
    PYTHON_BIN=".venv/bin/python"
else
    PYTHON_BIN="python"
fi

PYTHONPATH=src "$PYTHON_BIN" -m mcp_server.mcp_app
