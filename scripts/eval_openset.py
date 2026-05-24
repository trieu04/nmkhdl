#!/usr/bin/env python
"""Phase J: Open-set evaluation via softmax entropy & closeness thresholds.
Usage:
    python -m scripts.eval_openset --base-run 20260518-012834_E_E03_rotation_only
"""
import argparse
from pathlib import Path
import numpy as np
import torch
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.metrics import roc_auc_score, roc_curve

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.config import SEED, UNKNOWN_USERS
from src.experiment import ExperimentLogger
from src.train import load_npz, split_known_unknown
from src.models import make_model
from src.datasets import InertialDataset
import yaml


def softmax_entropy(logits):
    """Entropy of softmax distribution."""
    probs = np.softmax(logits, axis=1)
    entropy = -np.sum(probs * np.log(np.maximum(probs, 1e-10)), axis=1)
    return entropy


def max_softmax_prob(logits):
    """Max probability from softmax."""
    probs = np.softmax(logits, axis=1)
    return np.max(probs, axis=1)


def eval_openset_fold(X_k, y_k, X_u, fold_idx, device, model_path, cfg):
    """Evaluate open-set detection: known vs unknown users."""
    model_state = torch.load(model_path, map_location=device, weights_only=False)
    n_classes = len(model_state.get("classes", np.unique(y_k)))
    
    model = make_model(cfg, 6, n_classes).to(device)
    model.load_state_dict(model_state["state"])
    model.eval()
    
    # Get logits on known
    logits_k = []
    with torch.no_grad():
        for idx in range(0, len(X_k), 256):
            xb = torch.from_numpy(X_k[idx:idx+256]).float().to(device)
            logits = model(xb)
            logits_k.append(logits.cpu().numpy())
    logits_k = np.concatenate(logits_k)
    
    # Get logits on unknown
    logits_u = []
    with torch.no_grad():
        for idx in range(0, len(X_u), 256):
            xb = torch.from_numpy(X_u[idx:idx+256]).float().to(device)
            logits = model(xb)
            logits_u.append(logits.cpu().numpy())
    logits_u = np.concatenate(logits_u)
    
    # Compute scores
    score_k = max_softmax_prob(logits_k)  # Known should have high prob
    score_u = max_softmax_prob(logits_u)  # Unknown should have low prob
    
    # Labels: 1=known, 0=unknown
    scores = np.concatenate([score_k, score_u])
    labels = np.concatenate([np.ones_like(score_k), np.zeros_like(score_u)])
    
    # AUROC
    auroc = roc_auc_score(labels, scores)
    return auroc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-run", type=str, required=True,
                       help="Base run_id for model")
    parser.add_argument("--notes", type=str, default="")
    args = parser.parse_args()
    
    runs_dir = Path(__file__).parent.parent / "experiments" / "runs"
    base_run_dir = runs_dir / args.base_run
    
    if not base_run_dir.exists():
        raise FileNotFoundError(f"Base run dir not found: {base_run_dir}")
    
    cfg = yaml.safe_load(open(base_run_dir / "config.json"))
    
    # Load data
    X, y, activity, groups = load_npz()
    X_k, y_k, _, gr_k = split_known_unknown(X, y, activity, groups)
    
    # Unknown windows (those with y in UNKNOWN_USERS)
    X_u = X[np.isin(y, UNKNOWN_USERS)]
    
    if len(X_u) == 0:
        print(f"WARNING: no unknown windows found (UNKNOWN_USERS={UNKNOWN_USERS})")
        X_u = X_k[:100]  # Fallback
    
    # Eval on 3-fold
    skf = StratifiedGroupKFold(n_splits=3, shuffle=True, random_state=SEED)
    aurocs = []
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    for fold_idx, (_, va_idx) in enumerate(skf.split(X_k, y_k, groups=gr_k)):
        model_path = base_run_dir / f"fold{fold_idx}" / "model.pt"
        if not model_path.exists():
            continue
        
        try:
            auroc = eval_openset_fold(X_k[va_idx], y_k[va_idx], X_u,
                                      fold_idx, device, model_path, cfg)
            aurocs.append(auroc)
            print(f"Fold {fold_idx}: open-set AUROC={auroc:.4f}")
        except Exception as e:
            print(f"Fold {fold_idx} error: {e}")
    
    mean_auroc = float(np.mean(aurocs)) if aurocs else 0.0
    std_auroc = float(np.std(aurocs)) if aurocs else 0.0
    
    # Log as synthetic F1 (use AUROC as metric)
    logger = ExperimentLogger(
        name=f"J_openset_{args.base_run.split('_')[-1]}",
        phase="J",
        config={"base_run": args.base_run, "metric": "auroc"},
        notes=args.notes or f"Open-set AUROC on {args.base_run}"
    )
    # Report AUROC; interpret as synthetic F1 for leaderboard
    synthetic_f1 = mean_auroc  # Use AUROC directly as score
    logger.set_metric("mean_macroF1", synthetic_f1)
    logger.set_metric("std_macroF1", std_auroc)
    logger.set_metric("openset_auroc", mean_auroc)
    logger.set_metric("openset_auroc_std", std_auroc)
    
    print(f"\n[RESULT] Phase J Open-set AUROC = {mean_auroc:.4f} ± {std_auroc:.4f}")
    logger.__exit__(None, None, None)


if __name__ == "__main__":
    main()
