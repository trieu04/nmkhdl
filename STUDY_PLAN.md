# Kế hoạch nghiên cứu & Giải thích chi tiết các slide khoá IT4142

Tài liệu này tập hợp **toàn bộ nội dung 14 slide** của môn học, giải thích lý thuyết và **ánh xạ trực tiếp vào đồ án định danh người dùng** mà nhóm đang triển khai. Đọc xong, các thành viên sẽ biết: trong báo cáo / bài thuyết trình, từng phần đang dùng kiến thức của slide nào, và cần nói rõ điều gì.

---

## 0. Yêu cầu đồ án rút từ L0 (course information)

L0 quy định chính xác barème và sản phẩm phải nộp. Tóm tắt:

### 0.1 Cách tính điểm

- **Đồ án (P)**: tối đa 10 điểm.
- **Thi trắc nghiệm (E)**: tối đa 10 điểm.
- **Điểm học phần G = 0.4 × P + 0.6 × E.**

### 0.2 Sản phẩm phải nộp (3 phần)

1. **Mã nguồn** đóng trong file nén.
2. **`readme.txt` / `README.md`** mô tả: cài đặt, biên dịch, chạy, kèm danh sách gói phần mềm.
3. **Báo cáo PDF** với 7 mục bắt buộc:
   - Mô tả bài toán thực tế.
   - Chi tiết (các) phương pháp học máy và (các) dataset sử dụng.
   - Kết quả thí nghiệm đánh giá hiệu năng.
   - Các chức năng chính của hệ thống và cách sử dụng.
   - Cấu trúc mã nguồn — vai trò các **class** và **method** chính.
   - Khó khăn gặp phải & cách giải quyết.
   - Khám phá mới hoặc kết luận.

### 0.3 Tiêu chí chấm

| Tiêu chí | Cách "ghi điểm" trong project này |
| --- | --- |
| Mức độ phức tạp bài toán | Định danh 12 người **kèm open-set** trên 3 hoạt động + 3 modality. |
| Tính đúng đắn / phù hợp của phương pháp | Pipeline DSP → CNN/RF + chia tập **group-by-file** (nghiêm hơn random). |
| Đánh giá / lựa chọn mô hình kỹ lưỡng | 2 mô hình (CNN, RF) × 3-fold CV × 2 chiến lược open-set, có macroF1/AUROC. |
| Chất lượng presentation | Đã có [PRESENTATION.md](PRESENTATION.md) và tài liệu này. |
| Chất lượng báo cáo | [report.md](report.md) bổ sung đủ 7 mục L0 yêu cầu. |
| Cài đặt hệ thống dễ dùng | CLI `python -m src.<module>`, README có ví dụ. |
| Thuyết trình 15 phút, mọi thành viên trình bày | Chia mục theo từng thành viên (xem 8.2 cuối tài liệu). |
| Trích dẫn thư viện sử dụng | Có ở README và §1.4. |

> **Kết luận**: project hiện đã đáp ứng tất cả ô trên — phần còn lại là *kể câu chuyện* tốt trong báo cáo và slide thuyết trình.

---

## 1. L1 — Tổng quan Khoa học dữ liệu

### 1.1 Khái niệm cốt lõi

- **Khoa học dữ liệu (Donoho)**: "the science of learning from data".
- 2 mục tiêu chính: **Descriptive** (mô tả) và **Predictive** (dự đoán).
- Quy trình chuẩn: **Thu thập → Tiền xử lý → Học máy → Trực quan hoá**.
- 10 Vs của Big Data (Volume, Velocity, Variety, Veracity, Value, Variability, Visualization, Validity, Vulnerability, Volatility).

### 1.2 Ánh xạ vào project

| L1 nói | Project làm |
| --- | --- |
| Có "câu hỏi cụ thể không biết trước" | "Người ngồi trước máy *là ai*?" — open-set classification. |
| Predictive task | Dự đoán nhãn user từ vector cảm biến. |
| Quy trình 4 bước | App Android thu CSV → `src/preprocess.py` → `src/train.py` → `reports/figures/*.png`. |
| Dữ liệu giàu V | Volume (39k cửa sổ), Variety (3 modality), Veracity (xử lý userA lỗi). |

