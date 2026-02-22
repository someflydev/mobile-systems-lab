#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../.." && pwd)"
TMP_ROOT="${REPO_ROOT}/.tmp/stage2"

case "${TMP_ROOT}" in
  "${REPO_ROOT}/.tmp/stage2") ;;
  *)
    echo "unsafe temp root: ${TMP_ROOT}" >&2
    exit 1
    ;;
esac

if [ -e "${TMP_ROOT}" ]; then
  rm -rf "${TMP_ROOT}"
fi
rmdir "${REPO_ROOT}/.tmp" 2>/dev/null || true

echo "teardown ok: ${TMP_ROOT}"
