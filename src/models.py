"""CNN 1D + ResNet1D + TCN + BiLSTM cho định danh người dùng từ chuỗi cảm biến."""
from __future__ import annotations
import torch
import torch.nn as nn
import torch.nn.functional as F


class CNN1D(nn.Module):
    """Parameterized CNN 1D.

    filters: list số kênh ở mỗi tầng conv (mặc định [32,64,128]).
    kernels: list kernel size tương ứng (mặc định [7,5,3]).
    """

    def __init__(self, in_channels: int = 6, n_classes: int = 12,
                 filters: list[int] | None = None,
                 kernels: list[int] | None = None,
                 dropout: float = 0.3,
                 emb_dim: int | None = None):
        super().__init__()
        filters = filters or [32, 64, 128]
        kernels = kernels or [7, 5, 3]
        assert len(filters) == len(kernels), "filters và kernels phải cùng độ dài"

        layers = []
        c_in = in_channels
        for i, (c_out, k) in enumerate(zip(filters, kernels)):
            layers += [
                nn.Conv1d(c_in, c_out, kernel_size=k, padding=k // 2),
                nn.BatchNorm1d(c_out),
                nn.ReLU(inplace=True),
            ]
            if i < len(filters) - 1:
                layers.append(nn.MaxPool1d(2))
            c_in = c_out
        layers.append(nn.AdaptiveAvgPool1d(1))
        self.features = nn.Sequential(*layers)

        self.emb_dim = emb_dim or filters[-1]
        if emb_dim is not None and emb_dim != filters[-1]:
            self.proj = nn.Linear(filters[-1], emb_dim)
        else:
            self.proj = nn.Identity()
        self.dropout = nn.Dropout(dropout)
        self.head = nn.Linear(self.emb_dim, n_classes)

    def forward(self, x: torch.Tensor, return_embedding: bool = False):
        z = self.features(x).squeeze(-1)
        z = self.proj(z)
        if return_embedding:
            return z
        return self.head(self.dropout(z))

    def embed(self, x: torch.Tensor) -> torch.Tensor:
        return self.forward(x, return_embedding=True)


class _ResBlock1D(nn.Module):
    def __init__(self, c_in: int, c_out: int, k: int = 3, downsample: bool = False):
        super().__init__()
        stride = 2 if downsample else 1
        self.conv1 = nn.Conv1d(c_in, c_out, k, stride=stride, padding=k // 2)
        self.bn1 = nn.BatchNorm1d(c_out)
        self.conv2 = nn.Conv1d(c_out, c_out, k, stride=1, padding=k // 2)
        self.bn2 = nn.BatchNorm1d(c_out)
        if downsample or c_in != c_out:
            self.short = nn.Sequential(
                nn.Conv1d(c_in, c_out, 1, stride=stride),
                nn.BatchNorm1d(c_out),
            )
        else:
            self.short = nn.Identity()

    def forward(self, x):
        h = F.relu(self.bn1(self.conv1(x)), inplace=True)
        h = self.bn2(self.conv2(h))
        return F.relu(h + self.short(x), inplace=True)


class ResNet1D(nn.Module):
    """ResNet 1D nhỏ, n_stage = len(filters)."""

    def __init__(self, in_channels: int = 6, n_classes: int = 12,
                 filters: list[int] | None = None, dropout: float = 0.3,
                 emb_dim: int | None = None):
        super().__init__()
        filters = filters or [64, 128, 256]
        self.stem = nn.Sequential(
            nn.Conv1d(in_channels, filters[0], kernel_size=7, padding=3),
            nn.BatchNorm1d(filters[0]),
            nn.ReLU(inplace=True),
        )
        blocks = []
        c = filters[0]
        for i, c_out in enumerate(filters):
            blocks.append(_ResBlock1D(c, c_out, downsample=(i > 0)))
            blocks.append(_ResBlock1D(c_out, c_out, downsample=False))
            c = c_out
        self.blocks = nn.Sequential(*blocks)
        self.pool = nn.AdaptiveAvgPool1d(1)
        self.emb_dim = emb_dim or filters[-1]
        if emb_dim is not None and emb_dim != filters[-1]:
            self.proj = nn.Linear(filters[-1], emb_dim)
        else:
            self.proj = nn.Identity()
        self.dropout = nn.Dropout(dropout)
        self.head = nn.Linear(self.emb_dim, n_classes)

    def forward(self, x, return_embedding: bool = False):
        z = self.pool(self.blocks(self.stem(x))).squeeze(-1)
        z = self.proj(z)
        if return_embedding:
            return z
        return self.head(self.dropout(z))

    def embed(self, x):
        return self.forward(x, return_embedding=True)


class _TCNBlock(nn.Module):
    def __init__(self, c_in: int, c_out: int, k: int, dilation: int, dropout: float):
        super().__init__()
        pad = (k - 1) * dilation
        self.conv1 = nn.Conv1d(c_in, c_out, k, padding=pad, dilation=dilation)
        self.conv2 = nn.Conv1d(c_out, c_out, k, padding=pad, dilation=dilation)
        self.drop = nn.Dropout(dropout)
        self.short = nn.Conv1d(c_in, c_out, 1) if c_in != c_out else nn.Identity()
        self.pad = pad

    def _crop(self, x):
        return x[..., :-self.pad] if self.pad > 0 else x

    def forward(self, x):
        h = F.relu(self._crop(self.conv1(x)), inplace=True)
        h = self.drop(h)
        h = self._crop(self.conv2(h))
        return F.relu(h + self.short(x), inplace=True)


class TCN(nn.Module):
    """Temporal Convolutional Network."""

    def __init__(self, in_channels: int = 6, n_classes: int = 12,
                 channels: list[int] | None = None,
                 kernel_size: int = 5, dropout: float = 0.2,
                 emb_dim: int | None = None):
        super().__init__()
        channels = channels or [64, 64, 128, 128]
        blocks = []
        c = in_channels
        for i, c_out in enumerate(channels):
            blocks.append(_TCNBlock(c, c_out, k=kernel_size,
                                    dilation=2 ** i, dropout=dropout))
            c = c_out
        self.tcn = nn.Sequential(*blocks)
        self.pool = nn.AdaptiveAvgPool1d(1)
        self.emb_dim = emb_dim or channels[-1]
        if emb_dim is not None and emb_dim != channels[-1]:
            self.proj = nn.Linear(channels[-1], emb_dim)
        else:
            self.proj = nn.Identity()
        self.dropout = nn.Dropout(dropout)
        self.head = nn.Linear(self.emb_dim, n_classes)

    def forward(self, x, return_embedding: bool = False):
        z = self.pool(self.tcn(x)).squeeze(-1)
        z = self.proj(z)
        if return_embedding:
            return z
        return self.head(self.dropout(z))

    def embed(self, x):
        return self.forward(x, return_embedding=True)


class BiLSTMAttn(nn.Module):
    """BiLSTM + attention pooling."""

    def __init__(self, in_channels: int = 6, n_classes: int = 12,
                 hidden: int = 128, num_layers: int = 2, dropout: float = 0.3,
                 emb_dim: int | None = None):
        super().__init__()
        self.lstm = nn.LSTM(in_channels, hidden, num_layers=num_layers,
                            batch_first=True, bidirectional=True,
                            dropout=dropout if num_layers > 1 else 0.0)
        self.attn = nn.Linear(2 * hidden, 1)
        self.emb_dim = emb_dim or 2 * hidden
        if emb_dim is not None and emb_dim != 2 * hidden:
            self.proj = nn.Linear(2 * hidden, emb_dim)
        else:
            self.proj = nn.Identity()
        self.dropout = nn.Dropout(dropout)
        self.head = nn.Linear(self.emb_dim, n_classes)

    def forward(self, x, return_embedding: bool = False):
        # x: (B, C, T) → (B, T, C)
        x = x.transpose(1, 2)
        h, _ = self.lstm(x)
        a = torch.softmax(self.attn(h).squeeze(-1), dim=1)
        z = (h * a.unsqueeze(-1)).sum(dim=1)
        z = self.proj(z)
        if return_embedding:
            return z
        return self.head(self.dropout(z))

    def embed(self, x):
        return self.forward(x, return_embedding=True)


def make_model(cfg: dict, in_channels: int, n_classes: int) -> nn.Module:
    """Factory: cfg = {'type': 'cnn'|'resnet'|'tcn'|'bilstm', ...}."""
    t = cfg.get("type", "cnn").lower()
    if t == "cnn":
        return CNN1D(
            in_channels=in_channels, n_classes=n_classes,
            filters=cfg.get("filters", [32, 64, 128]),
            kernels=cfg.get("kernels", [7, 5, 3]),
            dropout=cfg.get("dropout", 0.3),
            emb_dim=cfg.get("emb_dim"),
        )
    if t == "resnet":
        return ResNet1D(
            in_channels=in_channels, n_classes=n_classes,
            filters=cfg.get("filters", [64, 128, 256]),
            dropout=cfg.get("dropout", 0.3),
            emb_dim=cfg.get("emb_dim"),
        )
    if t == "tcn":
        return TCN(
            in_channels=in_channels, n_classes=n_classes,
            channels=cfg.get("channels", [64, 64, 128, 128]),
            kernel_size=cfg.get("kernel_size", 5),
            dropout=cfg.get("dropout", 0.2),
            emb_dim=cfg.get("emb_dim"),
        )
    if t == "bilstm":
        return BiLSTMAttn(
            in_channels=in_channels, n_classes=n_classes,
            hidden=cfg.get("hidden", 128),
            num_layers=cfg.get("num_layers", 2),
            dropout=cfg.get("dropout", 0.3),
            emb_dim=cfg.get("emb_dim"),
        )
    raise ValueError(f"Unknown model type: {t}")
