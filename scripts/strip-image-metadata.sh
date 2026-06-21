#!/usr/bin/env bash
# Strip all metadata (EXIF/GPS/etc.) from staged image files before commit.
# Guarantees no privacy-intrusive metadata ever lands in git history.
# Installed as the repo's pre-commit hook (see scripts/install-hooks.sh).
set -euo pipefail

staged=$(git diff --cached --name-only --diff-filter=ACM \
  | grep -iE '\.(jpe?g|png|tiff?|webp)$' || true)

[ -z "$staged" ] && exit 0

if ! command -v exiftool >/dev/null 2>&1; then
  echo "pre-commit: exiftool not found; cannot verify image metadata is stripped." >&2
  echo "Install it (brew install exiftool) or unstage the images." >&2
  exit 1
fi

while IFS= read -r f; do
  [ -f "$f" ] || continue
  if [ -n "$(exiftool -s3 -all "$f" 2>/dev/null)" ]; then
    exiftool -all= -overwrite_original "$f" >/dev/null 2>&1
    git add "$f"
    echo "pre-commit: stripped metadata from $f"
  fi
done <<< "$staged"
