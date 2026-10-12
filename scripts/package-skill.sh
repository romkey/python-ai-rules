#!/bin/sh
# Packages this repo as an Agent Skill: a zip holding one python-ai-rules/
# folder with SKILL.md at its top, for uploading to Claude or any tool that
# reads Agent Skills. Packs the committed tree (HEAD), not local edits.
#
#   scripts/package-skill.sh [OUTPUT.zip]    # default python-ai-rules-skill.zip
#
# The release workflow attaches it to every GitHub Release.
set -eu
out=${1:-python-ai-rules-skill.zip}
cd "$(dirname "$0")/.."
git archive --format=zip --prefix=python-ai-rules/ -o "$out" HEAD \
  SKILL.md RULES.md UPGRADING.md LICENSE docs skills templates
echo "$out"
