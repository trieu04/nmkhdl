**ĐẠI HỌC BÁCH KHOA HÀ NỘI**

Trường Công nghệ Thông tin và Truyền thông

**BÁO CÁO QUÁ TRÌNH**

**Đề tài: _Phát triển hệ thống định danh người dùng qua hành vi sử dụng điện thoại_**

Môn: Nhập môn Khoa học dữ liệu - IT4930

Lớp: 166129

Giáo viên hướng dẫn: Nguyễn Đức Anh

Thành viên:

| Lương Mạnh Tường<br><br>Bùi Minh Tuấn<br><br>Trương Quốc Triệu<br><br>Nguyễn Đức Thành<br><br>Nguyễn Anh Tuấn<br><br>Vũ Ngọc Lâm<br><br>Vũ Nhật Quang<br><br>Mai Văn Đăng<br><br>Nguyễn Đình Thành | 20225949<br><br>20225678<br><br>20225941<br><br>20225930<br><br>20225772<br><br>20225645<br><br>20225761<br><br>20225699<br><br>20225670 |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |

**Mục lục**

[CHƯƠNG 1. GIỚI THIỆU ĐỀ TÀI 3](#_Toc226750845)

[1.1. Bối cảnh 3](#_Toc226750846)

[1.2. Mục tiêu đề tài 3](#_Toc226750847)

[CHƯƠNG 2. CƠ SỞ LÝ THUYẾT 4](#_Toc226750848)

[2.1. Sinh trắc học hành vi 4](#_Toc226750849)

[2.2. Dữ liệu cảm biến trên thiết bị Android 4](#_Toc226750850)

[2.3. Mô hình CNN 1D cho dữ liệu chuỗi thời gian 4](#_Toc226750851)

[CHƯƠNG 3. TIẾN ĐỘ THỰC HIỆN ĐỀ TÀI 5](#_Toc226750852)

[3.1. Tổng quan tiến độ 5](#_Toc226750853)

[3.2. Các bước thực hiện của hệ thống 5](#_Toc226750854)

[3.3. Công việc đã thực hiện 6](#_Toc226750855)

[1\. Nghiên cứu cơ sở lý thuyết 6](#_Toc226750856)

[2\. Phát triển ứng dụng thu thập dữ liệu 6](#_Toc226750857)

[3.4. Kế hoạch thực hiện tiếp theo 6](#_Toc226750858)

# CHƯƠNG 1. GIỚI THIỆU ĐỀ TÀI

## 1.1. Bối cảnh

Trong những năm gần đây, các phương pháp xác thực người dùng trên thiết bị di động ngày càng phát triển nhằm tăng cường tính bảo mật. Ngoài các phương pháp truyền thống như mật khẩu, vân tay hoặc nhận diện khuôn mặt, một hướng nghiên cứu mới là **sinh trắc học hành vi (Behavioral Biometrics).**

Sinh trắc học hành vi khai thác các đặc điểm hành vi của người dùng khi tương tác với thiết bị, chẳng hạn như cách cầm điện thoại, cách di chuyển thiết bị hoặc các chuyển động tay. Những hành vi này có thể được thu thập thông qua các cảm biến có sẵn trên điện thoại thông minh như **gia tốc kế (Accelerometer)** và **con quay hồi chuyển (Gyroscope)**.

Việc sử dụng dữ liệu cảm biến để nhận diện người dùng giúp hệ thống có thể xác thực người dùng một cách tự nhiên và liên tục trong quá trình sử dụng thiết bị.

## 1.2. Mục tiêu đề tài

Đề tài "**Phát triển hệ thống định danh người dùng qua hành vi sử dụng điện thoại**" hướng tới việc xây dựng một hệ thống nhận diện người dùng dựa trên hành động **rút điện thoại lên để nghe máy**.

Hệ thống sẽ sử dụng dữ liệu từ các cảm biến chuyển động của điện thoại và áp dụng mô hình học sâu để học đặc trưng hành vi của từng người dùng.

Các mục tiêu chính của đề tài gồm:

- Xây dựng ứng dụng Android để thu thập dữ liệu cảm biến.
- Thu thập dữ liệu hành vi người dùng khi thực hiện động tác nghe điện thoại.
- Xây dựng mô hình học máy để nhận diện người dùng.
- Áp dụng cơ chế phát hiện người dùng không thuộc tập đã đăng ký.
- Đánh giá khả năng ứng dụng của hệ thống trong việc hỗ trợ mở khóa điện thoại.

# CHƯƠNG 2. CƠ SỞ LÝ THUYẾT

## 2.1. Sinh trắc học hành vi

Sinh trắc học hành vi (Behavioral Biometrics) là phương pháp xác thực người dùng dựa trên các đặc điểm hành vi trong quá trình sử dụng thiết bị.

Các đặc điểm này có thể bao gồm:

- Nhịp gõ phím
- Chuyển động tay
- Dáng đi
- Dữ liệu từ các cảm biến chuyển động

Bằng cách phân tích các dữ liệu này, hệ thống có thể xây dựng một hồ sơ hành vi riêng cho mỗi người dùng và sử dụng nó để nhận diện người dùng trong các lần sử dụng tiếp theo.

Phương pháp này có ưu điểm là không yêu cầu người dùng thực hiện thao tác xác thực riêng biệt và có thể hoạt động trong nền.

## 2.2. Dữ liệu cảm biến trên thiết bị Android

Các điện thoại thông minh hiện nay được trang bị nhiều loại cảm biến giúp thu thập dữ liệu về chuyển động của thiết bị.

Trong đề tài này, hệ thống sử dụng ba loại cảm biến chính:

- **Accelerometer:** đo gia tốc của thiết bị theo ba trục x, y, z.
- **Gyroscope:** đo tốc độ xoay của thiết bị quanh các trục.
- **Proximity Sensor:** đo khoảng cách giữa thiết bị và vật thể phía trước màn hình.

Dữ liệu từ các cảm biến này tạo thành **chuỗi thời gian nhiều chiều**, phản ánh hành vi sử dụng thiết bị của người dùng.

## 2.3. Mô hình CNN 1D cho dữ liệu chuỗi thời gian

Dữ liệu cảm biến được thu thập theo thời gian, vì vậy chúng được xem là **dữ liệu chuỗi thời gian (time-series)**.

Trong đề tài này, nhóm sử dụng **mạng nơ-ron tích chập một chiều (CNN 1D)** để học các đặc trưng từ chuỗi dữ liệu cảm biến.

CNN 1D có một số ưu điểm:

- Có khả năng tự động trích xuất đặc trưng từ dữ liệu.
- Huấn luyện nhanh và hiệu quả với dữ liệu chuỗi thời gian.
- Phù hợp để triển khai trên thiết bị di động.

# CHƯƠNG 3. TIẾN ĐỘ THỰC HIỆN ĐỀ TÀI

## 3.1. Tổng quan tiến độ

Đề tài được thực hiện theo nhiều giai đoạn từ nghiên cứu lý thuyết, thu thập dữ liệu, xây dựng mô hình đến triển khai hệ thống.

Tính đến thời điểm hiện tại, nhóm đã hoàn thành các bước chuẩn bị ban đầu, bao gồm nghiên cứu cơ sở lý thuyết và xây dựng ứng dụng Android để thu thập dữ liệu cảm biến. Hiện tại, nhóm đang trong giai đoạn **thu thập dữ liệu từ người dùng thử nghiệm.**

## 3.2. Các bước thực hiện của hệ thống

Quá trình thực hiện đề tài được chia thành các bước chính sau:

| **Bước** | **Nội dung**                                 | **Trạng thái** |
| -------- | -------------------------------------------- | -------------- |
| 1        | Nghiên cứu tài liệu và cơ sở lý thuyết       | Đã hoàn thành  |
| 2        | Khảo sát cảm biến trên Android               | Đã hoàn thành  |
| 3        | Thiết kế hệ thống thu thập dữ liệu           | Đã hoàn thành  |
| 4        | Phát triển ứng dụng Android thu thập dữ liệu | Đã hoàn thành  |
| 5        | Thu thập dữ liệu người dùng                  | Đã hoàn thành  |
| 6        | Tiền xử lý dữ liệu cảm biến                  | Đã hoàn thành  |
| 7        | Xây dựng mô hình CNN 1D                      | Đã hoàn thành  |
| 8        | Đánh giá hệ thống                            | Đã hoàn thành  |

Bảng trên cho thấy đề tài hiện đang ở **giai đoạn thu thập dữ liệu**, đây là bước quan trọng để xây dựng tập dữ liệu cho việc huấn luyện mô hình.

## 3.3. Công việc đã thực hiện

### 1\. Nghiên cứu cơ sở lý thuyết

Nhóm đã tìm hiểu các khái niệm liên quan đến sinh trắc học hành vi, dữ liệu cảm biến trên thiết bị di động và các phương pháp học máy sử dụng cho dữ liệu chuỗi thời gian.

### 2\. Phát triển ứng dụng thu thập dữ liệu

Nhóm đã xây dựng một ứng dụng Android có chức năng thu thập dữ liệu từ các cảm biến chuyển động của điện thoại.

Ứng dụng ghi lại dữ liệu từ:

- Accelerometer
- Gyroscope
- Proximity Sensor

Dữ liệu được lưu lại để phục vụ cho việc xây dựng tập dữ liệu huấn luyện.

## 3.4. Kế hoạch thực hiện tiếp theo

Trong giai đoạn tiếp theo, nhóm sẽ thực hiện các công việc sau:

- Hoàn thành việc thu thập dữ liệu từ người dùng.
- Thực hiện tiền xử lý dữ liệu cảm biến.
- Xây dựng và huấn luyện mô hình CNN 1D.
- Đánh giá khả năng nhận diện của hệ thống.

# CHƯƠNG 4. TRIỂN KHAI HỆ THỐNG

## 4.1. Dữ liệu thực tế

Sau khi hoàn thành thu thập, bộ dữ liệu cuối cùng gồm **15 người dùng (userA–userQ)** với tổng cộng **325 file CSV** trải đều trên ba modality:

- **Inertial (cảm biến quán tính)**: gia tốc kế và con quay hồi chuyển, kèm cảm biến từ trường. Đây là modality chính, gồm các kịch bản sitting, standing, walking.
- **Keystroke**: nhật ký gõ phím (timestamp các sự kiện DOWN/UP).
- **Touch**: log chạm và cuộn màn hình.

Bảng manifest tự sinh (`data/interim/manifest.csv`) chuẩn hoá tên file theo nhiều schema (`_s{S}_att{n}.csv`, `_s{S}_r{m}.csv`, …) và rút ra: người dùng, modality, hoạt động, session, attempt/rep, fs đo lường. Tần số lấy mẫu thực tế của cảm biến quán tính được xác định **fs ≈ 50 Hz** (timestamp_ns chênh ~20 ms cho 14/15 người dùng). Riêng userA bị lỗi phiên bản app (timestamp_ns = 0, magnetometer = 0) nên hệ thống chỉ dùng 6 kênh `acc_xyz + gyro_xyz`.

## 4.2. Tiền xử lý

Pipeline tiền xử lý cho dữ liệu quán tính được cài đặt trong `src/preprocess.py`:

1. Điền NaN bằng ffill/bfill.
2. Resample về 50 Hz bằng `scipy.signal.resample_poly` nếu fs lệch >1 Hz.
3. **Lowpass Butterworth** bậc 4, cutoff 20 Hz: loại nhiễu cao tần.
4. **Highpass Butterworth** bậc 4, cutoff 0.3 Hz, áp dụng riêng cho 3 trục `acc_*`: tách thành phần trọng lực khỏi gia tốc tuyến tính.
5. **Trượt cửa sổ** 128 mẫu (2.56 s), bước nhảy 64 (chồng lấp 50%).

Để cân bằng class, mỗi file bị giới hạn tối đa 300 cửa sổ, lấy đều bằng `np.linspace`. Kết quả: tensor `X` kích thước **(39018, 128, 6)** lưu tại `data/processed/windows.npz`.

## 4.3. Tách tập

Dữ liệu được chia theo nguyên tắc nghiêm ngặt:

- **Người dùng "chưa biết" (unknown)**: userD, userE, userI — dành riêng cho đánh giá open-set, hoàn toàn không tham gia huấn luyện.
- **Phần còn lại** (12 người): dùng `StratifiedGroupKFold` với `groups = "{user}__{filename}"` — toàn bộ cửa sổ của cùng một file luôn cùng nằm ở train hoặc val, ngăn rò rỉ phiên ghi. Số fold = 3 (do userQ chỉ có 3 file ghi).

## 4.4. Mô hình CNN 1D

Kiến trúc trong `src/models.py`:

```
Conv1d(6→32, k=7) → BN → ReLU
Conv1d(32→64, k=5) → BN → ReLU → MaxPool(2)
Conv1d(64→128, k=3) → BN → ReLU → AdaptiveAvgPool(1)
Dropout(0.3) → Linear(128 → 12)
```

Vector embedding 128-d được tách riêng để dùng cho open-set. Huấn luyện: Adam (lr=1e-3, wd=1e-4), cross-entropy có trọng số 1/freq, 40 epoch, batch size 128. Augmentation thời gian thực: jitter σ=0.02, scale 0.9–1.1, rotation 3D θ ≤ 0.1 rad áp dụng đồng thời cho cả acc và gyro.

## 4.5. Baseline Random Forest

Để đối chứng, hệ thống còn trích **62 đặc trưng thủ công** mỗi cửa sổ (mean, std, mad, min, max, iqr, energy, fft_entropy, fft_dom_freq cho 6 kênh; correlation chéo; SMA) và huấn luyện Random Forest 300 cây, `class_weight=balanced_subsample`, scaler chuẩn.

## 4.6. Đánh giá open-set

`src/openset.py` triển khai hai chiến lược:

- **Softmax max-prob** ngưỡng hoá: điểm "known" = max softmax.
- **Mahalanobis** trên embedding 128-d: ước lượng Gaussian theo class trên tập train, điểm "known" = -min(Mahalanobis distance).

Chỉ số sử dụng: AUROC unknown-vs-known, TPR@FPR=5 %.

# CHƯƠNG 5. KẾT QUẢ THỰC NGHIỆM

## 5.1. Closed-set (12 người đã biết)

Phân chia 3-fold theo file, lấy trung bình ± std trên các fold:

| Mô hình             | macro-F1 (val)     | accuracy (val) |
| ------------------- | ------------------ | -------------- |
| **Random Forest**   | **0.785 ± 0.020**  | **0.801**      |
| CNN 1D (40 epoch)   | 0.645 ± 0.018      | 0.663          |

Trên giao thức group-by-file rất nghiêm khắc, baseline thủ công + RF **vượt CNN** — phù hợp với nhận xét quen thuộc trong văn liệu HAR khi lượng phiên ghi/người ít: đặc trưng thống kê tay nắm được cấu trúc tần số ổn định giữa các phiên, trong khi CNN dễ chạy theo nhiễu cấp phiên. Đây là kết quả thẳng thắn dùng để định hướng cải tiến (xem 5.4).

Hiệu năng CNN theo hoạt động:

| Activity   | n cửa sổ | accuracy | macro-F1 |
| ---------- | -------- | -------- | -------- |
| sitting    | 8568     | 0.629    | 0.609    |
| standing   | 9308     | 0.682    | 0.663    |
| walking    | 11849    | 0.673    | 0.648    |

Walking và standing cho tín hiệu phân biệt người dùng tốt hơn sitting (chuyển động ít hơn → ít sai khác giữa người).

## 5.2. Confusion matrix

Ma trận nhầm lẫn tổng hợp 3 fold cho CNN: `reports/figures/cnn_confusion.png`. Biểu đồ per-activity: `reports/figures/cnn_per_activity.png`.

## 5.3. Open-set (D/E/I chưa biết)

Trung bình trên 3 fold:

| Phương pháp     | AUROC (known vs unknown) | TPR @ FPR = 5 % |
| --------------- | ------------------------ | --------------- |
| Softmax max-prob | **0.659 ± 0.020**       | **0.273**       |
| Mahalanobis      | 0.610 ± 0.020            | 0.062           |

Softmax đơn giản tốt hơn Mahalanobis ở giao thức này — do embedding học từ dữ liệu nhỏ chưa đủ tách bạch để các Gaussian theo class ổn định. AUROC 0.66 cho thấy hệ thống có tín hiệu phân biệt người chưa biết nhưng còn khoảng cách lớn so với mức triển khai thực (mong muốn ≥ 0.85).

## 5.4. Phân tích và hướng cải tiến

1. **Augmentation mạnh hơn / SimCLR pretraining**: tăng đa dạng phiên ghi giả lập để CNN không phụ thuộc đặc trưng của một phiên cụ thể.
2. **Fusion**: kết hợp CNN trên cảm biến với đặc trưng keystroke/touch (đã trích sẵn ở `data/interim/feat_*.csv`) ở mức người dùng — cải thiện đặc biệt khi inertial yếu.
3. **Tăng số phiên ghi mỗi người** (chuẩn ≥ 5 phiên/người để StratifiedGroupKFold 5-fold làm việc bền vững).
4. **Loại bỏ userA hoặc thu lại** vì lỗi timestamp/magnetometer.

# CHƯƠNG 6. CHỨC NĂNG HỆ THỐNG VÀ CÁCH SỬ DỤNG

## 6.1. Các chức năng chính

Hệ thống được tổ chức thành 6 chức năng dòng lệnh độc lập, dễ kiểm thử từng phần:

| # | Lệnh CLI | Chức năng | Đầu ra |
| --- | --- | --- | --- |
| 1 | `python -m src.io` | Quét toàn bộ `rootdata - Copy/`, phân tích filename, sinh manifest | `data/interim/manifest.csv` |
| 2 | `python -m src.preprocess` | Lọc Butterworth + trượt cửa sổ → tensor huấn luyện | `data/processed/windows.npz` |
| 3 | `python -m src.features` | Trích đặc trưng keystroke + touch (cho phân tích bổ sung) | `data/interim/feat_*.csv` |
| 4 | `python -m src.train --epochs 40 --folds 3` | Huấn luyện CNN 1D với StratifiedGroupKFold | `models/foldK/model.pt`, `models/cv_summary.json` |
| 5 | `python -m src.openset` | Đánh giá open-set bằng softmax + Mahalanobis | `reports/openset_results.json` |
| 6 | `python -m src.evaluate` | Random Forest baseline + confusion matrix + per-activity | `reports/evaluate_results.json`, `reports/figures/*.png` |

## 6.2. Cách dùng nhanh

```bash
source venv/bin/activate
pip install -r requirements.txt --index-url https://pypi.org/simple
python -m src.io && python -m src.preprocess && python -m src.features
python -m src.train --epochs 40 --folds 3
python -m src.openset
python -m src.evaluate
```

Toàn bộ pipeline chạy được trên CPU khoảng 25–30 phút với dataset hiện tại.

## 6.3. Tham số có thể điều chỉnh

Tập trung trong `src/config.py`:

- `WINDOW_SIZE = 128`, `WINDOW_STRIDE = 64` — kích thước/bước cửa sổ.
- `FS = 50.0`, `LOWPASS_CUTOFF = 20.0`, `HIGHPASS_GRAVITY = 0.3` — DSP.
- `UNKNOWN_USERS = ["userD", "userE", "userI"]` — tập user dành cho open-set.
- `SEED = 42` — đảm bảo tái lập.

Tham số runtime: `--epochs`, `--folds`, `--no-aug` cho `src.train`.

# CHƯƠNG 7. CẤU TRÚC MÃ NGUỒN

## 7.1. Sơ đồ module

```
src/
├── config.py        Hằng số toàn cục
├── io.py            Đọc CSV + manifest builder
├── preprocess.py    Filter + sliding window
├── features.py      Đặc trưng thủ công (inertial / keystroke / touch)
├── datasets.py      PyTorch Dataset + augmentation
├── models.py        Kiến trúc CNN 1D
├── train.py         3-fold CV trainer
├── openset.py       Softmax + Mahalanobis OOD
└── evaluate.py      Random Forest baseline + figures
```

## 7.2. Vai trò class & method chính

### `src/config.py`
- Khai báo `PROJECT_ROOT`, `RAW_DIR`, `INTERIM_DIR`, `PROCESSED_DIR`, `MODELS_DIR`, `REPORTS_DIR`, `FIGURES_DIR` và auto-tạo thư mục.
- Các hằng số DSP (`FS`, `LOWPASS_CUTOFF`, `HIGHPASS_GRAVITY`), kích thước cửa sổ (`WINDOW_SIZE`, `WINDOW_STRIDE`), danh sách kênh (`INERTIAL_CHANNELS`), `UNKNOWN_USERS`, `SEED`.

### `src/io.py`
- `parse_filename(fname)` — match 1 trong 3 regex (INERTIAL_RE, KEY_RE, TOUCH_RE) để rút `(activity, session, attempt, rep)`.
- `_estimate_fs(df)` — tính `1e9 / median(diff(timestamp_ns))`.
- `load_inertial / load_keystroke / load_touch / load_metadata` — wrapper đọc CSV và chuẩn hoá tên cột.
- `build_manifest(root)` — duyệt cây thư mục, gọi parser, tạo `DataFrame` 325 dòng.
- `save_manifest(df)` — ghi `data/interim/manifest.csv`.

### `src/preprocess.py`
- `_butter_lowpass(data, cutoff, fs, order=4)` — filtfilt zero-phase với cutoff 20 Hz.
- `_butter_highpass(data, cutoff, fs, order=4)` — filtfilt cho `acc_*`, tách trọng lực.
- `preprocess_inertial(df, fs_in)` — pipeline đầy đủ: NaN → resample → lowpass → highpass.
- `sliding_windows(arr, win, stride)` — trả về `(n_win, win, n_ch)`.
- `build_windows(manifest, max_per_file=300, seed=SEED)` — gom cửa sổ, sample đều bằng `np.linspace` để cân bằng class; lưu `windows.npz`.

### `src/features.py`
- `_stats_per_axis(x)` — trả 9 chỉ số (mean, std, mad, min, max, iqr, energy, fft_entropy, fft_dom_freq).
- `window_features(W)` — vector 62 chiều cho 1 cửa sổ.
- `batch_features(X)` — chạy `window_features` cho `N` cửa sổ → `(N, 62)`.
- `keystroke_features(df)`, `touch_tap_features(df)`, `touch_scroll_features(df)` — đặc trưng cho 2 modality phụ.
- `aggregate_user_features()` — tổng hợp ở mức user, lưu CSV.

### `src/datasets.py`
- **Class `InertialDataset(Dataset)`**:
  - `__init__(X, y, mean, std, augment, rng_seed)` — lưu tensor, scaler.
  - `__getitem__(i)` — áp dụng jitter / scaling / rotation 3D nếu `augment=True`; chuyển `(T, C) → (C, T)` cho Conv1D.
  - `__len__` — số mẫu.
- `compute_scaler(X)` — tính `mean, std` shape `(C,)` từ tập train.

### `src/models.py`
- **Class `CNN1D(nn.Module)`**:
  - `__init__(in_channels=6, n_classes=12, emb_dim=128, dropout=0.3)` — định nghĩa 3 tầng Conv1d → BN → ReLU, MaxPool, AdaptiveAvgPool, Dropout, Linear head.
  - `forward(x, return_embedding=False)` — chạy `features → head` hoặc trả embedding 128-d.
  - `embed(x)` — alias `forward(x, return_embedding=True)` cho open-set.

### `src/train.py`
- `load_npz()` — đọc `windows.npz`, trả `X, y, activity, groups`.
- `split_known_unknown(...)` — tách `UNKNOWN_USERS` ra khỏi tập train.
- `train_one_fold(...)` — huấn luyện 1 fold: Adam + class-weighted CrossEntropy + best-checkpoint theo macro-F1; trả `(best_f1, state, history, mean, std)`.
- `run_cv(epochs, n_splits, augment)` — vòng lặp StratifiedGroupKFold, lưu artefact mỗi fold + `cv_summary.json`.
- `main()` — CLI với `argparse`.

### `src/openset.py`
- `_embed_batch(model, X, mean, std, device)` — chạy `model.embed` theo batch, trả `(embeddings, softmax_probs)`.
- `_fit_gaussians(emb_tr, y_tr, n_classes)` — ước lượng `(μ_c, Σ_c^{-1})` mỗi class, regularize `Σ + 1e-3·I`.
- `_mahalanobis_score(emb, mus, inv_covs)` — min Mahalanobis tới các class.
- `evaluate_fold(fold_dir, X_tr, y_tr, X_va, y_va, X_un, device)` — tính AUROC + TPR@FPR=5 % cho softmax và Mahalanobis.
- `main()` — chạy 3 fold, tổng hợp, lưu JSON.

### `src/evaluate.py`
- `cnn_predictions(...)` — gom prediction val của 3 fold thành 1 cặp `(gts, preds)` đầy đủ.
- `rf_baseline(Xk, yk_id, grk, n_splits)` — Random Forest 300 cây với `class_weight=balanced_subsample`, cùng split như CNN.
- `plot_confusion(gts, preds, classes, out_path)` — vẽ heatmap chuẩn hoá theo hàng.
- `per_activity_accuracy(gts, preds, acts)` — break-down theo `sitting / standing / walking`.
- `plot_per_activity(per_act, out_path)` — bar chart kép `accuracy` vs `macroF1`.
- `main()` — chạy CNN aggregate, RF baseline, lưu `evaluate_results.json` + 2 PNG.

## 7.3. Tổng dòng mã

Khoảng ~700 dòng Python, mọi module có hàm `__main__` riêng để chạy độc lập — phục vụ đúng tinh thần "single-responsibility" mà L8 nhấn mạnh trong khi thiết kế data pipeline.

# CHƯƠNG 8. KHÓ KHĂN GẶP PHẢI VÀ CÁCH GIẢI QUYẾT

## 8.1. Lỗi phiên bản app — userA mất kênh

**Triệu chứng**: file inertial của userA có toàn bộ `timestamp_ns = 0`, `mag_x = mag_y = mag_z = 0`.

**Giải pháp**: thay vì sửa từng file, chúng tôi **bỏ kênh magnetometer toàn cục** và chỉ dùng 6 kênh `acc + gyro`. Trade-off: mất 1 modality nhưng cứu được toàn bộ 21 file của userA. Bài học: phải EDA metadata trước khi train.

## 8.2. Schema filename không thống nhất

**Triệu chứng**: cùng modality inertial có tới 4 cách đặt tên (`_s1_att2.csv`, `_s1_r3.csv`, `_s1_att2_r1.csv`, `_r1.csv`).

**Giải pháp**: viết 3 regex riêng cho 3 modality trong `src/io.py`; sau đó validate 0 dòng `UNPARSED` trong manifest. Nếu lười dùng 1 regex chung, sẽ bỏ sót ~40 % file.

## 8.3. Mất cân bằng cửa sổ cực mạnh

**Triệu chứng**: lần build đầu tiên ra **467 k cửa sổ** — riêng 1 file của userQ chiếm ~150 k vì rất dài.

**Giải pháp**: cap **300 cửa sổ/file**, lấy đều bằng `np.linspace(0, n-1, 300, dtype=int)`. Kết quả còn 39 k cửa sổ, phân phối userQ giảm từ 30 % xuống ~2.3 %.

## 8.4. CUDA driver cũ

**Triệu chứng**: PyTorch 2.6 không tương thích NVIDIA driver 12020.

**Giải pháp**: code tự fallback sang CPU bằng `torch.cuda.is_available()`. Batch nhỏ + model gọn (~50 k tham số) nên CPU vẫn chạy tốt trong ~25 phút.

## 8.5. PEP 668 chặn `pip install` toàn cục

**Triệu chứng**: trên Ubuntu 24, pip báo `error: externally-managed-environment`.

**Giải pháp**: bắt buộc dùng `venv`. Ngoài ra mirror PyPI mặc định của một số mạng nội bộ trả về "No matching distribution", phải dùng `--index-url https://pypi.org/simple`.

## 8.6. pandas trả ndarray read-only

**Triệu chứng**: `df.diff().to_numpy()` đôi khi cho mảng `flags.writeable=False`, làm sklearn báo lỗi.

**Giải pháp**: thêm `.copy()` sau mọi lần chuyển từ pandas sang numpy ở `src/features.py`.

## 8.7. userP & userQ trùng metadata

**Triệu chứng**: hai user có cùng device name và metadata timestamp — nghi ngờ trùng phiên hoặc bản sao.

**Giải pháp**: tránh dùng cả P và Q làm "unknown" trong open-set; chọn **D, E, I** thay thế. Quan sát này cũng là một "kết quả EDA" đáng ghi nhận.

## 8.8. StratifiedGroupKFold thiếu class ở val

**Triệu chứng**: với 5-fold, userQ (chỉ 3 file) không xuất hiện trong val của một số fold → skip fold, mất dữ liệu đánh giá.

**Giải pháp**: hạ xuống **3-fold** để mỗi fold val có đủ 12 class. Có thêm logic `if missing: skip` để pipeline không crash khi gặp tình huống tương tự.

## 8.9. CNN không vượt được RF

**Triệu chứng**: sau 40 epoch, CNN macro-F1 ≈ 0.65 trong khi RF ≈ 0.78.

**Giải pháp**: thay vì cố tune để CNN vượt, chúng tôi **báo cáo trung thực** kết quả này — đây là hiện tượng được literature ghi nhận với dataset HAR nhỏ. Đề xuất cải tiến (contrastive learning, thêm phiên ghi/user) đã ghi rõ ở §5.4.

# CHƯƠNG 9. KHÁM PHÁ VÀ KẾT LUẬN

## 9.1. Các khám phá đáng chú ý

1. **Hand-crafted features + Random Forest vẫn vượt CNN khi dữ liệu nhỏ và phiên ghi ít** (RF 0.78 > CNN 0.65 macro-F1). Đây là minh chứng cụ thể cho lời nhắc L7: "không nên mặc định deep learning luôn tốt nhất".
2. **Group-by-file là tiêu chuẩn đánh giá phải có** cho bài toán cá nhân hoá: nếu split random theo cửa sổ, CNN sẽ đạt > 99% accuracy nhưng đó là *leakage* — không phản ánh khả năng tổng quát hoá tới phiên ghi mới.
3. **Walking và standing dễ phân biệt người dùng hơn sitting** (∆macroF1 ≈ +0.05). Lý giải vật lý: chuyển động mạnh hơn → tín hiệu giàu hơn → đặc trưng cá nhân nổi bật hơn.
4. **Softmax max-prob đánh bại Mahalanobis cho open-set với dataset nhỏ** (AUROC 0.66 vs 0.61). Mahalanobis cần covariance ổn định — không đạt được với ~2 k mẫu/class.
5. **Phát hiện userA bị lỗi app và userP/Q trùng metadata** — chỉ bằng EDA metadata, không cần mở từng CSV — đây là ví dụ điển hình cho giá trị của bước manifest mà L3 nhấn mạnh.

## 9.2. Đối sánh với khung lý thuyết môn học

| Module | Bằng chứng trong project |
| --- | --- |
| L1 (DS overview) | Pipeline đúng 4 bước Donoho. |
| L2 (data collection) | App Android tự thu — thay cho web crawling. |
| L3 (cleaning + ETL) | NaN handling, resample, schema unification, manifest. |
| L4 (EDA) | `fs_est`, `mag_zero_ratio`, phân tích outlier user. |
| L5-6 (visualization) | Confusion matrix, per-activity bar chart. |
| L7 (ML) | RF + CNN, class weighting, regularization. |
| L8 (big data design) | Cấu trúc `data/{raw,interim,processed}` mô phỏng data lake. |
| L10-11 (CV) | Kiến trúc Conv 1D mượn ý tưởng từ LeNet/TextCNN. |
| L12 (evaluation) | StratifiedGroupKFold, macro-F1, AUROC, TPR@FPR=5%. |

## 9.3. Kết luận

Nhóm đã hoàn tất toàn bộ pipeline từ thu thập đến đánh giá: manifest chuẩn hoá, tiền xử lý (lowpass + tách trọng lực + trượt cửa sổ 2.56 s @ 50 Hz), trích 62 đặc trưng thủ công cho RF, huấn luyện CNN 1D 6-kênh với augmentation acc+gyro, đánh giá 3-fold group-by-file, và open-set bằng softmax/Mahalanobis. Kết quả thực nghiệm cho thấy RF baseline đạt **macro-F1 ≈ 0.78** ở closed-set và open-set softmax đạt **AUROC ≈ 0.66**, là điểm khởi đầu hợp lý cho các bước cải tiến tiếp theo nêu trong §5.4. Toàn bộ mã nguồn nằm dưới `src/`, kết quả số lưu ở `models/cv_summary.json`, `reports/openset_results.json`, `reports/evaluate_results.json`, hình vẽ tại `reports/figures/`.

Tài liệu liên quan: [README.md](README.md) hướng dẫn cài/chạy, [PRESENTATION.md](PRESENTATION.md) bản thuyết trình chi tiết, [STUDY_PLAN.md](STUDY_PLAN.md) ánh xạ kiến thức từng slide IT4142 vào project.
