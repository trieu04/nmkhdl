"""Dataset + augmentation cho chuỗi cảm biến 6 kênh (acc_xyz, gyro_xyz).

Augmentation (bật/tắt qua aug_cfg):
- jitter: cộng Gaussian noise N(0, σ²)
- scale: nhân với hệ số ngẫu nhiên trong [s_low, s_high]
- rotation: quay đồng thời acc và gyro quanh 3 trục (góc nhỏ ±θ rad)
- time_warp: cubic-spline warping miền thời gian (n_knots, σ_warp)

MixUp / CutMix nên áp dụng ở mức batch (xem `mixup_batch`, `cutmix_batch`).
"""
from __future__ import annotations
import numpy as np
import torch
from torch.utils.data import Dataset


def _rotation_matrix(theta_x: float, theta_y: float, theta_z: float) -> np.ndarray:
    cx, sx = np.cos(theta_x), np.sin(theta_x)
    cy, sy = np.cos(theta_y), np.sin(theta_y)
    cz, sz = np.cos(theta_z), np.sin(theta_z)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return Rz @ Ry @ Rx


def _time_warp(x: np.ndarray, n_knots: int, sigma: float, rng: np.random.Generator) -> np.ndarray:
    """Cubic spline warping. x shape (T, C)."""
    T, C = x.shape
    knot_x = np.linspace(0, T - 1, n_knots)
    knot_y = knot_x + rng.normal(0, sigma * T / n_knots, size=n_knots)
    knot_y[0] = 0
    knot_y[-1] = T - 1
    knot_y = np.sort(np.clip(knot_y, 0, T - 1))
    # piecewise linear interpolation of new sampling positions
    new_idx = np.interp(np.arange(T), knot_y, knot_x)
    out = np.empty_like(x)
    for c in range(C):
        out[:, c] = np.interp(new_idx, np.arange(T), x[:, c])
    return out


class InertialDataset(Dataset):
    """X: (N, T, C); y: (N,). Trả về tensor shape (C, T) cho Conv1D."""

    def __init__(self, X: np.ndarray, y: np.ndarray,
                 mean: np.ndarray | None = None, std: np.ndarray | None = None,
                 augment: bool = False,
                 aug_cfg: dict | None = None,
                 rng_seed: int = 0):
        self.X = X.astype(np.float32)
        self.y = y.astype(np.int64)
        self.mean = (np.zeros(X.shape[-1], dtype=np.float32)
                     if mean is None else mean.astype(np.float32))
        self.std = (np.ones(X.shape[-1], dtype=np.float32)
                    if std is None else std.astype(np.float32))
        self.augment = augment
        cfg = aug_cfg or {}
        self.jitter_sigma = cfg.get("jitter_sigma", 0.02)
        self.scale_low = cfg.get("scale_low", 0.9)
        self.scale_high = cfg.get("scale_high", 1.1)
        self.rot_theta = cfg.get("rot_theta", 0.1)
        self.use_jitter = cfg.get("use_jitter", True)
        self.use_scale = cfg.get("use_scale", True)
        self.use_rotation = cfg.get("use_rotation", True)
        self.use_time_warp = cfg.get("use_time_warp", False)
        self.tw_knots = cfg.get("tw_knots", 5)
        self.tw_sigma = cfg.get("tw_sigma", 0.2)
        self.rng = np.random.default_rng(rng_seed)

    def __len__(self):
        return len(self.X)

    def _augment(self, x: np.ndarray) -> np.ndarray:
        # x: (T, C=6) — first 3 acc, last 3 gyro
        if self.use_rotation and x.shape[1] >= 6:
            tx, ty, tz = self.rng.uniform(-self.rot_theta, self.rot_theta, size=3)
            R = _rotation_matrix(tx, ty, tz).astype(np.float32)
            x = x.copy()
            x[:, 0:3] = x[:, 0:3] @ R.T
            x[:, 3:6] = x[:, 3:6] @ R.T
        if self.use_scale:
            s = self.rng.uniform(self.scale_low, self.scale_high)
            x = x * s
        if self.use_jitter and self.jitter_sigma > 0:
            x = x + self.rng.normal(0, self.jitter_sigma, size=x.shape).astype(np.float32)
        if self.use_time_warp:
            x = _time_warp(x, self.tw_knots, self.tw_sigma, self.rng).astype(np.float32)
        return x

    def __getitem__(self, idx):
        x = self.X[idx]
        if self.augment:
            x = self._augment(x)
        # normalize
        x = (x - self.mean) / (self.std + 1e-8)
        # to (C, T)
        x = x.T.astype(np.float32)
        return torch.from_numpy(x), int(self.y[idx])


def compute_scaler(X: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """X (N, T, C) → mean, std shape (C,)."""
    flat = X.reshape(-1, X.shape[-1])
    return flat.mean(axis=0), flat.std(axis=0)


def mixup_batch(x: torch.Tensor, y: torch.Tensor, alpha: float = 0.2,
                rng: np.random.Generator | None = None
                ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, float]:
    """Trả về (x_mixed, y_a, y_b, lam) — dùng với CE: lam*CE(y_a)+(1-lam)*CE(y_b)."""
    rng = rng or np.random.default_rng()
    lam = float(rng.beta(alpha, alpha)) if alpha > 0 else 1.0
    idx = torch.randperm(x.size(0), device=x.device)
    x_m = lam * x + (1 - lam) * x[idx]
    return x_m, y, y[idx], lam


def cutmix_batch(x: torch.Tensor, y: torch.Tensor, alpha: float = 1.0,
                 rng: np.random.Generator | None = None
                 ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, float]:
    """CutMix dọc trục thời gian. x: (B, C, T)."""
    rng = rng or np.random.default_rng()
    lam = float(rng.beta(alpha, alpha)) if alpha > 0 else 1.0
    B, C, T = x.shape
    idx = torch.randperm(B, device=x.device)
    cut_len = int(T * (1 - lam))
    if cut_len > 0:
        start = int(rng.integers(0, T - cut_len + 1))
        x = x.clone()
        x[:, :, start:start + cut_len] = x[idx, :, start:start + cut_len]
        lam = 1 - cut_len / T
    return x, y, y[idx], lam
