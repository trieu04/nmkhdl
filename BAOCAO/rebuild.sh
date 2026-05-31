#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Clean LaTeX temporary files from previous runs.
rm -f bao_cao.aux bao_cao.log bao_cao.out bao_cao.toc

# Build PDF (run twice to stabilize references/table of contents).
pdflatex -interaction=nonstopmode -halt-on-error bao_cao.tex >/dev/null
pdflatex -interaction=nonstopmode -halt-on-error bao_cao.tex >/dev/null

echo "Done: generated bao_cao.pdf"
