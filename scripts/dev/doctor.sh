#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../.." && pwd)"

require_cmd() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "missing required command: $cmd" >&2
    exit 1
  fi
}

require_cmd bash
require_cmd python3
require_cmd make

if command -v rg >/dev/null 2>&1; then
  echo "tool: rg (present)"
elif command -v grep >/dev/null 2>&1; then
  echo "tool: rg (missing, using grep fallback)"
else
  echo "missing required command: rg or grep" >&2
  exit 1
fi

test -f "${REPO_ROOT}/cli-tools/mobile-systems-lab"
test -f "${REPO_ROOT}/Makefile"
test -f "${REPO_ROOT}/artifacts/contracts/LAB_SPEC.v2.json"
test -f "${REPO_ROOT}/artifacts/spec-examples/LAB_01_SENSOR_TOGGLE_APP.spec.v2.json"

echo "doctor ok: ${REPO_ROOT}"
