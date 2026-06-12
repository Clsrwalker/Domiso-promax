#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

swift --version
swift test
swift build -c release

if [[ -n "${DOMISO_TOOLS_DIR:-}" ]]; then
  test -f "$DOMISO_TOOLS_DIR/domiso_generate_select.py"
else
  test -f "../tools/domiso_generate_select.py"
fi

echo "Domiso-macOS verification passed."
