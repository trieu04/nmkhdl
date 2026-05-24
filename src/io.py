"""I/O: parse filename, load CSV, build manifest."""
from __future__ import annotations
import re
from pathlib import Path
import pandas as pd

from .config import RAW_DIR, INTERIM_DIR, INERTIAL_CHANNELS

INERTIAL_RE = re.compile(
    r"^inertial_(?P<activity>sitting|standing|walking)"
    r"(?:_s(?P<session>\d+))?"
    r"(?:_att(?P<attempt>\d+))?"
    r"(?:_r(?P<rep>\d+))?\.csv$"
)
KEY_RE = re.compile(
    r"^keystroke"
    r"(?:_s(?P<session>\d+))?"
    r"(?:_att(?P<attempt>\d+))?"
    r"(?:_r(?P<rep>\d+))?\.csv$"
)
TOUCH_RE = re.compile(
    r"^touch_(?P<kind>tap|scroll)"
    r"(?:_s(?P<session>\d+))?"
    r"(?:_att(?P<attempt>\d+))?"
    r"(?:_r(?P<rep>\d+))?\.csv$"
)


def parse_filename(fname: str) -> dict | None:
    for mod, rx in [("inertial", INERTIAL_RE), ("keystroke", KEY_RE), ("touch", TOUCH_RE)]:
        m = rx.match(fname)
        if m:
            d = m.groupdict()
            d["modality"] = mod
            return d
    return None


def _estimate_fs(df: pd.DataFrame) -> float | None:
    if "timestamp_ns" not in df.columns:
        return None
    ts = df["timestamp_ns"].to_numpy()
    if len(ts) < 2 or ts.max() <= 0:
        return None
    dt = (ts[-1] - ts[0]) / (len(ts) - 1) / 1e9
    return 1.0 / dt if dt > 0 else None


def build_manifest(root: Path = RAW_DIR) -> pd.DataFrame:
    """Quét toàn bộ user*/*.csv, trả về 1 dòng/file với meta + n_rows + fs_est."""
    rows = []
    for user_dir in sorted(Path(root).glob("user*")):
        if not user_dir.is_dir():
            continue
        user = user_dir.name
        for fp in sorted(user_dir.glob("*.csv")):
            if fp.name == "metadata.csv":
                continue
            meta = parse_filename(fp.name)
            if meta is None:
                rows.append({"user": user, "file": fp.name, "modality": "UNPARSED"})
                continue
            try:
                df = pd.read_csv(fp)
            except Exception as e:
                rows.append({"user": user, "file": fp.name, "modality": meta["modality"],
                             "n_rows": 0, "error": str(e)})
                continue
            fs = _estimate_fs(df) if meta["modality"] == "inertial" else None
            mag_zero_ratio = None
            if meta["modality"] == "inertial" and {"mag_x", "mag_y", "mag_z"}.issubset(df.columns):
                mag_zero_ratio = float((df[["mag_x", "mag_y", "mag_z"]].abs().sum(axis=1) == 0).mean())
            rows.append({
                "user": user, "file": fp.name, "modality": meta["modality"],
                "activity": meta.get("activity"),
                "session": meta.get("session"),
                "attempt": meta.get("attempt"),
                "rep": meta.get("rep"),
                "kind": meta.get("kind"),
                "n_rows": len(df), "fs_est": fs,
                "mag_zero_ratio": mag_zero_ratio,
            })
    return pd.DataFrame(rows)


def load_inertial(user: str, fname: str, root: Path = RAW_DIR) -> pd.DataFrame:
    fp = Path(root) / user / fname
    df = pd.read_csv(fp, usecols=lambda c: c in INERTIAL_CHANNELS + ["timestamp_ns", "activity"])
    return df


def load_keystroke(user: str, fname: str, root: Path = RAW_DIR) -> pd.DataFrame:
    return pd.read_csv(Path(root) / user / fname)


def load_touch(user: str, fname: str, root: Path = RAW_DIR) -> pd.DataFrame:
    return pd.read_csv(Path(root) / user / fname)


def load_metadata(user: str, root: Path = RAW_DIR) -> dict:
    fp = Path(root) / user / "metadata.csv"
    if not fp.exists():
        return {}
    df = pd.read_csv(fp)
    return dict(zip(df["field"], df["value"]))


def save_manifest(df: pd.DataFrame, out: Path = INTERIM_DIR / "manifest.csv") -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    return out


if __name__ == "__main__":
    m = build_manifest()
    p = save_manifest(m)
    print(f"Manifest: {p}  ({len(m)} rows)")
    print(m.groupby("modality").size())
    unparsed = m[m["modality"] == "UNPARSED"]
    if len(unparsed):
        print("UNPARSED files:")
        print(unparsed[["user", "file"]])
