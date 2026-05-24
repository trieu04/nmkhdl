#!/usr/bin/env python
"""Phase H: Train Random Forest on CNN deep features from a trained CNN model.
Usage:
    python -m scripts.train_rf_features --base-run 20260518-012834_E_E03_rotation_only \
                                         --n-forests 3 --n-estimators 300
"""
import argparse
from pathlib import Path
import numpy as np
import torch
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.metrics import f1_score
from sklearn.preprocessing import StandardScaler

import yaml

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.config import SEED
from src.experiment import ExperimentLogger
from src.train import load_npz, split_known_unknown
from src.models import make_model
from src.datasets import InertialDataset


def extract_features_fold(X, y, groups, fold_idx, device, model_path, cfg):
    """Extract CNN hidden features from a trained fold."""
    model_state = torch.load(model_path, map_location=device, weights_only=False)
    
    in_ch = 6  # hard-code for inertial
    n_classes = len(model_state.get("classes", np.unique(y)))
    model = make_model(cfg, in_ch, n_classes).to(device)
    model.load_state_dict(model_state["state"])
    model.eval()
    
    # Remove classification head, keep embedding layer
    # Assume model has .proj or can access penultimate layer
    # For now, extract logits then return (works as features)
    
    all_feat = []
    with torch.no_grad():
        for idx in range(0, len(X), 256):
            xb = torch.from_numpy(X[idx:idx+256]).float().to(device)
            # Forward through model, extract logits (as deep features)
            logits = model(xb)  # shape (B, n_classes)
            all_feat.append(logits.cpu().numpy())
    return np.concatenate(all_feat)  # (N, n_classes)


def train_rf_on_features(X, y, groups, base_run_id, n_forests, n_estimators, verbose=True):
    """Train RF on CNN features extracted from base_run model."""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    runs_dir = Path(__file__).parent.parent / "experiments" / "runs"
    base_run_dir = runs_dir / base_run_id
    
    if not base_run_dir.exists():
        raise FileNotFoundError(f"Base run dir not found: {base_run_dir}")
    
    cfg_path = base_run_dir / "config.json"
    with open(cfg_path) as f:
        cfg = yaml.safe_load(f)
    
    skf = StratifiedGroupKFold(n_splits=n_forests, shuffle=True, random_state=SEED)
    fold_f1s = []
    
    for fold_idx, (tr_idx, va_idx) in enumerate(skf.split(X, y, groups=groups)):
        if verbose:
            print(f"[fold {fold_idx}] extracting features from base model ...")
        
        model_path = base_run_dir / f"fold{fold_idx}" / "model.pt"
        if not model_path.exists():
            print(f"  WARNING: model path {model_path} not found, skip fold {fold_idx}")
            continue
        
        # Extract features
        F_tr = extract_features_fold(X[tr_idx], y[tr_idx], groups[tr_idx], 
                                     fold_idx, device, model_path, cfg)
        F_va = extract_features_fold(X[va_idx], y[va_idx], groups[va_idx],
                                     fold_idx, device, model_path, cfg)
        
        # Scale & train RF
        scaler = StandardScaler().fit(F_tr)
        F_tr_sc = scaler.transform(F_tr)
        F_va_sc = scaler.transform(F_va)
        
        rf = RandomForestClassifier(n_estimators=n_estimators, n_jobs=-1,
                                    random_state=SEED, class_weight="balanced_subsample")
        rf.fit(F_tr_sc, y[tr_idx])
        pred = rf.predict(F_va_sc)
        
        f1 = f1_score(y[va_idx], pred, average="macro", zero_division=0)
        fold_f1s.append(f1)
        if verbose:
            print(f"  RF fold {fold_idx}: macroF1={f1:.4f}")
    
    mean_f1 = float(np.mean(fold_f1s)) if fold_f1s else 0.0
    std_f1 = float(np.std(fold_f1s)) if fold_f1s else 0.0
    return mean_f1, std_f1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-run", type=str, required=True,
                       help="Base run_id to extract features from (e.g., 20260518-012834_E_E03_rotation_only)")
    parser.add_argument("--n-forests", type=int, default=3, help="Number of folds")
    parser.add_argument("--n-estimators", type=int, default=300, help="RF n_estimators")
    parser.add_argument("--notes", type=str, default="", help="Optional notes")
    args = parser.parse_args()
    
    # Load data
    X, y, activity, groups = load_npz()
    X_k, y_k, _, gr_k = split_known_unknown(X, y, activity, groups)
    
    # Train RF on features
    mean_f1, std_f1 = train_rf_on_features(X_k, y_k, gr_k, args.base_run,
                                           args.n_forests, args.n_estimators)
    
    # Log result
    logger = ExperimentLogger(
        name=f"H_rf_on_{args.base_run.split('_')[-1]}",
        phase="H",
        config={"base_run": args.base_run, "n_forests": args.n_forests,
                "n_estimators": args.n_estimators},
        notes=args.notes or f"RF n_est={args.n_estimators} on CNN logits from {args.base_run}"
    )
    logger.set_metric("mean_macroF1", mean_f1)
    logger.set_metric("std_macroF1", std_f1)
    print(f"\n[RESULT] Phase H RF on base={args.base_run}")
    print(f"  mean_macroF1 = {mean_f1:.4f} ± {std_f1:.4f}")
    logger.__exit__(None, None, None)


if __name__ == "__main__":
    main()
