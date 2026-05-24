"""Sweep nhiều YAML config liên tiếp.

Usage:
    python -m scripts.sweep --configs experiments/configs/B*.yaml
"""
import argparse
import glob
import subprocess
import sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--configs", nargs="+", required=True,
                    help="glob patterns hoặc đường dẫn YAML")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    files = []
    for pat in args.configs:
        files.extend(sorted(glob.glob(pat)))
    files = [f for f in files if f.endswith(".yaml")]
    print(f"Sweep over {len(files)} configs")
    for f in files:
        cmd = [sys.executable, "-m", "scripts.run_experiment", "--config", f]
        if args.quiet:
            cmd.append("--quiet")
        print(f"\n>>> {f}")
        r = subprocess.run(cmd, cwd=str(Path(__file__).resolve().parent.parent))
        if r.returncode != 0:
            print(f"!!! Failed: {f} (exit {r.returncode})")


if __name__ == "__main__":
    main()
