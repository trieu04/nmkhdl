#!/usr/bin/env python
"""Run the simplified RF + CNN experiment for the project report.

This script intentionally avoids the old sweep-style configs. It trains one
plain CNN 1D configuration and one Random Forest baseline, then writes a small
JSON summary under reports/simple_results.json.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import REPORTS_DIR
from src.evaluate import rf_baseline
from src.train import load_npz, run_cv, split_known_unknown


DEFAULT_CONFIG = Path("experiments/configs/SIMPLE_CNN.yaml")


def _load_known_labels():
    data = load_npz()
    X, y, activity, groups = (
        data["X"],
        data["y"],
        data["activity"],
        data["groups"],
    )
    Xk, yk, _actk, grk = split_known_unknown(X, y, activity, groups)
    classes = sorted(np.unique(yk).tolist())
    cls2id = {c: i for i, c in enumerate(classes)}
    yk_id = np.array([cls2id[v] for v in yk])
    return Xk, yk_id, grk, classes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--skip-cnn", action="store_true")
    parser.add_argument("--skip-rf", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    cfg_path = Path(args.config)
    with open(cfg_path) as f:
        cfg = yaml.safe_load(f)

    out_path = REPORTS_DIR / "simple_results.json"
    if out_path.exists() and (args.skip_cnn or args.skip_rf):
        with open(out_path) as f:
            results = json.load(f)
    else:
        results = {}

    results.update({
        "config": str(cfg_path),
        "method": "Simple baseline: CNN 1D + Random Forest",
    })

    if not args.skip_cnn:
        print("=== Train simple CNN 1D ===")
        results["cnn"] = run_cv(cfg, verbose=not args.quiet)

    if not args.skip_rf:
        print("\n=== Train Random Forest baseline ===")
        Xk, yk_id, grk, classes = _load_known_labels()
        results["rf"] = rf_baseline(
            Xk,
            yk_id,
            grk,
            n_splits=cfg.get("n_splits", 3),
        )
        print(
            "RF mean_macroF1="
            f"{results['rf']['mean_macroF1']:.4f} ± {results['rf']['std_macroF1']:.4f}"
        )
        results["classes"] = classes

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved -> {out_path}")


if __name__ == "__main__":
    main()
