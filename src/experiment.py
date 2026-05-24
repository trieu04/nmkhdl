"""Lightweight experiment logger — CSV-based, không phụ thuộc thư viện ngoài.

Schema `experiments/log.csv` (append-only):
run_id, phase, name, timestamp, mean_macroF1, std_macroF1,
fold0_f1, fold1_f1, fold2_f1, openset_auroc, runtime_sec, notes, config_json

Cách dùng:
    from src.experiment import ExperimentLogger
    with ExperimentLogger("B03_cosine_80ep", phase="B", config=cfg) as run:
        ...
        run.set_metric("mean_macroF1", 0.72)
        run.set_metric("fold0_f1", 0.71)
        run.set_history(history_list)   # ghi history.json
        run.set_report(report_dict)     # ghi report.json
"""
from __future__ import annotations
import csv
import json
import time
import datetime as dt
from pathlib import Path
from typing import Any

from .config import PROJECT_ROOT

EXP_DIR = PROJECT_ROOT / "experiments"
RUNS_DIR = EXP_DIR / "runs"
LOG_CSV = EXP_DIR / "log.csv"
WINNERS_MD = EXP_DIR / "winners.md"

EXP_DIR.mkdir(parents=True, exist_ok=True)
RUNS_DIR.mkdir(parents=True, exist_ok=True)

LOG_COLUMNS = [
    "run_id", "phase", "name", "timestamp",
    "mean_macroF1", "std_macroF1",
    "fold0_f1", "fold1_f1", "fold2_f1",
    "openset_auroc", "rf_macroF1",
    "runtime_sec", "notes", "config_json",
]


def _ensure_csv():
    if not LOG_CSV.exists():
        with open(LOG_CSV, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(LOG_COLUMNS)


class ExperimentLogger:
    def __init__(self, name: str, phase: str = "X", config: dict | None = None,
                 notes: str = ""):
        self.name = name
        self.phase = phase
        self.config = config or {}
        self.notes = notes
        self.metrics: dict[str, Any] = {}
        self.t0 = None
        self.run_id = None
        self.run_dir: Path | None = None

    def __enter__(self):
        _ensure_csv()
        ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        self.run_id = f"{ts}_{self.phase}_{self.name}"
        self.run_dir = RUNS_DIR / self.run_id
        self.run_dir.mkdir(parents=True, exist_ok=True)
        with open(self.run_dir / "config.json", "w") as f:
            json.dump(self.config, f, indent=2, default=str)
        self.t0 = time.time()
        return self

    def set_metric(self, k: str, v: Any):
        self.metrics[k] = v

    def set_history(self, history: list):
        with open(self.run_dir / "history.json", "w") as f:
            json.dump(history, f, indent=2)

    def set_report(self, report: dict):
        with open(self.run_dir / "report.json", "w") as f:
            json.dump(report, f, indent=2)

    def save_json(self, name: str, obj: Any):
        with open(self.run_dir / name, "w") as f:
            json.dump(obj, f, indent=2, default=str)

    def __exit__(self, exc_type, exc, tb):
        runtime = time.time() - (self.t0 or time.time())
        row = {col: "" for col in LOG_COLUMNS}
        row["run_id"] = self.run_id
        row["phase"] = self.phase
        row["name"] = self.name
        row["timestamp"] = dt.datetime.now().isoformat(timespec="seconds")
        row["runtime_sec"] = f"{runtime:.1f}"
        row["notes"] = self.notes if exc_type is None else f"ERROR: {exc}"
        row["config_json"] = json.dumps(self.config, default=str)
        for k in ("mean_macroF1", "std_macroF1", "fold0_f1", "fold1_f1",
                  "fold2_f1", "openset_auroc", "rf_macroF1"):
            if k in self.metrics:
                v = self.metrics[k]
                row[k] = f"{v:.4f}" if isinstance(v, float) else str(v)
        # append
        with open(LOG_CSV, "a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=LOG_COLUMNS)
            w.writerow(row)
        # save metrics.json
        self.save_json("metrics.json", self.metrics)
        return False  # don't suppress
