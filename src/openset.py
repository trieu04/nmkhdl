"""Open-set evaluation: softmax max-prob, Mahalanobis trên embedding 128-d.

Unknown set = userD, userE, userI; Known = các fold đã train.
Dùng các model fold đã lưu, tổng hợp điểm trên toàn bộ unknown + val của từng fold.
"""
from __future__ import annotations
import json
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.model_selection import StratifiedGroupKFold

from .config import PROCESSED_DIR, MODELS_DIR, REPORTS_DIR, FIGURES_DIR, UNKNOWN_USERS, SEED, N_CHANNELS
from .datasets import InertialDataset
from .models import CNN1D
from .train import load_npz, split_known_unknown


def _embed_batch(model, X, mean, std, device, batch=256):
    ds = InertialDataset(X, np.zeros(len(X), dtype=np.int64), mean, std, augment=False)
    dl = DataLoader(ds, batch_size=batch, shuffle=False)
    embs, probs = [], []
    model.eval()
    with torch.no_grad():
        for xb, _ in dl:
            xb = xb.to(device)
            e = model.embed(xb)
            l = model.head(e)
            embs.append(e.cpu().numpy())
            probs.append(torch.softmax(l, 1).cpu().numpy())
    return np.concatenate(embs), np.concatenate(probs)


def _mahalanobis_score(emb, mus, inv_covs):
    """Trả về min distance tới các class-conditional Gaussian."""
    dists = np.empty((emb.shape[0], len(mus)), dtype=np.float32)
    for k, (mu, ic) in enumerate(zip(mus, inv_covs)):
        d = emb - mu
        dists[:, k] = np.einsum("ni,ij,nj->n", d, ic, d)
    return dists.min(axis=1)


def _fit_gaussians(emb_tr, y_tr, n_classes, reg=1e-3):
    mus, inv_covs = [], []
    d = emb_tr.shape[1]
    for k in range(n_classes):
        e = emb_tr[y_tr == k]
        if len(e) < 2:
            mus.append(np.zeros(d, dtype=np.float32))
            inv_covs.append(np.eye(d, dtype=np.float32))
            continue
        mu = e.mean(0)
        cov = np.cov(e, rowvar=False) + reg * np.eye(d)
        mus.append(mu.astype(np.float32))
        inv_covs.append(np.linalg.inv(cov).astype(np.float32))
    return mus, inv_covs


def evaluate_fold(fold_dir: Path, X_tr, y_tr, X_va, y_va, X_un, device):
    ckpt = torch.load(fold_dir / "model.pt", map_location=device, weights_only=False)
    classes = ckpt["classes"]; mean = ckpt["mean"]; std = ckpt["std"]
    model = CNN1D(in_channels=N_CHANNELS, n_classes=len(classes)).to(device)
    model.load_state_dict(ckpt["state"])

    emb_tr, _ = _embed_batch(model, X_tr, mean, std, device)
    emb_va, prob_va = _embed_batch(model, X_va, mean, std, device)
    emb_un, prob_un = _embed_batch(model, X_un, mean, std, device)

    # Softmax max prob (score càng cao = càng có khả năng known)
    s_soft_va = prob_va.max(axis=1)
    s_soft_un = prob_un.max(axis=1)

    # Mahalanobis: distance nhỏ = known. Lấy -distance làm score "known".
    mus, inv_covs = _fit_gaussians(emb_tr, y_tr, n_classes=len(classes))
    d_va = _mahalanobis_score(emb_va, mus, inv_covs)
    d_un = _mahalanobis_score(emb_un, mus, inv_covs)
    s_maha_va = -d_va
    s_maha_un = -d_un

    def auroc(s_known, s_unknown):
        y = np.concatenate([np.ones_like(s_known), np.zeros_like(s_unknown)])
        s = np.concatenate([s_known, s_unknown])
        return float(roc_auc_score(y, s))

    def tpr_at_fpr(s_known, s_unknown, target_fpr=0.05):
        y = np.concatenate([np.ones_like(s_known), np.zeros_like(s_unknown)])
        s = np.concatenate([s_known, s_unknown])
        fpr, tpr, _ = roc_curve(y, s)
        idx = np.searchsorted(fpr, target_fpr, side="right") - 1
        idx = max(idx, 0)
        return float(tpr[idx])

    return {
        "softmax": {
            "auroc": auroc(s_soft_va, s_soft_un),
            "tpr_at_fpr5": tpr_at_fpr(s_soft_va, s_soft_un, 0.05),
        },
        "mahalanobis": {
            "auroc": auroc(s_maha_va, s_maha_un),
            "tpr_at_fpr5": tpr_at_fpr(s_maha_va, s_maha_un, 0.05),
        },
        "n_val": int(len(s_soft_va)),
        "n_unknown": int(len(s_soft_un)),
    }


def main():
    device = "cpu"
    X, y, activity, groups = load_npz()
    (Xk, yk, actk, grk, Xu, yu, actu, gru) = split_known_unknown(X, y, activity, groups)
    classes = sorted(np.unique(yk).tolist())
    cls2id = {c: i for i, c in enumerate(classes)}
    yk_id = np.array([cls2id[v] for v in yk])

    # Tái tạo cùng split như train.py (3 folds)
    skf = StratifiedGroupKFold(n_splits=3, shuffle=True, random_state=SEED)
    results = {"folds": []}
    for fold, (tr_idx, va_idx) in enumerate(skf.split(Xk, yk_id, groups=grk)):
        fold_dir = MODELS_DIR / f"fold{fold}"
        if not (fold_dir / "model.pt").exists():
            continue
        print(f"=== Fold {fold} ===")
        r = evaluate_fold(fold_dir,
                          Xk[tr_idx], yk_id[tr_idx],
                          Xk[va_idx], yk_id[va_idx],
                          Xu, device)
        r["fold"] = fold
        print(json.dumps(r, indent=2))
        results["folds"].append(r)

    # Aggregate
    if results["folds"]:
        for method in ["softmax", "mahalanobis"]:
            aurocs = [r[method]["auroc"] for r in results["folds"]]
            tprs = [r[method]["tpr_at_fpr5"] for r in results["folds"]]
            results[method] = {
                "mean_auroc": float(np.mean(aurocs)),
                "std_auroc": float(np.std(aurocs)),
                "mean_tpr_at_fpr5": float(np.mean(tprs)),
            }
    out = REPORTS_DIR / "openset_results.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved -> {out}")
    print(json.dumps({k: v for k, v in results.items() if k != "folds"}, indent=2))


if __name__ == "__main__":
    main()
