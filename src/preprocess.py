"""Tiền xử lý inertial: resample → filter → window → scale → npz."""
from __future__ import annotations
import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt, resample_poly
from pathlib import Path

from .config import (
    FS, WINDOW_SIZE, WINDOW_STRIDE, INERTIAL_CHANNELS,
    LOWPASS_CUTOFF, HIGHPASS_GRAVITY, PROCESSED_DIR, INTERIM_DIR, SEED,
)
from .io import load_inertial


def _butter_lowpass(data: np.ndarray, cutoff: float, fs: float, order: int = 4) -> np.ndarray:
    nyq = 0.5 * fs
    b, a = butter(order, cutoff / nyq, btype="low")
    return filtfilt(b, a, data, axis=0)


def _butter_highpass(data: np.ndarray, cutoff: float, fs: float, order: int = 4) -> np.ndarray:
    nyq = 0.5 * fs
    b, a = butter(order, cutoff / nyq, btype="high")
    return filtfilt(b, a, data, axis=0)


def preprocess_inertial(df: pd.DataFrame, fs_in: float | None = None) -> np.ndarray:
    """Trả về mảng (T, 6) đã filter, fs cuối = FS (50 Hz)."""
    x = df[INERTIAL_CHANNELS].to_numpy(dtype=np.float32)
    # NaN safety
    if np.isnan(x).any():
        x = pd.DataFrame(x).ffill().bfill().to_numpy(dtype=np.float32)
    # Resample nếu fs_in lệch nhiều
    if fs_in and fs_in > 0 and abs(fs_in - FS) > 1.0:
        up = int(round(FS))
        down = int(round(fs_in))
        if up != down:
            x = resample_poly(x, up, down, axis=0).astype(np.float32)
    if len(x) < 8:
        return x
    # Low-pass khử nhiễu cao tần
    x = _butter_lowpass(x, LOWPASS_CUTOFF, FS).astype(np.float32)
    # High-pass tách trọng lực cho 3 trục acc (cột 0..2)
    if len(x) > 30:
        acc_body = _butter_highpass(x[:, :3], HIGHPASS_GRAVITY, FS).astype(np.float32)
        x[:, :3] = acc_body
    return x


def sliding_windows(x: np.ndarray, size: int = WINDOW_SIZE, stride: int = WINDOW_STRIDE) -> np.ndarray:
    """(T,C) → (N, size, C)."""
    if len(x) < size:
        return np.empty((0, size, x.shape[1]), dtype=np.float32)
    n = 1 + (len(x) - size) // stride
    out = np.empty((n, size, x.shape[1]), dtype=np.float32)
    for i in range(n):
        out[i] = x[i * stride : i * stride + size]
    return out


def build_windows(manifest: pd.DataFrame, max_per_file: int = 300, seed: int = SEED) -> dict:
    """Duyệt mọi file inertial, sinh windows + nhãn.

    max_per_file: cap số window mỗi file để tránh imbalance (1 file dài có thể
    sinh hàng chục nghìn window). Lấy mẫu đều dọc theo trục thời gian.
    """
    rng = np.random.default_rng(seed)
    Xs, ys, acts, files = [], [], [], []
    inertial = manifest[manifest["modality"] == "inertial"].reset_index(drop=True)
    for _, r in inertial.iterrows():
        df = load_inertial(r["user"], r["file"])
        if df.empty:
            continue
        fs_in = r["fs_est"] if pd.notna(r["fs_est"]) else FS
        x = preprocess_inertial(df, fs_in=fs_in)
        w = sliding_windows(x)
        if len(w) == 0:
            continue
        if len(w) > max_per_file:
            # Lấy mẫu đều theo index để giữ tính phân tán theo thời gian
            idx = np.linspace(0, len(w) - 1, max_per_file).astype(int)
            w = w[idx]
        Xs.append(w)
        ys.extend([r["user"]] * len(w))
        acts.extend([r["activity"]] * len(w))
        files.extend([f"{r['user']}__{r['file']}"] * len(w))
    X = np.concatenate(Xs, axis=0).astype(np.float32)
    y = np.array(ys)
    activity = np.array(acts)
    groups = np.array(files)  # group = user__file để chống leakage
    return {"X": X, "y": y, "activity": activity, "groups": groups}


def main():
    manifest = pd.read_csv(INTERIM_DIR / "manifest.csv")
    out = build_windows(manifest)
    out_path = PROCESSED_DIR / "windows.npz"
    np.savez_compressed(out_path, **out)
    print(f"Saved {out_path}")
    print(f"  X shape : {out['X'].shape}")
    print(f"  y unique: {sorted(np.unique(out['y']).tolist())}")
    print(f"  N per user:")
    s = pd.Series(out["y"]).value_counts().sort_index()
    print(s.to_string())
    print(f"  N per activity:")
    print(pd.Series(out["activity"]).value_counts().to_string())


if __name__ == "__main__":
    main()
