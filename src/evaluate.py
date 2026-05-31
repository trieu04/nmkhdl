"""Đánh giá tổng hợp: RF baseline trên feature thủ công, confusion matrix CNN,
per-activity accuracy, vẽ figure."""
from __future__ import annotations
import json
from pathlib import Path

import numpy as np
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.metrics import (classification_report, confusion_matrix, f1_score,
                             accuracy_score)
from sklearn.preprocessing import StandardScaler

from .config import (PROCESSED_DIR, MODELS_DIR, REPORTS_DIR, FIGURES_DIR,
                     UNKNOWN_USERS, SEED, N_CHANNELS, ACTIVITIES)
from .datasets import InertialDataset
from .features import batch_features
from .models import CNN1D
from .train import load_npz, split_known_unknown


def rf_baseline(Xk, yk_id, grk, n_splits=3):
    print("Extract hand-crafted features ...")
    F, _names = batch_features(Xk)
    F = np.nan_to_num(F, nan=0.0, posinf=0.0, neginf=0.0)
    print(f"Features shape: {F.shape}")
    skf = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=SEED)
    f1s, accs = [], []
    for fold, (tr, va) in enumerate(skf.split(F, yk_id, groups=grk)):
        sc = StandardScaler().fit(F[tr])
        Ft, Fv = sc.transform(F[tr]), sc.transform(F[va])
        clf = RandomForestClassifier(n_estimators=300, n_jobs=-1, random_state=SEED,
                                     class_weight="balanced_subsample")
        clf.fit(Ft, yk_id[tr])
        pred = clf.predict(Fv)
        f1 = f1_score(yk_id[va], pred, average="macro", zero_division=0)
        acc = accuracy_score(yk_id[va], pred)
        f1s.append(f1); accs.append(acc)
        print(f"  RF fold{fold}: macroF1={f1:.4f}  acc={acc:.4f}")
    return {"fold_f1s": [float(v) for v in f1s],
            "fold_accuracies": [float(v) for v in accs],
            "mean_macroF1": float(np.mean(f1s)),
            "std_macroF1": float(np.std(f1s)),
            "mean_accuracy": float(np.mean(accs))}


def cnn_predictions(Xk, yk_id, grk, actk, n_splits=3):
    """Chạy lại 3-fold để gom pred CNN từ checkpoint đã lưu."""
    skf = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=SEED)
    all_gts, all_preds, all_acts = [], [], []
    device = "cpu"
    for fold, (tr_idx, va_idx) in enumerate(skf.split(Xk, yk_id, groups=grk)):
        ckpt = MODELS_DIR / f"fold{fold}" / "model.pt"
        if not ckpt.exists():
            continue
        st = torch.load(ckpt, map_location=device, weights_only=False)
        classes = st["classes"]
        model = CNN1D(in_channels=N_CHANNELS, n_classes=len(classes)).to(device)
        model.load_state_dict(st["state"])
        model.eval()
        ds = InertialDataset(Xk[va_idx], yk_id[va_idx], st["mean"], st["std"])
        dl = DataLoader(ds, batch_size=256, shuffle=False)
        preds = []
        with torch.no_grad():
            for xb, _ in dl:
                preds.append(model(xb.to(device)).argmax(1).cpu().numpy())
        preds = np.concatenate(preds)
        all_gts.append(yk_id[va_idx]); all_preds.append(preds)
        all_acts.append(actk[va_idx])
    return (np.concatenate(all_gts), np.concatenate(all_preds),
            np.concatenate(all_acts), classes)


def plot_confusion(gts, preds, classes, out_path):
    cm = confusion_matrix(gts, preds, labels=list(range(len(classes))))
    cm_norm = cm.astype(np.float32) / np.maximum(cm.sum(axis=1, keepdims=True), 1)
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(cm_norm, cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks(range(len(classes))); ax.set_yticks(range(len(classes)))
    ax.set_xticklabels(classes, rotation=45, ha="right")
    ax.set_yticklabels(classes)
    ax.set_xlabel("Predicted"); ax.set_ylabel("True")
    ax.set_title("CNN1D 3-fold aggregated (normalized)")
    for i in range(len(classes)):
        for j in range(len(classes)):
            v = cm_norm[i, j]
            if v > 0.02:
                ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                        color="white" if v > 0.5 else "black", fontsize=7)
    fig.colorbar(im, ax=ax, fraction=0.046)
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)


def per_activity_accuracy(gts, preds, acts):
    out = {}
    for a in ACTIVITIES + ["unknown"]:
        m = acts == a
        if m.sum() == 0:
            continue
        out[a] = {
            "n": int(m.sum()),
            "accuracy": float(accuracy_score(gts[m], preds[m])),
            "macroF1": float(f1_score(gts[m], preds[m], average="macro", zero_division=0)),
        }
    return out


def plot_per_activity(per_act, out_path):
    labels = list(per_act.keys())
    accs = [per_act[a]["accuracy"] for a in labels]
    f1s = [per_act[a]["macroF1"] for a in labels]
    x = np.arange(len(labels)); w = 0.35
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(x - w/2, accs, w, label="accuracy")
    ax.bar(x + w/2, f1s, w, label="macroF1")
    ax.set_xticks(x); ax.set_xticklabels(labels)
    ax.set_ylim(0, 1); ax.set_ylabel("score")
    ax.set_title("CNN1D per-activity performance")
    ax.legend()
    fig.tight_layout(); fig.savefig(out_path, dpi=120); plt.close(fig)


def main():
    data = load_npz()
    X, y, activity, groups = (
        data["X"],
        data["y"],
        data["activity"],
        data["groups"],
    )
    (Xk, yk, actk, grk, *_) = split_known_unknown(X, y, activity, groups)
    classes = sorted(np.unique(yk).tolist())
    cls2id = {c: i for i, c in enumerate(classes)}
    yk_id = np.array([cls2id[v] for v in yk])

    # --- CNN aggregated ---
    print("Collecting CNN predictions ...")
    gts, preds, acts, classes_ck = cnn_predictions(Xk, yk_id, grk, actk)
    cnn_acc = float(accuracy_score(gts, preds))
    cnn_f1 = float(f1_score(gts, preds, average="macro", zero_division=0))
    print(f"CNN aggregated: acc={cnn_acc:.4f}  macroF1={cnn_f1:.4f}")

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    plot_confusion(gts, preds, classes, FIGURES_DIR / "cnn_confusion.png")
    per_act = per_activity_accuracy(gts, preds, acts)
    plot_per_activity(per_act, FIGURES_DIR / "cnn_per_activity.png")
    print("Per-activity:", per_act)

    # --- RF baseline ---
    print("\nRandom Forest baseline ...")
    rf = rf_baseline(Xk, yk_id, grk)
    print("RF:", rf)

    metrics = {
        "cnn_aggregated": {"accuracy": cnn_acc, "macroF1": cnn_f1},
        "cnn_per_activity": per_act,
        "rf_baseline": rf,
    }
    out = REPORTS_DIR / "evaluate_results.json"
    with open(out, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"Saved -> {out}")


if __name__ == "__main__":
    main()
