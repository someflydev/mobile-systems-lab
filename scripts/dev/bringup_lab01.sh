#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../.." && pwd)"
TMP_ROOT="${REPO_ROOT}/.tmp/stage2"
LOG_DIR="${TMP_ROOT}/logs"

bash "${SCRIPT_DIR}/doctor.sh"

mkdir -p "${LOG_DIR}" "${TMP_ROOT}/generated"
date -u +"%Y-%m-%dT%H:%M:%SZ" > "${TMP_ROOT}/session-start.txt"

(
  cd "${REPO_ROOT}"
  ./cli-tools/mobile-systems-lab --help > "${LOG_DIR}/cli-help.log"
  ./cli-tools/mobile-systems-lab generate artifacts/spec-examples/LAB_01_SENSOR_TOGGLE_APP.spec.v2.json --dry-run \
    > "${LOG_DIR}/generate-dry-run.log"
)

echo "bringup ok: ${TMP_ROOT}"
