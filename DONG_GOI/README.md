# README — Hệ thống định danh người dùng qua hành vi điện thoại

Đồ án môn **Nhập môn Khoa học dữ liệu (IT4142)**.

## 1. Mô tả ngắn

Pipeline ML hoàn chỉnh: từ CSV thô (15 user, dữ liệu cảm biến và gõ phím) → tiền xử lý DSP → 2 mô hình song song (CNN 1D, Random Forest) → đánh giá closed-set + open-set.

## 2. Yêu cầu môi trường

- **OS**: Linux / macOS / Windows (đã test trên Ubuntu 24).
- **Python** 3.10+ (test trên 3.12).
- **RAM** ≥ 4 GB.
- **Đĩa** ≈ 1.5 GB (raw + processed + models).

## 3. Cài đặt

```bash
# 1. Clone / extract source
unzip nmkhdl_source.zip
cd NMKHDL

# 2. Tạo virtualenv (PEP 668 yêu cầu)
python3 -m venv venv
source venv/bin/activate           # Windows: venv\Scripts\activate

# 3. Cài thư viện (dùng mirror chính chủ pypi)
pip install -r requirements.txt --index-url https://pypi.org/simple
```

### Các thư viện chính (đã liệt kê ở `requirements.txt`)

| Gói | Phiên bản tối thiểu | Vai trò |
| --- | --- | --- |
| numpy | 1.24 | mảng đa chiều |
| pandas | 2.0 | DataFrame, đọc CSV |
| scipy | 1.10 | lọc Butterworth, FFT, resample |
| scikit-learn | 1.3 | RandomForest, StratifiedGroupKFold, metrics |
| torch | 2.0 | CNN 1D |
| matplotlib / seaborn | 3.7 / 0.12 | hình ảnh, confusion matrix |
| tqdm, joblib | mới nhất | tiện ích |

## 4. Cấu trúc thư mục

```
NMKHDL/
├── rootdata - Copy/              # Dữ liệu thô (15 user, 185 CSV dùng trong pipeline cuối)
├── src/                          # Mã nguồn
│   ├── config.py                 # Hằng số, đường dẫn
│   ├── io.py                     # Đọc CSV + build manifest
│   ├── preprocess.py             # Filter + sliding window
│   ├── features.py               # Đặc trưng thủ công + keystroke
│   ├── datasets.py               # PyTorch Dataset + augmentation
│   ├── models.py                 # Kiến trúc CNN 1D
│   ├── train.py                  # 3-fold CV trainer
│   ├── openset.py                # Softmax / Mahalanobis open-set
│   └── evaluate.py               # RF baseline + confusion + figures
├── scripts/
│   └── pptx_to_md.py             # Trích nội dung slide ra Markdown
├── data/
│   ├── interim/                  # manifest.csv, feat_*.csv
│   └── processed/                # windows.npz
├── models/                       # Checkpoint mỗi fold + cv_summary.json
├── reports/
│   ├── *.json                    # Số liệu open-set & evaluate
│   └── figures/                  # PNG confusion / per-activity
├── docs/slides_md/               # Slide khoá học đã trích text
├── report.md                     # Báo cáo chính
├── PRESENTATION.md               # Tài liệu thuyết trình chi tiết
├── STUDY_PLAN.md                 # Kế hoạch nghiên cứu + map slide
├── README.md                     # File này
└── requirements.txt
```

## 5. Cách chạy end-to-end

### 5.1 Chạy toàn bộ pipeline (~25 phút trên CPU)

```bash
source venv/bin/activate

# Bước 1: Quét rootdata, sinh manifest
python -m src.io
# → data/interim/manifest.csv

# Bước 2: Lọc + cửa sổ hoá, tạo tensor windows.npz
python -m src.preprocess
# → data/processed/windows.npz (39018, 128, 6)

# Bước 3: Trích đặc trưng keystroke (cho phân tích thêm)
python -m src.features
# → data/interim/feat_keystroke.csv

# Bước 4: Huấn luyện CNN 1D 3-fold CV
python -m src.train --epochs 40 --folds 3
# → models/fold{0,1,2}/model.pt, models/cv_summary.json

# Bước 5: Đánh giá open-set
python -m src.openset
# → reports/openset_results.json

# Bước 6: Random Forest baseline + confusion matrix + per-activity
python -m src.evaluate
# → reports/evaluate_results.json, reports/figures/*.png
```

### 5.2 Chạy nhanh (chỉ kiểm tra)

```bash
python -m src.train --epochs 2 --folds 2     # ~2 phút
python -m src.openset
python -m src.evaluate
```

## 6. Đầu ra mong đợi

Sau khi chạy đủ bước 1–6:

```
models/cv_summary.json            # mean_macroF1 ≈ 0.65
reports/evaluate_results.json     # RF macroF1 ≈ 0.78
reports/openset_results.json      # softmax AUROC ≈ 0.66
reports/figures/cnn_confusion.png
reports/figures/cnn_per_activity.png
```

## 7. Cách thay đổi cấu hình

Mọi hằng số đều ở `src/config.py`:

| Biến | Ý nghĩa | Mặc định |
| --- | --- | --- |
| `WINDOW_SIZE` | Độ dài cửa sổ (mẫu) | 128 |
| `WINDOW_STRIDE` | Bước trượt | 64 |
| `FS` | Tần số chuẩn hoá | 50.0 Hz |
| `LOWPASS_CUTOFF` | Cutoff Butterworth lowpass | 20.0 Hz |
| `HIGHPASS_GRAVITY` | Cutoff highpass tách trọng lực | 0.3 Hz |
| `UNKNOWN_USERS` | Danh sách user dành cho open-set | `[userD, userE, userI]` |
| `SEED` | Random seed | 42 |

## 8. Giải quyết sự cố thường gặp

| Triệu chứng | Cách khắc phục |
| --- | --- |
| `error: externally-managed-environment` khi `pip install` | Bật venv: `source venv/bin/activate` rồi cài lại. |
| `pip` báo "no matching distribution" | Thêm `--index-url https://pypi.org/simple`. |
| Lỗi `CUDA initialization` | Bỏ qua — code tự fallback sang CPU. |
| `val thiếu class {N} — skip fold` | Giảm `--folds` xuống 3 (user ít file). |
| `read-only ndarray` trong features | Đã fix bằng `.copy()`; nếu lặp lại, kiểm tra pandas version. |

## 9. Trích dẫn

- **PyTorch**: Paszke et al., *PyTorch: An Imperative Style, High-Performance Deep Learning Library*, NeurIPS 2019.
- **scikit-learn**: Pedregosa et al., *Scikit-learn: Machine Learning in Python*, JMLR 2011.
- **scipy.signal.butter**: Virtanen et al., *SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python*, Nature Methods 2020.
- **UCI HAR Dataset** (cảm hứng thiết kế cửa sổ 2.56 s @ 50 Hz): Anguita et al., 2013.

## 10. Tài liệu khác

- [report.md](report.md) — báo cáo đồ án (đáp ứng đủ 7 mục L0).
- [PRESENTATION.md](PRESENTATION.md) — tài liệu thuyết trình chi tiết.
- [STUDY_PLAN.md](STUDY_PLAN.md) — kế hoạch học tập + ánh xạ slide IT4142.

## 11. Liên hệ nhóm

Xem trang đầu [report.md](report.md).
