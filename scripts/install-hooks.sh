#!/usr/bin/env bash
# Install repo git hooks. Run once after cloning: ./scripts/install-hooks.sh
set -euo pipefail
root=$(git rev-parse --show-toplevel)
ln -sf ../../scripts/strip-image-metadata.sh "$root/.git/hooks/pre-commit"
chmod +x "$root/scripts/strip-image-metadata.sh"
echo "Installed pre-commit hook (image metadata stripping)."
