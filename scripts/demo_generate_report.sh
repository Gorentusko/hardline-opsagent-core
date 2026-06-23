#!/usr/bin/env bash
set -euo pipefail

echo "=== Hardline OpsAgent Core demo ==="
curl -s http://localhost:8088/health | python3 -m json.tool
echo
curl -s http://localhost:8088/analyze | python3 -m json.tool
echo
echo "Reports:"
ls -lah data/reports || true
