"""Chạy một experiment từ YAML config.

Usage:
    python -m scripts.run_experiment --config experiments/configs/B01_baseline.yaml
"""
import argparse
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.train import run_cv


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    cfg_path = Path(args.config)
    with open(cfg_path) as f:
        cfg = yaml.safe_load(f)
    # default name from filename
    cfg.setdefault("name", cfg_path.stem)
    print(f"=== Running experiment: {cfg['name']} (phase {cfg.get('phase', 'X')}) ===")
    out = run_cv(cfg, verbose=not args.quiet)
    print(f"=== DONE  mean_F1={out['mean_macroF1']:.4f} ± {out['std_macroF1']:.4f}  "
          f"run_id={out['run_id']} ===")


if __name__ == "__main__":
    main()
