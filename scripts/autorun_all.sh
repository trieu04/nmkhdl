#!/usr/bin/env bash
# autorun_all.sh - Chạy chuỗi Phase D -> E -> G sau khi C07 xong.
# Có thể treo máy chạy qua đêm.

set -u
cd "$(dirname "$0")/.."
PY=venv/bin/python
LOGDIR=experiments/logs
mkdir -p "$LOGDIR"

echo "[autorun] $(date)  ==== START ===="

# --- Wait for any currently-running run_experiment process ---
echo "[autorun] waiting for any in-flight run_experiment (e.g., C07)..."
while pgrep -f "scripts.run_experiment" > /dev/null; do
  sleep 30
done
echo "[autorun] $(date)  no in-flight runs, proceeding."

# --- Leaderboard at end of C ---
echo "[autorun] === Leaderboard Phase C ==="
$PY -m scripts.leaderboard --phase C --top 10 | tee "$LOGDIR/leaderboard_C.txt" || true

run_phase() {
  local PHASE="$1"
  local GLOB="$2"
  echo "[autorun] $(date) === Phase $PHASE start ==="
  for CFG in $GLOB; do
    NAME=$(basename "$CFG" .yaml)
    echo "[autorun] $(date) -- running $NAME --"
    $PY -m scripts.run_experiment --config "$CFG" \
        2>&1 | tee "$LOGDIR/phase${PHASE}_${NAME}.log"
    echo "[autorun] $(date) -- finished $NAME --"
  done
  echo "[autorun] === Leaderboard Phase $PHASE ==="
  $PY -m scripts.leaderboard --phase "$PHASE" --top 10 \
      | tee "$LOGDIR/leaderboard_${PHASE}.txt" || true
}

run_phase D "experiments/configs/D??_*.yaml"
run_phase E "experiments/configs/E??_*.yaml"
run_phase G "experiments/configs/G??_*.yaml"

echo "[autorun] $(date)  ==== ALL PHASES DONE ===="
echo "[autorun] final overall leaderboard:"
$PY -m scripts.leaderboard --top 20 | tee "$LOGDIR/leaderboard_FINAL.txt" || true