### 1.3 Câu để nói trong slide

> "Đề tài chúng tôi nằm trong nhóm Predictive Task, kết hợp Data Description (EDA và confusion matrix) với Supervised Learning (CNN 1D + Random Forest), đi đúng quy trình 4 bước Donoho/Tukey đã chỉ ra."

### 1.4 Trích dẫn thư viện (yêu cầu L0)

- pandas, numpy, scipy, scikit-learn (BSD/MIT).
- PyTorch (BSD).
- matplotlib, seaborn (PSF/BSD).
- python-pptx (MIT) — chỉ dùng cho tài liệu nội bộ.

---

## 2. L2 — Thu thập & tiền xử lý dữ liệu (web crawling)

### 2.1 Slide nói

- Các nguồn dữ liệu (web, log, sensor, social).
- Crawler: Scrapy, BeautifulSoup, request, robots.txt, rate-limit.
- Storage: file system, NoSQL.

### 2.2 Ánh xạ project

- Chúng tôi **không crawl web**, mà **tự thu** bằng app Android — đây vẫn là một "data acquisition pipeline" hợp lệ. Tương đương với "sensor data" được đề cập ở L2.
- App đẩy CSV ra storage cục bộ; manifest builder ([src/io.py](src/io.py)) đóng vai như "data ingestion layer".
- 3 regex phân tích filename = phiên bản đơn giản của "URL pattern extraction" mà crawler hay làm.

### 2.3 Câu nói

> "Slide L2 trình bày các phương pháp thu thập từ web; ở chỗ chúng tôi nguồn dữ liệu chính là cảm biến điện thoại, nhưng vai trò *manifest + ingestion* vẫn tương đương: phải có một bộ phân tích filename + đọc CSV ổn định, tương tự cách crawler chuẩn hoá URL."

---

## 3. L3 — Làm sạch & tích hợp dữ liệu

### 3.1 Slide nói

- **Data integration**: 3 hướng (Ad-hoc programming, Data Warehouse, Virtual integration).
- **ETL**: Extract → Transform → Load, chiếm 70–80% công sức dự án BI.
- **Chất lượng dữ liệu**: chính xác, đầy đủ, nhất quán, kịp thời, hợp lệ.
- **Các bước tiền xử lý**: phát hiện thiếu/trùng/nhiễu, chuẩn hoá, mã hoá categorical.
- Công cụ: OpenRefine, pandas.

### 3.2 Ánh xạ project (rất sát)

| Khái niệm L3 | Bước tương ứng trong project |
| --- | --- |
| **Extract** | `pd.read_csv` 325 file × 3 modality. |
| **Transform** | NaN → ffill/bfill; `resample_poly` 50 Hz; lọc Butterworth; sliding window. |
| **Load** | `windows.npz` (NPZ binary) + `feat_*.csv`. |
| **Schema integration** | 3 regex thống nhất filename schema khác nhau (`_s{S}_att{n}`, `_s{S}_r{m}`, `_r{m}`). |
| **Data quality** | Phát hiện userA `timestamp_ns = 0`, `mag = 0`; phát hiện userP/Q trùng metadata. |
| **Outlier handling** | Cap 300 cửa sổ/file để tránh 1 file 150k cửa sổ phá phân phối. |

### 3.3 Câu nói

> "Pipeline của chúng tôi là một quy trình ETL hoàn chỉnh. Phần *Transform* là phần mang giá trị lớn nhất: lọc Butterworth tách trọng lực, sliding window, và caps 300 cửa sổ/file để đảm bảo cân bằng lớp."

---

## 4. L4 — Exploratory Data Analysis (EDA)

### 4.1 Slide nói

- EDA là *triết lý*, không phải kỹ thuật: hiểu cấu trúc, ngoại lệ, pattern.
- 4 nhóm câu hỏi: phân bố, nhiễu, tương quan, outlier.
- Univariate: mean, median, mode, std, var, skew, kurtosis, histogram, box plot.
- Bivariate / multivariate: scatter, correlation, PCA.

