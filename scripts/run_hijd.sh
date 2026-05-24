#!/usr/bin/env bash
# run_hijd.sh - Run Phase H/I/J/L (RF features, fusion, open-set, report)
# Usage: bash scripts/run_hijd.sh

set -u
cd "$(dirname "$0")/.."
PY=venv/bin/python
LOGDIR=experiments/logs
mkdir -p "$LOGDIR"

BEST_RUN="20260518-012834_E_E03_rotation_only"  # E03_rotation_only winner

echo "[hijd] $(date) === START H/I/J/L ==="

# Phase H: RF on CNN features
echo "[hijd] === Phase H: RF features ==="
$PY -m scripts.train_rf_features --base-run "$BEST_RUN" \
    --n-forests 3 --n-estimators 300 \
    --notes "RF 300 trees on CNN logits from E03 winner" \
    2>&1 | tee "$LOGDIR/phase_H.log"

# Phase J: Open-set evaluation
echo "[hijd] === Phase J: Open-set AUROC ==="
$PY -m scripts.eval_openset --base-run "$BEST_RUN" \
    --notes "Softmax entropy open-set detection on E03" \
    2>&1 | tee "$LOGDIR/phase_J.log"

# Phase L: Final report
echo "[hijd] === Phase L: Final report ==="
$PY -m scripts.final_report 2>&1 | tee "$LOGDIR/phase_L.log"

echo "[hijd] $(date) === DONE ==="
echo "[hijd] Results logged to experiments/log.csv"
echo "[hijd] Final report: FINAL_REPORT.md"
