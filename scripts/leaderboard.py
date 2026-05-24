"""Bảng xếp hạng từ experiments/log.csv.

Usage:
    python -m scripts.leaderboard --top 10
    python -m scripts.leaderboard --phase B
"""
import argparse
import csv
from pathlib import Path

LOG = Path(__file__).resolve().parent.parent / "experiments" / "log.csv"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", default=None)
    ap.add_argument("--top", type=int, default=20)
    args = ap.parse_args()
    if not LOG.exists():
        print("No log yet"); return
    rows = list(csv.DictReader(open(LOG)))
    if args.phase:
        rows = [r for r in rows if r["phase"] == args.phase]
    def f1(r):
        try: return float(r["mean_macroF1"])
        except: return -1.0
    rows.sort(key=f1, reverse=True)
    print(f"{'#':>3} {'phase':<6} {'name':<32} {'F1':>7} {'±':>7} {'runtime':>9}  notes")
    print("-" * 90)
    for i, r in enumerate(rows[:args.top], 1):
        print(f"{i:>3} {r['phase']:<6} {r['name'][:32]:<32} "
              f"{r['mean_macroF1']:>7} {r['std_macroF1']:>7} "
              f"{r['runtime_sec']:>9}  {r['notes'][:40]}")


if __name__ == "__main__":
    main()