### 4.2 Ánh xạ project

- **Univariate**: tính `fs_est` mỗi file, `mag_zero_ratio`, `n_rows` → đã ghi sẵn trong `data/interim/manifest.csv`.
- **Bivariate**: ma trận tương quan giữa 6 trục là 9 trong 62 đặc trưng thủ công ([src/features.py](src/features.py)).
- **Outlier detection**: chính việc phát hiện userA và userP/Q là EDA trên metadata.
- **Visualization** (đã có): confusion matrix `reports/figures/cnn_confusion.png`, per-activity bar chart.

### 4.3 Mở rộng đề xuất cho EDA chuyên sâu hơn

> Có thể bổ sung notebook `notebooks/eda.ipynb` để vẽ:
> - Histogram số cửa sổ / user / activity.
> - Box plot biên độ `acc_*` theo activity.
> - Scatter PCA 2D của embedding 128-d, tô màu theo user.

### 4.4 Câu nói

> "EDA của chúng tôi không chỉ là vẽ chart đẹp; nó dẫn trực tiếp đến 3 quyết định kỹ thuật: (1) bỏ kênh magnetometer, (2) loại userP/Q khỏi tập unknown, (3) cap 300 cửa sổ/file."

---

## 5. L5–L6 — Trực quan hoá dữ liệu (univariate + multivariate)

### 5.1 Slide nói

- Mã hoá trực quan: position, length, area, color, texture.
- Univariate: histogram, density, box, violin.
- Multivariate: scatter matrix, parallel coordinates, heatmap, PCA/t-SNE.
- "Visualization-first" rồi mới thống kê.

### 5.2 Ánh xạ project

- **Heatmap** = confusion matrix `cnn_confusion.png` (đã có).
- **Bar group** = per-activity accuracy `cnn_per_activity.png` (đã có).
- **Đề xuất bổ sung** cho slide thuyết trình:
  - **PCA / t-SNE** trên embedding 128-d → trực quan hoá xem 12 user có tách thành 12 cụm không.
  - **Spectrogram** của 1 user lúc walking — so với sitting (chứng minh "tín hiệu giàu" hơn).
  - **Line plot** mất mát theo epoch (đã có sẵn `models/foldK/history.json`).

### 5.3 Câu nói

> "Slide L5-L6 cho 1 nguyên tắc: encoding position (toạ độ) mạnh hơn color. Confusion matrix tận dụng color vì chiều dữ liệu là 12 × 12 — bắt buộc; còn per-activity bar chart dùng position để so sánh accuracy/F1 chính xác hơn."

---

## 6. L7 — Học máy (ML basics + mô hình)

### 6.1 Slide nói

- **Supervised**: classification (rời rạc) vs regression (liên tục).
- Linear/Ridge/LASSO regression: $w^* = (A^T A + \lambda I)^{-1} A^T y$ (Ridge).
- Logistic regression, k-NN, Decision Tree, **Random Forest**, SVM.
- Loss function, overfitting, regularization, cross-validation.

### 6.2 Ánh xạ project (rất sát)

| Khái niệm L7 | Project |
| --- | --- |
| Classification 12-class | CNN 1D + Random Forest. |
| Cross-entropy loss có trọng số | `nn.CrossEntropyLoss(weight=w)` trong [src/train.py](src/train.py). |
| Regularization | Weight decay 1e-4 + Dropout 0.3 (≈ L2 regularization của Ridge). |
| Bagging / Random Forest | `RandomForestClassifier(n_estimators=300, class_weight=balanced_subsample)`. |
| Train/Val split | StratifiedGroupKFold 3-fold. |
| Overfitting | Theo dõi train_loss giảm vs val_macroF1 plateau → chọn checkpoint best. |

### 6.3 Tại sao CNN thay vì Linear/Logistic?

- Tín hiệu cảm biến **phi tuyến** theo thời gian; linear model không bắt được pattern dài 2.56 s.
- CNN 1D = chuỗi *learnable filter* — tổng quát hoá của bộ lọc thủ công ở L7 (Sobel, Gabor).

### 6.4 Câu nói

