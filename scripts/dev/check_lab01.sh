#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../.." && pwd)"
TMP_ROOT="${REPO_ROOT}/.tmp/stage2"
LOG_DIR="${TMP_ROOT}/logs"

bash "${SCRIPT_DIR}/bringup_lab01.sh"
mkdir -p "${LOG_DIR}"

(
  cd "${REPO_ROOT}"
  make validate | tee "${LOG_DIR}/make-validate.log"
  mkdir -p "${LOG_DIR}"
  ./cli-tools/mobile-systems-lab compare LAB_01_SENSOR_TOGGLE_APP | tee "${LOG_DIR}/compare-lab01.log"
  ./cli-tools/mobile-systems-lab generate artifacts/spec-examples/LAB_01_SENSOR_TOGGLE_APP.spec.v2.json --dry-run \
    | tee "${LOG_DIR}/generate-dry-run-check.log"
)

echo "check ok: LAB_01_SENSOR_TOGGLE_APP"
