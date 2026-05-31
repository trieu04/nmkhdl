"""Trích feature thủ công cho baseline cổ điển và keystroke."""
from __future__ import annotations
import numpy as np
import pandas as pd

from .config import INERTIAL_CHANNELS, FS, INTERIM_DIR
from .io import load_keystroke


# ---------------- Inertial HAR-style features ----------------

def _stats_per_axis(x: np.ndarray) -> dict:
    """x: (T,) → dict các thống kê cơ bản + FFT đặc trưng."""
    d = {}
    d["mean"] = float(np.mean(x))
    d["std"] = float(np.std(x))
    d["mad"] = float(np.mean(np.abs(x - np.mean(x))))
    d["min"] = float(np.min(x))
    d["max"] = float(np.max(x))
    d["iqr"] = float(np.percentile(x, 75) - np.percentile(x, 25))
    d["energy"] = float(np.mean(x ** 2))
    # entropy của |FFT|
    fft = np.abs(np.fft.rfft(x))
    p = fft / (fft.sum() + 1e-12)
    d["fft_entropy"] = float(-np.sum(p * np.log(p + 1e-12)))
    freqs = np.fft.rfftfreq(len(x), d=1.0 / FS)
    d["fft_dom_freq"] = float(freqs[np.argmax(fft)])
    return d


def window_features(w: np.ndarray) -> np.ndarray:
    """w: (T, C=6) → vector feature 1D."""
    feats = []
    names = []
    for ci, ch in enumerate(INERTIAL_CHANNELS):
        stats = _stats_per_axis(w[:, ci])
        for k, v in stats.items():
            feats.append(v)
            names.append(f"{ch}_{k}")
    # Correlation giữa các trục
    with np.errstate(divide="ignore", invalid="ignore"):
        corr = np.corrcoef(w.T)
    corr = np.nan_to_num(corr, nan=0.0, posinf=0.0, neginf=0.0)
    pairs = [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5), (0, 3), (1, 4), (2, 5)]
    for i, j in pairs:
        feats.append(float(corr[i, j]) if np.isfinite(corr[i, j]) else 0.0)
        names.append(f"corr_{INERTIAL_CHANNELS[i]}_{INERTIAL_CHANNELS[j]}")
    # Signal magnitude area
    feats.append(float(np.mean(np.sum(np.abs(w[:, :3]), axis=1))))
    names.append("acc_sma")
    feats.append(float(np.mean(np.sum(np.abs(w[:, 3:]), axis=1))))
    names.append("gyro_sma")
    return np.array(feats, dtype=np.float32), names


def batch_features(X: np.ndarray) -> tuple[np.ndarray, list[str]]:
    """X: (N, T, C) → (N, F)."""
    feats, names = [], None
    for i in range(len(X)):
        f, n = window_features(X[i])
        feats.append(f)
        if names is None:
            names = n
    return np.stack(feats, axis=0), names


# ---------------- Keystroke features (per file → 1 vector) ----------------

def keystroke_features(df: pd.DataFrame) -> dict:
    if len(df) == 0 or not {"interKeyMs", "isDelete", "charCount", "timestamp"}.issubset(df.columns):
        return {}
    iki = df["interKeyMs"].astype(float).to_numpy()
    iki = iki[iki > 0]  # bỏ phím đầu (0)
    out = {
        "n_events": len(df),
        "iki_mean": float(np.mean(iki)) if len(iki) else 0.0,
        "iki_std": float(np.std(iki)) if len(iki) else 0.0,
        "iki_p25": float(np.percentile(iki, 25)) if len(iki) else 0.0,
        "iki_p75": float(np.percentile(iki, 75)) if len(iki) else 0.0,
        "delete_rate": float(df["isDelete"].astype(str).str.lower().eq("true").mean()),
    }
    ts = df["timestamp"].astype(float).to_numpy()
    if len(ts) > 1 and (ts.max() - ts.min()) > 0:
        # ms → s; charCount đếm ký tự lũy kế
        out["typing_speed_cps"] = float(df["charCount"].max() / ((ts.max() - ts.min()) / 1000.0))
    else:
        out["typing_speed_cps"] = 0.0
    return out


# ---------------- Aggregate per user (cho baseline đơn giản) ----------------

def aggregate_user_features(manifest: pd.DataFrame) -> pd.DataFrame:
    """Gom đặc trưng keystroke theo từng file."""
    rows_k = []
    for _, r in manifest.iterrows():
        if r["modality"] == "keystroke":
            df = load_keystroke(r["user"], r["file"])
            feats = keystroke_features(df)
            if feats:
                feats.update({"user": r["user"], "file": r["file"]})
                rows_k.append(feats)
    return pd.DataFrame(rows_k)


def main():
    manifest = pd.read_csv(INTERIM_DIR / "manifest.csv")
    k_df = aggregate_user_features(manifest)
    k_df.to_csv(INTERIM_DIR / "feat_keystroke.csv", index=False)
    print(f"keystroke: {k_df.shape}")
    print("Sample keystroke head:")
    print(k_df.head())


if __name__ == "__main__":
    main()