> "L7 dạy đầy đủ 5 họ mô hình; chúng tôi chọn 2 đại diện: Random Forest (ensemble + tree-based) cho baseline thủ công và CNN 1D (deep learning) cho representation learning. Cả hai đều dùng cross-entropy hoặc Gini, đều áp dụng regularization, đều validate bằng cross-validation — đúng pipeline L7."

---

## 7. L8 — Big data management

### 7.1 Slide nói

- Hadoop, HDFS, MapReduce, Spark.
- Khi nào cần big data tooling? Khi single-machine không xử lý nổi.

### 7.2 Ánh xạ project

- 325 CSV, 39 k cửa sổ × 128 × 6 × float32 = **~120 MB** RAM → **single-machine đủ**.
- Tuy nhiên cách *thiết kế pipeline* (manifest CSV nhỏ, tách raw → interim → processed) **mượn ý tưởng từ HDFS data lake**: dữ liệu thô bất biến, transform chỉ thêm tầng mới.

### 7.3 Câu nói

> "Project hiện ở quy mô vài trăm MB nên chưa cần Spark; nhưng cấu trúc thư mục `data/{raw,interim,processed}` mô phỏng đúng pattern data lake mà L8 đề cập — dễ scale ngang khi user tăng từ 15 lên hàng nghìn."

---

## 8. L10–L11 — Phân tích các kiểu dữ liệu chuyên biệt

Có 4 sub-slide. Project chúng tôi liên quan trực tiếp với **time-series** (qua kiểu xử lý CNN1D) và gián tiếp với CV/NLP qua kiến trúc CNN.

### 8.1 L10-11-CV (Computer Vision)

- Slide nói: Conv 2D, pooling, kiến trúc LeNet/AlexNet/ResNet.
- Project mượn: kiến trúc 3 tầng Conv + Pool **trực tiếp lấy ý tưởng từ LeNet** nhưng đổi sang **Conv 1D** cho chuỗi thời gian.
- "Receptive field" của tầng Conv 7 đầu tiên = 140 ms — đây là khái niệm CV chuẩn.

### 8.2 L10-11-NLP / POS-tagging

- Liên quan đến project chủ yếu ở chỗ: cả CNN 1D cho NLP và cho cảm biến đều xử lý chuỗi 1D đa kênh (NLP: chiều embedding word; cảm biến: 6 trục). Có thể nói: "kiến trúc của chúng tôi *tương đương* TextCNN với độ dài cố định".

### 8.3 L10-11-LinkAnalysis

- Slide nói: PageRank, HITS, community detection.
- Project: **không** trực tiếp; nhưng nếu sau này muốn xây dựng **social biometric** (định danh user dựa trên đồ thị tương tác với bạn bè), thì LinkAnalysis sẽ vào cuộc.

---

## 9. L12 — Đánh giá kết quả phân tích (rất quan trọng)

### 9.1 Slide nói

- **Đánh giá thực nghiệm** (chứ không lý thuyết).
- Các chiến lược: **Hold-out**, **Stratified sampling**, **Repeated hold-out**, **k-fold cross-validation**, **Leave-one-out**, **Bootstrap**.
- Metrics: accuracy, precision, recall, F1, ROC, AUC.

### 9.2 Ánh xạ project (cực sát)

| L12 đề cập | Project |
| --- | --- |
| **Hold-out** | Chia known/unknown ban đầu (D/E/I tách hẳn). |
| **Stratified sampling** | `StratifiedGroupKFold` giữ tỉ lệ class mỗi fold. |
| **k-fold CV** | k = 3 (vì userQ chỉ 3 phiên ghi). |
| **Group-aware** | Mở rộng L12: thêm ràng buộc "cùng group không chia 2 phía" — chống leakage. |
| **macro-F1** | Bắt buộc khi class mất cân bằng (userQ 900 vs userD 5993 cửa sổ). |
| **AUROC** | Đường ROC + AUC cho open-set known-vs-unknown. |
| **Confusion matrix** | Trực quan hoá lỗi 12 × 12. |

### 9.3 Câu nói

> "Chương đánh giá là chương chúng tôi đi xa hơn L12: ngoài k-fold stratified, chúng tôi **bắt buộc thêm ràng buộc group-by-file** để mô phỏng đúng deployment scenario — một mức nghiêm khắc hơn standard k-fold."

---

## 10. Lộ trình thuyết trình 15 phút (theo yêu cầu L0)

Mỗi thành viên ~1.5 phút, đảm bảo cả 9 thành viên đều có phần. Gợi ý phân chia:

| Người | Phần | Slide trong PRESENTATION.md |
| --- | --- | --- |
| 1 — Lương Mạnh Tường | Giới thiệu bài toán + tổng quan pipeline | §0, §1 |
| 2 — Bùi Minh Tuấn | Dữ liệu thực tế + manifest | §1, §2 |
| 3 — Trương Quốc Triệu | Tiền xử lý DSP (Butterworth + window) | §3 |
| 4 — Nguyễn Đức Thành | 62 đặc trưng thủ công | §4 |
| 5 — Nguyễn Anh Tuấn | Kiến trúc CNN 1D + augmentation | §5 |
| 6 — Vũ Ngọc Lâm | Chia tập group-by-file + cross-validation | §6 |
| 7 — Vũ Nhật Quang | Open-set (softmax + Mahalanobis) | §7 |
| 8 — Mai Văn Đăng | Kết quả thực nghiệm + biểu đồ | §8, §9 |
| 9 — Nguyễn Đình Thành | Khó khăn & kết luận + Q&A | §11, §12 |

> 1 thành viên đứng đầu coi sóc Q&A; nên chuẩn bị trước 8 câu trong [PRESENTATION.md §11](PRESENTATION.md).

---

## 11. Plan nghiên cứu thêm (nếu có thời gian trước hôm bảo vệ)

| Việc | Cải thiện kỳ vọng | Tham chiếu slide |
| --- | --- | --- |
| Vẽ PCA / t-SNE trên embedding 128-d | Hình đẹp cho slide; chứng minh CNN học được cấu trúc user | L5-6 |
| Notebook EDA: phân bố biên độ theo activity | Trả lời "tại sao walking dễ phân biệt hơn sitting" | L4 |
| Late fusion CNN + RF (vote bằng softmax average) | macroF1 có thể tăng 0.02-0.05 | L7 |
| OpenMax thay Mahalanobis | AUROC open-set có thể tăng 0.02-0.04 | L12 |
| Báo cáo significance test (paired t-test) giữa RF và CNN | Tăng độ chặt chẽ thống kê | L12 |
| Slide diagram pipeline render bằng mermaid → PNG | Đẹp hơn ASCII | L5-6 |

> Ưu tiên: **PCA t-SNE + late fusion** — đây là 2 việc tăng cả số và hình ảnh nhiều nhất với ~2 giờ công.

---

## 12. Checklist nộp bài (so với L0)

- [x] Mã nguồn: `src/` (8 module Python).
- [x] Pipeline chạy end-to-end: `python -m src.io && ... && python -m src.evaluate`.
- [ ] **`README.md`** mô tả setup → đã được tạo cùng tài liệu này.
- [ ] **Báo cáo PDF**: xuất từ [report.md](report.md) (đã bổ sung 7 mục L0). Khi nộp dùng `pandoc report.md -o report.pdf` hoặc Word export.
- [x] Kết quả thí nghiệm: `models/cv_summary.json`, `reports/*.json`, `reports/figures/*.png`.
- [x] Khó khăn & giải pháp: §11 trong report.md.
- [x] Khám phá: "RF beats CNN ở giao thức group-by-file"; "softmax > Mahalanobis open-set với embedding nhỏ".

---

## 13. Một dòng tóm tắt cho mọi câu hỏi "đề tài liên quan môn học thế nào?"

> "Đồ án đi đầy đủ qua **6 module của chương trình** (L1 tổng quan → L2 thu thập → L3 ETL → L4 EDA → L7 ML → L12 đánh giá) trên một bài toán supervised classification + open-set detection, với cấu trúc thư mục mô phỏng data lake (L8) và chọn lọc kỹ thuật trực quan hoá theo L5-L6."
