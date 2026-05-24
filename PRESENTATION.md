# Tài liệu thuyết trình — Định danh người dùng qua hành vi cảm biến
> **Bản 2026-05-18 — chi tiết theo code.**
> Mỗi run được giải thích **bản chất toán học + đoạn code thực thi + tại sao thắng hoặc thua**.
> Kết quả tốt nhất: **E03_rotation_only = macro-F1 0.8266 ± 0.0354** (3-fold StratifiedGroupKFold).

---

## Mục lục

| Phần | Nội dung | Slide |
|---|---|---|
| A | Bài toán + dữ liệu + DSP + giao thức CV | 1–6 |
| B | Phase B (B01–B06) — Optimizer & Scheduler | 7–13 |
| C | Phase C (C01–C07) — Architecture | 14–21 |
| D | Phase D (D01–D07) — Loss & class-weight | 22–29 |
| E | Phase E (E01–E08) — **Augmentation (winner)** | 30–38 |
| G | Phase G (G01–G05) — Scale-up | 39–44 |
| H/J | RF baseline + Open-set | 45–46 |
| Z | Tổng kết + bài học + Q&A | 47–50 |

---

# PHẦN A — Nền tảng chung

## Slide 1 — Tiêu đề

**Định danh người dùng qua hành vi cảm biến điện thoại**
*Behavioral biometrics with inertial signals — Closed-set & Open-set*

- 12 user known · 3 user unknown (D, E, I) · 6 kênh acc + gyro · 50 Hz
- Pipeline 36 runs / 7 phases / ~5.2 giờ compute
- Best macro-F1: **0.8266** (E03)

---

## Slide 2 — Bài toán

| Mục | Closed-set | Open-set |
|---|---|---|
| Input | 1 cửa sổ 2.56 s, 6 kênh inertial | Cùng đầu vào |
| Output | 1 trong 12 user đã đăng ký | "known" hoặc "unknown" |
| Metric | macro-F1 (3-fold) | AUROC + TPR @ FPR=5% |
| Khó vì | mất cân bằng class (~1:7) | mạng overconfident với OOD |

---

## Slide 3 — Pipeline tổng quan (theo `src/`)

```
rootdata/CSV  →  io.py (manifest)  →  preprocess.py (Butterworth + window)  →  windows.npz
                                                                                    │
                                                ┌───────────────────────────────────┤
                                                ▼                                   ▼
                                   models.py (CNN/ResNet/TCN/BiLSTM)        features.py + RF
                                                │
                                                ▼
                                    train.py (3-fold CV)  ──→  experiment.py (log.csv)
                                                │
                                                ▼
                                      openset.py (softmax / Mahalanobis)
```

Mỗi phase chạy lệnh duy nhất:
```bash
python -m scripts.run_experiment --config experiments/configs/<name>.yaml
```

---

## Slide 4 — Tiền xử lý DSP (cố định, file `src/preprocess.py`)

| Bước | Cấu hình | Lý do |
|---|---|---|
| Butterworth lowpass bậc 4 | cutoff **20 Hz** | Cắt nhiễu cao tần, giữ băng chuyển động 0–10 Hz |
| Butterworth highpass bậc 4 (chỉ acc) | cutoff **0.3 Hz** | Tách trọng lực 9.81 m/s² (DC) khỏi gia tốc tuyến tính |
| `scipy.signal.filtfilt` zero-phase | – | Triệt tiêu trễ pha — quan trọng cho mạng nhạy thời gian |
| Resample về 50 Hz | `resample_poly` | Đồng nhất fs giữa các phiên |
| Window | **W=128 (2.56 s), stride 64 (overlap 50%)** | Chuẩn HAR; chứa 2–3 chu kỳ gait |
| Cap | **300 cửa sổ/file** (lấy đều `np.linspace`) | Chống userQ/file dài chiếm phân phối |
| Tổng | **N ≈ 39 018 cửa sổ** (12 user known) | – |

> Khối DSP này **giữ nguyên cho toàn bộ 36 runs**. Nhờ vậy chênh lệch F1 giữa các run **chỉ đến từ thay đổi mô hình/loss/aug**.

---

## Slide 5 — Giao thức đánh giá (file `src/train.py:run_cv`)

```python
skf = StratifiedGroupKFold(n_splits=3, shuffle=True, random_state=seed)
for tr_idx, va_idx in skf.split(X, y_idx, groups=groups):
    ...   # groups = "userX__filename.csv"
```

- **Stratified**: mỗi fold đều có đủ 12 user.
- **Group**: cùng 1 file → không bao giờ ở cả train + val (chống leakage qua cửa sổ liền kề overlap 50%).
- **3 fold (không 5)**: vì userQ chỉ có 3 file ⇒ k=5 sẽ có fold thiếu userQ trong val.
- **Metric báo cáo**: `mean_macroF1 ± std` qua 3 fold.

> Đây là điểm khác biệt quyết định so với "tutorial-grade HAR" (random-split nội cửa sổ → F1 ảo > 99%, vô dụng khi deploy).

---

## Slide 6 — Cách đọc bảng số

Mỗi run lưu vào `experiments/log.csv` qua `ExperimentLogger`:
```
run_id, phase, name, mean_macroF1, std_macroF1, fold0_f1, fold1_f1, fold2_f1, config_json
```

**Đường tiến hoá tổng**: 0.6451 (baseline gốc) → 0.6453 (B01 tái hiện) → 0.6906 (B04) → 0.7822 (C07) → **0.8266 (E03)**.

---

# PHẦN B — Phase B: Optimizer & Scheduler

> **Câu hỏi phase B**: Trước khi đụng kiến trúc, vắt thêm bao nhiêu F1 chỉ bằng cách *dạy cùng một CNN baseline* tốt hơn?
> **Mô hình cố định**: CNN1D 3-tầng filters=[32,64,128], kernels=[7,5,3], dropout=0.3.
> **Dữ liệu cố định**: aug đầy đủ (jitter+scale+rotation), CE + invfreq.

## Slide 7 — Phase B tổng quan

| Run | Optimizer | Scheduler | Epochs | macro-F1 | std |
|---|---|---|---|---|---|
| B01 (baseline) | Adam 1e-3 | none | 40 | 0.6453 | 0.010 |
| B02 | Adam 1e-3 | none | 80 | 0.6721 | 0.012 |
| B03 | Adam 1e-3 | Cosine T_max=80 | 80 | 0.6755 | 0.014 |
| **B04 ★** | **Adam 1e-4** | **OneCycle max_lr=3e-3** | 80 | **0.6906** | **0.006** |
| B05 | AdamW wd=5e-4 | Cosine T_max=80 | 80 | 0.6747 | 0.011 |
| B06 | AdamW wd=5e-4 | Cosine 120ep + ES p=20 | 120 | 0.6835 | 0.020 |

---

## Slide 8 — B01 (baseline tái hiện): bản chất phương pháp

**Cấu hình**: Adam lr=1e-3, weight_decay=1e-4, không scheduler, 40 epochs.

**Bản chất Adam** (Kingma 2014):
- Lưu **moving average bậc 1** $m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t$ (xu hướng gradient).
- Lưu **moving average bậc 2** $v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t^2$ (độ lớn gradient).
- Cập nhật: $\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{\hat v_t}+\epsilon}\hat m_t$.
- ⇒ **per-parameter adaptive learning rate**, ít cần tune `lr` thủ công.

**Code thực thi** (`src/train.py:_build_optimizer`):
```python
return torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)
```

**Vì sao đạt 0.6453**: Adam tự thích nghi đủ tốt để chạy mà không cần scheduler, nhưng 40 epoch không đủ — loss train còn giảm khi dừng (xem `history.json` của fold0). Đây là **chưa hội tụ**.

---

## Slide 9 — B02: tăng epoch 40 → 80

**Thay đổi**: chỉ tăng `epochs: 80`, mọi thứ khác giữ nguyên.

**Kết quả**: 0.6453 → **0.6721** (+0.027).

**Diễn giải**:
- Loss train tiếp tục giảm, loss val ổn định → mô hình **vẫn còn dư đường học** ở epoch 40.
- Nhưng từ epoch ~60 trở đi, val_F1 dao động → bắt đầu có dấu hiệu overfit nhẹ.

⇒ Cần **scheduler** để giảm `lr` về cuối training.

---

## Slide 10 — B03: thêm Cosine annealing

**Cấu hình**: Adam 1e-3 + `CosineAnnealingLR(T_max=80)`.

**Bản chất Cosine annealing**:
$$\eta_t = \eta_{\min} + \frac{1}{2}(\eta_{\max}-\eta_{\min})\left(1 + \cos\frac{\pi t}{T}\right)$$
- Bắt đầu ở 1e-3, giảm mượt theo cosine xuống ~0 sau 80 epoch.
- Pha cuối **lr nhỏ** ⇒ mô hình **fine-tune** quanh điểm tối ưu.

**Code** (`src/train.py:_build_scheduler`):
```python
return torch.optim.lr_scheduler.CosineAnnealingLR(optim, T_max=80)
```

**Kết quả**: 0.6721 → **0.6755** (+0.003). Cải thiện khiêm tốn — vì khởi đầu 1e-3 vẫn khá lớn cho dataset nhỏ này.

---

## Slide 11 — 🏆 B04: OneCycleLR max_lr=3e-3

**Cấu hình**: `lr_init=1e-4`, `OneCycleLR(max_lr=3e-3)`, 80 epoch.

**Bản chất OneCycle** (Smith 2018, "super-convergence"):
- Pha 1 (warm-up, 30% epochs): `lr` tăng tuyến tính từ `max_lr/25` → `max_lr` (1e-4 → 3e-3).
- Pha 2 (anneal, 70% epochs): `lr` giảm cosine từ `max_lr` → `max_lr/10000`.
- Đồng thời momentum đi ngược chiều.

**Lý thuyết**: lr cao ở giữa training **đẩy mô hình ra khỏi vùng minimum hẹp** (sharp), buộc nó tìm minimum rộng (flat) ⇒ tổng quát hoá tốt hơn.

**Code**:
```python
return torch.optim.lr_scheduler.OneCycleLR(
    optim, max_lr=3e-3, steps_per_epoch=len(dl_tr), epochs=80)
# Quan trọng: gọi sched.step() SAU MỖI BATCH (xem train.py:200)
```

**Kết quả**: 0.6755 → **0.6906** (+0.015) **và std giảm còn 0.006** (ổn định nhất phase B).

⇒ **B04 trở thành xương sống cho mọi phase sau** (epochs=80, OneCycleLR max_lr=3e-3, lr_init=1e-4).

---

## Slide 12 — B05: AdamW không hơn Adam

**Cấu hình**: AdamW `lr=1e-3, wd=5e-4`, Cosine 80ep.

**Khác biệt AdamW vs Adam**: AdamW (Loshchilov 2019) **tách weight decay khỏi gradient** — `θ ← θ − η·∇L − η·λ·θ` thay vì cộng λθ vào gradient rồi mới qua Adam. Lý thuyết: tốt hơn cho mô hình lớn vì decay không bị "scale" bởi adaptive `v_t`.

**Kết quả**: 0.6755 → **0.6747** (gần như bằng B03).

**Vì sao không thắng?**: Mô hình baseline chỉ ~50k params, weight decay 1e-4 (Adam) đã đủ. AdamW chỉ phát huy khi mô hình lớn hơn nhiều (ResNet50+).

---

## Slide 13 — B06: thử thêm 120 epoch + early stopping

**Cấu hình**: AdamW + Cosine 120ep + `early_stopping_patience=20`.

**Cơ chế early stopping** (`train.py:241–246`):
```python
if f1 > best_f1:
    best_f1 = f1; bad_epochs = 0; best_state = ...
else:
    bad_epochs += 1
    if bad_epochs >= patience: break
```

**Kết quả**: 0.6835 — tốt hơn B05 nhưng vẫn dưới B04 (0.6906). Std cao (0.020) ⇒ **early stop ở fold khác nhau** ⇒ kém ổn định.

⇒ **OneCycleLR + 80ep cố định thắng cosine + 120ep + ES** trong setup này.

---

# PHẦN C — Phase C: Architecture

> **Câu hỏi phase C**: Giữ nguyên B04 setup, đổi kiến trúc → kiến trúc nào hợp với tín hiệu cảm biến đa kênh?
> **Tham khảo**: lr_init=1e-4 + OneCycleLR + 80ep, CE + invfreq, aug đầy đủ.

## Slide 14 — Phase C tổng quan

| Run | Kiến trúc | Tham số chính | macro-F1 | std |
|---|---|---|---|---|
| C01 | CNN dropout=0.2 | filters [32,64,128] | 0.6973 | 0.008 |
| C02 | CNN dropout=0.5 | filters [32,64,128] | 0.6832 | 0.008 |
| C03 | CNN big | **filters [64,128,256]** | 0.7254 | 0.013 |
| C04 | CNN deep 4-tầng | [32,64,128,256], [7,5,5,3] | 0.7421 | 0.016 |
| **C05** | **ResNet1D** | filters [64,128,256] | 0.7677 | 0.021 |
| C06 | TCN | channels [64,64,128,128], k=5 | 0.7600 | 0.031 |
| **C07 ★** | **BiLSTM-Attn** | hidden=128, layers=2 | **0.7822** | 0.019 |

---

## Slide 15 — C01/C02: Dropout sweep (regularization)

**Bản chất Dropout** (Srivastava 2014):
- Mỗi forward training, mỗi neuron bị "tắt" với xác suất `p`.
- Inference: dùng toàn bộ neuron, scale activation × (1−p).
- Tương đương **ensemble ngầm** của 2^N mạng con.

**Code** (`src/models.py:CNN1D`):
```python
self.dropout = nn.Dropout(dropout)
self.head = nn.Linear(self.emb_dim, n_classes)
# forward: self.head(self.dropout(z))   # chỉ dropout TRƯỚC head, không trong conv
```

**Kết quả**:
- C01 dropout=0.2: 0.6973 (tốt nhất trong CNN nhỏ).
- C02 dropout=0.5: 0.6832 (sụt — quá nhiều regularization khiến mô hình underfit).

⇒ Bài học: **với dataset 30k mẫu + mô hình nhỏ, dropout 0.2–0.3 là sweet spot**.

---

## Slide 16 — C03: CNN big — wider channels

**Cấu hình**: filters `[32,64,128]` → **`[64,128,256]`** (gấp đôi).

**Vì sao wider có ích**:
- Tầng cuối có **256 filter** thay vì 128 ⇒ embedding 256-d giàu thông tin hơn.
- Mỗi filter học **một loại pattern** (gait phase, bàn tay vung, v.v.) ⇒ nhiều filter ⇒ phủ nhiều pattern hơn.

**Tham số tăng**: ~50k → ~200k params. Vẫn nhỏ so với 30k mẫu (tỉ lệ 1:150).

**Kết quả**: 0.6973 → **0.7254** (+0.028). Capacity là vấn đề thực sự.

---

## Slide 17 — C04: CNN deep 4-tầng

**Cấu hình**: `filters [32,64,128,256], kernels [7,5,5,3]`.

**Receptive field** (cộng dồn qua các tầng pool):
- Tầng 1: k=7, RF=7 mẫu
- Tầng 2 (sau MaxPool 2): RF tương đương 7+5×2 = 17 mẫu
- Tầng 3 (sau MaxPool 4): RF ~ 17+5×4 = 37 mẫu
- Tầng 4 (sau MaxPool 8): RF ~ 37+3×8 = 61 mẫu ≈ **1.2 giây**

⇒ Tầng cuối "nhìn" gần một chu kỳ gait đầy đủ.

**Code** (`src/models.py:CNN1D` block loop):
```python
for i, (c_out, k) in enumerate(zip(filters, kernels)):
    layers += [nn.Conv1d(c_in, c_out, k, padding=k//2),
               nn.BatchNorm1d(c_out), nn.ReLU()]
    if i < len(filters) - 1:
        layers.append(nn.MaxPool1d(2))    # halve length
```

**Kết quả**: 0.7254 → **0.7421** (+0.017).

---

## Slide 18 — C05: ResNet1D — skip connection

**Bản chất ResNet** (He 2016):
- Mỗi block học **residual** $F(x)$, output = $F(x) + x$.
- Khi $F$ khó học, mạng có thể "rút gọn" về identity → **không bao giờ tệ hơn baseline nông hơn**.
- Skip làm gradient chảy thẳng về tầng đầu → triệt tiêu vanishing gradient.

**Code** (`src/models.py:_ResBlock1D`):
```python
def forward(self, x):
    h = F.relu(self.bn1(self.conv1(x)))
    h = self.bn2(self.conv2(h))
    return F.relu(h + self.short(x))   # ← KEY: residual + shortcut
```

**Kiến trúc cụ thể**:
- stem: Conv7 → BN → ReLU
- 3 stage × 2 block, downsample (stride=2) ở block đầu mỗi stage trừ stage 0
- AdaptiveAvgPool1d(1) → embedding 256-d → head 12-class

**Kết quả**: **0.7677** — vượt CNN deep +0.026.

⇒ **C05 trở thành backbone "cost-effective"** cho phase D/E/G (rẻ hơn BiLSTM, mạnh hơn CNN).

---

## Slide 19 — C06: TCN (Temporal Convolutional Network)

**Bản chất TCN** (Bai 2018):
- **Dilated causal convolution**: dilation $d_i = 2^i$ ⇒ receptive field tăng **mũ** theo độ sâu.
- 4 block với dilation 1, 2, 4, 8 ⇒ RF lý thuyết = (k−1)·(2^4 − 1)·2 = **120 mẫu** ≈ toàn cửa sổ.
- Block có residual + dropout.

**Code** (`src/models.py:_TCNBlock`):
```python
pad = (k - 1) * dilation
self.conv1 = nn.Conv1d(c_in, c_out, k, padding=pad, dilation=dilation)
# crop pad cuối để giữ độ dài → causal
```

**Vì sao thua ResNet trong phase này (0.76 < 0.77)?**:
- TCN ít nông hơn ResNet (4 block vs 6 block) ⇒ ít capacity.
- Causal padding lãng phí một phần input ở 2 đầu.
- std=0.031 (cao) ⇒ kết quả không ổn định giữa các fold.

---

## Slide 20 — 🏆 C07: BiLSTM + Attention pooling

**Bản chất BiLSTM-Attn**:

1. **BiLSTM 2 lớp, hidden=128**:
   - Forward LSTM đọc chuỗi từ trái sang phải, backward từ phải sang trái.
   - Output mỗi step: $h_t = [\overrightarrow{h_t} ; \overleftarrow{h_t}]$ chiều 256.
   - Bộ nhớ ngắn-dài hạn qua cell state $C_t$ và 3 gate (input, forget, output).

2. **Attention pooling** (thay cho average pool):
   $$\alpha_t = \text{softmax}(W h_t),\quad z = \sum_t \alpha_t h_t$$
   - Mạng tự học **trọng số $\alpha_t$ cho từng time-step** — tập trung vào phần "có thông tin nhất" (ví dụ pha tiếp đất khi đi bộ).

**Code** (`src/models.py:BiLSTMAttn`):
```python
self.lstm = nn.LSTM(in_channels, hidden, num_layers=2,
                    batch_first=True, bidirectional=True, dropout=0.3)
self.attn = nn.Linear(2 * hidden, 1)
# forward
h, _ = self.lstm(x.transpose(1, 2))           # (B, T, 2*hidden)
a = torch.softmax(self.attn(h).squeeze(-1), dim=1)  # (B, T)
z = (h * a.unsqueeze(-1)).sum(dim=1)          # (B, 2*hidden)
```

**Kết quả**: **0.7822** — best phase C.

---

## Slide 21 — Vì sao chọn ResNet (C05) làm xương sống dù C07 cao hơn?

| Tiêu chí | C05 ResNet1D | C07 BiLSTM-Attn |
|---|---|---|
| macro-F1 | 0.7677 | **0.7822** |
| Runtime/fold | ~240s | ~234s nhưng 80ep |
| Tổng 3-fold runtime | **~720s** | ~700s (gần như nhau) |
| Tham số | ~1.2M | ~0.4M |
| Forward parallelizable | **Có** (Conv) | Không (LSTM tuần tự) |
| Inference batch latency | Thấp | Cao hơn |

**Quyết định**: phase D/E/G cần chạy **20+ runs** ⇒ chọn ResNet1D vì ổn định, dễ parallel, và chênh lệch F1 chỉ 0.015 (nhỏ hơn std giữa các fold).

⇒ **Backbone phase D/E/G = ResNet1D [64,128,256], dropout 0.3**.

---

# PHẦN D — Phase D: Loss & Class Weighting

> **Câu hỏi phase D**: Class mất cân bằng (userQ ~900 cửa sổ vs userD 5993). Loss + class-weight nào bù mất cân bằng tốt nhất?
> **Backbone cố định**: ResNet1D [64,128,256] + B04 setup + aug đầy đủ.

## Slide 22 — Phase D tổng quan

| Run | Loss type | Class weight | macro-F1 |
|---|---|---|---|
| D01 | CE | none | 0.7664 |
| D02 | CE | sqrt-inv-freq | 0.7658 |
| D03 | CE | effective-num β=0.999 | 0.7678 |
| D04 | Focal γ=2 | none | 0.7573 |
| D05 | Focal γ=2 | sqrt-inv-freq | 0.7604 |
| D06 | LabelSmooth 0.1 | inv-freq | 0.7727 |
| **D07 ★** | **LabelSmooth 0.1** | **sqrt-inv-freq** | **0.7737** |

---

## Slide 23 — Bản chất class-weighting (file `src/train.py:_class_weights`)

Cho `n_c` = số mẫu class c, `N` = tổng:

| Strategy | Công thức | Đặc điểm |
|---|---|---|
| `none` | $w_c = 1$ | Không bù gì, dựa vào loss tự cân bằng |
| `invfreq` | $w_c = N/n_c$, rồi chuẩn hoá $\bar w=1$ | Bù mạnh nhất — class hiếm có gradient lớn |
| `sqrtinvfreq` | $w_c = \sqrt{N/n_c}$ | Bù dịu hơn — tránh ép quá lệch class hiếm noisy |
| `effnum` (β=0.999) | $w_c = (1-\beta)/(1-\beta^{n_c})$ | "Effective number" Cui 2019, smooth giữa invfreq và uniform |

**Code**:
```python
counts = np.bincount(y, minlength=n_classes)
if strategy == "invfreq":   w = counts.sum() / counts
elif strategy == "sqrtinvfreq": w = np.sqrt(counts.sum() / counts)
elif strategy == "effnum":  w = (1 - beta) / (1 - beta**counts)
w = w / w.mean()    # ← chuẩn hoá để mean(w)=1
```

---

## Slide 24 — D01–D03: 3 chiến lược class-weight với CE

**CE chuẩn**:
$$\mathcal L = -\frac{1}{B}\sum_i w_{y_i} \log\frac{e^{z_{i,y_i}}}{\sum_j e^{z_{i,j}}}$$

| Run | Class weight | F1 |
|---|---|---|
| D01 | none | 0.7664 |
| D02 | sqrt-inv-freq | 0.7658 |
| D03 | effective-num | 0.7678 |

**Phát hiện 1 (quan trọng)**: D01 (không weight) gần như **bằng** D02/D03 (có weight). Tức là **mất cân bằng 1:7 không nghiêm trọng** với ResNet + 80 epoch — mạng tự xử lý được.

**Phát hiện 2**: D03 (effnum) nhỉnh nhất nhưng chỉ +0.001 — không đáng kể.

⇒ Class weight không phải đòn bẩy. Nhưng giữ `invfreq` làm default cho phase E (vì C07 dùng invfreq).

---

## Slide 25 — D04/D05: Focal Loss

**Bản chất Focal Loss** (Lin 2017):
$$\mathcal L_{\text{focal}} = -w_y (1 - p_y)^\gamma \log p_y$$
- $(1-p_y)^\gamma$ là **focusing term**: khi mô hình đã tự tin ($p_y\to 1$), gradient → 0 ⇒ "không lãng phí năng lượng vào easy examples", tập trung học hard examples.
- γ=2 là setting chuẩn (Lin 2017 cho object detection 1:1000).

**Code** (`src/train.py:FocalLoss`):
```python
logp = F.log_softmax(logits, dim=-1); p = logp.exp()
nll = F.nll_loss(((1 - p) ** gamma) * logp, target, weight=weight)
```

**Kết quả**:
- D04 (γ=2, no weight): **0.7573** — sụt 0.009 vs D01.
- D05 (γ=2 + sqrt weight): **0.7604** — vẫn dưới CE.

**Vì sao Focal thua CE ở đây?**:
- Focal thiết kế cho **mất cân bằng cực đoan** (1:1000+ trong object detection background vs foreground).
- Ở đây K=12, ratio ~1:7 ⇒ "easy examples" thực ra **ít** — focal đang downweight nhầm các mẫu hữu ích.
- Hyperparameter γ=2 cứng có thể quá khắt khe.

⇒ **Bài học**: chọn loss theo distribution thực tế, không theo "novelty paper".

---

## Slide 26 — D06/D07: Label Smoothing

**Bản chất Label Smoothing** (Szegedy 2016):
- Thay one-hot target $[0,...,1,...,0]$ bằng phân phối mềm:
$$y_{\text{soft}} = (1-\alpha)\cdot \text{onehot} + \alpha/K$$
- Với α=0.1, K=12: target mềm = 0.9 cho class đúng, 0.0083 cho mỗi class sai.
- Loss = KL(y_soft || softmax(logits)).

**Hiệu ứng**:
- Mạng **không cố ép logit → ∞** cho class đúng ⇒ **giảm overconfidence**.
- Embedding tách lớp **đều hơn** trong không gian latent (Müller 2019).
- Có lợi cho **open-set** vì softmax max-prob bớt "saturate".

**Code**: PyTorch native — chỉ một dòng:
```python
return nn.CrossEntropyLoss(weight=weights, label_smoothing=0.1)
```

**Kết quả**:
- D06 (α=0.1, invfreq): 0.7727
- D07 (α=0.1, sqrt-invfreq): **0.7737** ← winner phase D

---

## Slide 27 — D07 thắng vì sao?

**Phân tích so sánh D06 vs D07**:
- D06 dùng `invfreq` (gradient mạnh cho class hiếm).
- D07 dùng `sqrt(invfreq)` (gradient dịu hơn).
- userQ là class hiếm (~900 mẫu) **nhưng cũng là class noisy** (chỉ 3 file).
- ⇒ `invfreq` ép gradient mạnh vào userQ noisy → over-fit vào noise.
- ⇒ `sqrt(invfreq)` cân bằng giữa "bù hiếm" và "không bị noise dắt" tốt hơn.

⇒ **D07 = LS 0.1 + sqrt-invfreq** chọn làm default cho phase E nếu cần loss-tweak (nhưng phase E dùng CE+invfreq vẫn winner — vì augmentation lấn át loss).

---

## Slide 28 — Kết luận phase D

**Phát hiện then chốt**: cả D01–D07 (max 0.7737) đều **thấp hơn C07 (0.7822)**.

⇒ **Loss & class-weight KHÔNG phải đòn bẩy chính** trong bài này.

**Vì sao?**:
- K=12 nhỏ ⇒ mất cân bằng nhẹ.
- Mô hình ResNet đã đủ regularization qua BatchNorm + dropout.
- Augmentation đang ON (jitter+scale+rotation) — đây mới là phần đáng nghi.

⇒ **Phase E sẽ trả lời**: vấn đề thực sự nằm ở augmentation.

---

## Slide 29 — Phase D — bài học

> "Một phase với 7 runs *toàn null result* vẫn rất giá trị: nó loại bỏ một giả thuyết (loss tweaking) và **chuyển trọng tâm sang augmentation**. Nếu không chạy phase D, có thể đã phí thời gian sửa loss thay vì sửa aug."

Code chạy lại D07:
```bash
python -m scripts.run_experiment --config experiments/configs/D07_ls01_sqrt.yaml
```

---

# PHẦN E — Phase E: Augmentation (winner)

> **Câu hỏi phase E**: Augmentation đang ON theo 3 phép mặc định: jitter (σ=0.02), scaling (0.9–1.1), rotation 3D (±0.1 rad). Có phép nào đang **gây hại**?
> **Backbone**: ResNet1D + B04 setup + CE invfreq.

## Slide 30 — Phase E tổng quan (TÂM ĐIỂM CỦA CẢ CAMPAIGN)

| Run | Augmentation | macro-F1 | std | Δ vs C07 |
|---|---|---|---|---|
| C07 ref | jitter+scale+rotation (default) | 0.7822 | 0.019 | — |
| **E01** | **OFF (không augment)** | 0.8258 | 0.039 | **+0.044** |
| E02 | jitter+scale (BỎ rotation) | 0.7665 | 0.034 | −0.016 |
| **E03 ★** | **CHỈ rotation ±0.1 rad** | **0.8266** | 0.035 | **+0.044** |
| E04 | rotation lớn θ=0.2 rad | 0.7661 | 0.029 | −0.016 |
| E05 | aug đầy đủ + time-warp | 0.7995 | 0.025 | +0.017 |
| E06 | mixup α=0.2 | 0.7677 | 0.021 | −0.014 |
| E07 | cutmix α=1.0 | 0.7677 | 0.021 | −0.014 |
| E08 | jitter σ=0.05 (lớn) | 0.7162 | 0.019 | −0.066 |

---

## Slide 31 — Bản chất 3 phép augment mặc định (file `src/datasets.py`)

### (1) Jitter — Gaussian noise additive
**Công thức**: $x' = x + \mathcal{N}(0, \sigma^2 I)$, σ=0.02.
**Code** (`datasets.py:85`):
```python
if self.use_jitter and self.jitter_sigma > 0:
    x = x + self.rng.normal(0, self.jitter_sigma, size=x.shape).astype(np.float32)
```
**Mục đích lý thuyết**: mô phỏng nhiễu cảm biến.

### (2) Scaling — multiplicative scalar
**Công thức**: $x' = s\cdot x$, $s\sim U[0.9, 1.1]$.
**Code** (`datasets.py:82`):
```python
if self.use_scale:
    s = self.rng.uniform(0.9, 1.1)
    x = x * s
```
**Mục đích lý thuyết**: mô phỏng người cầm hơi mạnh/nhẹ.

### (3) Rotation — 3D rotation matrix đồng bộ acc+gyro
**Công thức**: $x'_{\text{acc}} = R\cdot x_{\text{acc}}$, $x'_{\text{gyro}} = R\cdot x_{\text{gyro}}$, $R = R_z R_y R_x$ với $\theta_{x,y,z}\sim U[-0.1, 0.1]$ rad.
**Code** (`datasets.py:76–81`):
```python
if self.use_rotation and x.shape[1] >= 6:
    tx, ty, tz = self.rng.uniform(-self.rot_theta, self.rot_theta, size=3)
    R = _rotation_matrix(tx, ty, tz).astype(np.float32)
    x = x.copy()
    x[:, 0:3] = x[:, 0:3] @ R.T   # acc
    x[:, 3:6] = x[:, 3:6] @ R.T   # gyro — CÙNG ma trận R!
```
**Mục đích lý thuyết**: mô phỏng người cầm điện thoại nghiêng nhẹ giữa các phiên ghi.

---

## Slide 32 — E01: tắt augment hoàn toàn

**Cấu hình**: `augment.enabled = false` ⇒ mạng học trực tiếp tensor đã chuẩn hoá.

**Kết quả**: 0.7822 → **0.8258** (+0.044) — **vọt lên top 2** toàn cuộc!

**Phân tích từng fold** (xem `log.csv`):
- fold0: 0.8248
- fold1: 0.7791
- fold2: **0.8736** ← max trong campaign

**Diễn giải đầu tiên**: augmentation đang **hại** mô hình. Có ít nhất 1 phép trong 3 phép mặc định **xoá thông tin nhận diện**.

⇒ Cần thí nghiệm tách từng phép để xác định thủ phạm.

---

## Slide 33 — E02 vs E03: ablation tách rotation

| Run | Rotation | Jitter | Scale | F1 |
|---|---|---|---|---|
| C07 ref | ✓ | ✓ | ✓ | 0.7822 |
| E01 | ✗ | ✗ | ✗ | 0.8258 |
| **E02** | **✗** | ✓ | ✓ | 0.7665 |
| **E03 ★** | **✓** | ✗ | ✗ | **0.8266** |

**Logic suy diễn**:
- E02 (BỎ rotation, GIỮ jitter+scale) sụt **mạnh** xuống 0.766 ⇒ jitter+scale **chủ động phá**.
- E03 (GIỮ rotation, BỎ jitter+scale) đạt **0.8266** — cao nhất tuyệt đối ⇒ rotation **chủ động giúp**.
- E03 > E01 chứng minh: rotation đúng liều **không phải neutral**, mà là **+0.0008 thực tế**.

⇒ **Thủ phạm = jitter + scale**. **Người hùng = rotation**.

---

## Slide 34 — E04: tăng rotation lên θ=0.2

**Cấu hình**: rotation θ=0.2 rad (~11.5°) thay vì 0.1 rad (~5.7°). Vẫn giữ jitter+scale (default).

**Kết quả**: **0.7661** — sụt mạnh.

**Diễn giải**:
- Người dùng cầm máy lệch ±5–10° giữa các phiên ⇒ rotation ±5.7° **đúng phân phối thực**.
- Rotation ±11.5° **vượt phân phối thực** ⇒ tạo mẫu "không tồn tại trong domain" ⇒ mô hình học invariance giả.
- Đặc biệt: rotation lớn **xáo trộn hướng trọng lực** trong acc — vốn là tín hiệu phân biệt tư thế quan trọng.

⇒ **Vùng vàng của rotation rất hẹp (~5–10°)**. Quá ít → không augment; quá nhiều → phá vật lý.

---

## Slide 35 — E05: thêm time-warp

**Bản chất Time-warp** (Um 2017):
- Tạo cubic-spline warp trục thời gian: $t' = t + \delta(t)$ với $\delta$ là spline qua n_knots điểm random.
- Mục đích: mô phỏng người đi nhanh/chậm tạm thời.

**Code** (`datasets.py:_time_warp`):
```python
knot_x = np.linspace(0, T-1, n_knots)
knot_y = knot_x + rng.normal(0, sigma * T / n_knots, size=n_knots)
new_idx = np.interp(np.arange(T), knot_y, knot_x)
out[:, c] = np.interp(new_idx, np.arange(T), x[:, c])
```

**Kết quả**: **0.7995** — tốt hơn C07 (+0.017) nhưng dưới E03 (−0.027).

**Diễn giải**: time-warp có ích, nhưng kết hợp với jitter+scale vẫn bị kéo xuống. Nếu thử `time-warp only` trong tương lai có thể vượt E03.

---

## Slide 36 — E06/E07: Mixup & CutMix

**Bản chất Mixup** (Zhang 2018):
- $\tilde x = \lambda x_a + (1-\lambda) x_b$, $\lambda\sim\text{Beta}(\alpha,\alpha)$.
- $\tilde y = \lambda y_a + (1-\lambda) y_b$ ⇒ loss = $\lambda\,\text{CE}(\tilde x, y_a) + (1-\lambda)\,\text{CE}(\tilde x, y_b)$.

**CutMix** (Yun 2019): cắt vùng từ mẫu khác dán vào (theo trục thời gian thay vì không gian ảnh).

**Code** (`datasets.py:mixup_batch`, `cutmix_batch`):
```python
lam = float(rng.beta(alpha, alpha))
idx = torch.randperm(B)
x_m = lam * x + (1 - lam) * x[idx]
return x_m, y, y[idx], lam
# loss = lam * CE(out, y_a) + (1-lam) * CE(out, y_b)
```

**Kết quả**: cả E06 (mixup α=0.2) và E07 (cutmix α=1.0) đều **0.7677** — sụt vs C07.

**Vì sao thất bại trong identity task?**:
- Bài identification cần **class boundary sắc nét**. Mixup làm mờ boundary.
- Trong image classification ImageNet (1000 class), mỗi class có 1000+ mẫu, mixup là "free regularization". Ở đây K=12, mỗi class 2k–6k mẫu, mạng đã có đủ regularization.
- Mixup user A + user B = một "user lai" không tồn tại — phá tính rời rạc của identity.

---

## Slide 37 — E08: jitter σ tăng lên 0.05

**Cấu hình**: jitter σ=0.02 → **σ=0.05** (gấp 2.5×). Giữ scale + rotation default.

**Kết quả**: **0.7162** — sụt mạnh **−0.066** vs C07!

**Diễn giải**:
- Jitter σ=0.05 trên dữ liệu đã chuẩn hoá (mean=0, std≈1) tương đương SNR ~1/0.05 = 20 ⇒ không quá tệ về vật lý.
- Nhưng: **chữ ký người dùng nằm trong vùng tần số trung bình**. Jitter là white noise (mọi tần số) ⇒ phủ lên các mẫu **vi tế** giúp phân biệt user.
- Kết quả này xác nhận thêm: **jitter σ=0.02 đã đủ hại**, σ=0.05 chỉ nhân lên.

⇒ Khẳng định **jitter không phù hợp với inertial sạch**.

---

## Slide 38 — Tổng kết phase E: vì sao rotation thắng?

### (1) Rotation đúng vì **mô phỏng đúng nguồn biến thiên hợp lệ**:
- Người dùng không cầm điện thoại ở góc giống hệt giữa các phiên → biến thiên ±5–10° là **tự nhiên**.
- Áp dụng cùng R cho acc+gyro **bảo toàn vật lý**: gyro là đạo hàm hướng trong cùng frame với acc.

### (2) Jitter sai vì **giả lập noise không tồn tại**:
- Sau filtfilt 20 Hz, tín hiệu đã "sạch". Jitter là white noise full-band → ép mạng học invariance đối với cái không có thật.

### (3) Scale sai vì **xoá thông tin có ích**:
- Biên độ acc/gyro **chính là** đặc trưng phân biệt mạnh nhất giữa user (vóc dáng khác → biên độ vung khác).
- Augment scale = chủ động xoá thông tin định danh.

### (4) Mixup/CutMix sai vì **phá class boundary trong identity task**.

### (5) Vùng vàng θ rotation rất hẹp:
- θ=0.1 rad: tốt (+0.0444 vs C07)
- θ=0.2 rad: tệ (−0.016 vs C07)
- ⇒ **không phải càng nhiều aug càng tốt**.

> **Câu chốt**: "Augmentation phải khớp với *invariance hợp lệ trong miền*. Với IMU sạch, chỉ rotation đáp ứng — và đáp ứng tuyệt vời."

---

# PHẦN G — Phase G: Scale-up architecture (kiểm chứng trần)

> **Câu hỏi phase G**: E03 đã 0.83. Nếu nhân 2/4 lần số filter trên ResNet/TCN, có vượt 0.85 không?
> **Lưu ý**: phase G chạy với aug **default** (jitter+scale+rotation) — chưa biết về phát hiện E03 lúc thiết kế.

## Slide 39 — Phase G tổng quan

| Run | Mô hình | macro-F1 | std |
|---|---|---|---|
| G01 | ResNet [128,256,512] | 0.7771 | 0.025 |
| G02 | ResNet wide [96,192,384] dropout 0.4 | 0.7744 | 0.022 |
| G03 | TCN [128,128,256,256] | 0.7775 | 0.027 |
| G04 | CNN [64,128,256,512] kernels [9,7,5,3] | 0.7540 | 0.022 |
| G05 | ResNet [128,256,512] 120ep + ES | 0.7710 | 0.014 |

⇒ **Tất cả G đều dưới E03 (0.8266)**.

---

## Slide 40 — G01: ResNet doubled

**Cấu hình**: filters [64,128,256] → **[128,256,512]**. Tham số ~5M (vs 1.2M).

**Kết quả**: 0.7677 (C05) → **0.7771** (+0.009).

**Diễn giải**: scale-up mô hình +0.009 — quá ít so với E03 +0.044. Vì sao?
- Aug default vẫn **chứa jitter+scale có hại**. Mô hình lớn hơn nhưng "input đã bị phá" ⇒ trần không đổi.
- 30k mẫu × 5M params → tỉ lệ 1:170, dễ overfit.

---

## Slide 41 — G02: ResNet wide + dropout cao

**Cấu hình**: filters `[96,192,384]`, dropout 0.4.

**Lý do thử**: nếu G01 overfit, tăng dropout có thể cứu.

**Kết quả**: **0.7744** — gần như G01. Tăng dropout không cứu vì vấn đề ở **input augmentation**, không phải capacity.

---

## Slide 42 — G03: TCN big

**Cấu hình**: channels `[128,128,256,256]`, kernel=5, dilation 1,2,4,8.

**Receptive field**: (5-1)·(2^4-1)·2 = 120 mẫu ≈ toàn cửa sổ.

**Kết quả**: **0.7775** — best phase G nhưng vẫn dưới E03 0.5%.

---

## Slide 43 — G04: CNN huge — counter-example

**Cấu hình**: filters `[64,128,256,512]`, kernels `[9,7,5,3]`.

**Kết quả**: **0.7540** — sụt vs C04 (0.7421 với CNN deep nhỏ hơn).

**Vì sao?**: CNN không có skip connection ⇒ tăng độ sâu mà không có residual ⇒ vanishing gradient ⇒ mất F1.

⇒ Bài học: **không phải kiến trúc lớn nào cũng tốt — phải có cơ chế truyền gradient (skip / dilation)**.

---

## Slide 44 — Tổng kết phase G

**Thông điệp**: **Augmentation đúng > kiến trúc lớn hơn**.

- ResNet [64,128,256] + rotation-only (E03) = 0.8266
- ResNet [128,256,512] + jitter+scale+rotation (G01) = 0.7771
- ⇒ Mô hình nhỏ hơn 4× nhưng aug đúng **vượt** mô hình to với aug sai.

⇒ **Trần thực sự không phải capacity, mà là chiến lược augmentation và lượng dữ liệu**.

> **Hướng tương lai**: chạy G01 với rotation-only → kỳ vọng > 0.84. Nhưng G05 (120ep ES) đã cho std nhỏ nhất (0.014) ⇒ E03 + scale-up sẽ ổn định hơn nữa.

---

# PHẦN H/J — RF baseline & Open-set

## Slide 45 — Phase H: Random Forest trên đặc trưng thủ công

**62 đặc trưng** (file `src/features.py`):
- Thống kê thời gian: mean, std, MAD, min, max, IQR, energy × 6 trục = 42
- Tần số (FFT): dominant freq + spectral entropy × 6 trục = 12
- Cross-correlation 9 cặp + SMA 2 = 9+2 = ... tổng 62

**Random Forest**: 200 trees, `class_weight="balanced"`, `n_jobs=-1`, dùng cùng StratifiedGroupKFold.

**Kết quả**: macro-F1 = **0.785 ± 0.020** (đời trước).

⇒ Trước phase E, RF còn vượt CNN. **Sau phase E**, CNN (0.8266) **đã vượt** RF (+0.04). Augmentation đúng là chìa khoá.

---

## Slide 46 — Phase J: Open-set scoring

**File**: `src/openset.py`.

**Bài toán**: với x test, tính score $s(x)$ "known". Đặt ngưỡng τ → s≥τ nhận, s<τ từ chối.

**Method 1 — Softmax max-prob**:
$$s(x) = \max_c \text{softmax}(z_c) = \max_c \frac{e^{z_c}}{\sum_k e^{z_k}}$$

**Method 2 — Mahalanobis trên embedding 128/256-d**:
$$d_c(x) = (e(x)-\mu_c)^T \Sigma_c^{-1} (e(x)-\mu_c),\quad s(x) = -\min_c d_c(x)$$
Với $\mu_c, \Sigma_c$ ước lượng từ train embedding (covariance regularize $\lambda=10^{-3}I$).

**Kết quả** (trên CNN baseline, đời trước):
| Method | AUROC | TPR @ FPR=5% |
|---|---|---|
| Softmax | 0.659 | ~0.18 |
| Mahalanobis | 0.610 | ~0.15 |

⇒ Có tín hiệu nhưng chưa production. Hướng nâng cấp: contrastive learning + chạy lại trên embedding E03.

---

# PHẦN Z — Tổng kết

## Slide 47 — Đường tiến hoá F1 toàn campaign

```
Baseline gốc:   0.6451
  ↓ +0.045  (B04: OneCycleLR)
B04:            0.6906
  ↓ +0.092  (C07: BiLSTM-Attn)
C07:            0.7822
  ↓ −0.009  (D07: loss-tweak — không cải thiện)
D07:            0.7737
  ↓ +0.044  (E03: rotation-only) ← BƯỚC ĐỘT PHÁ
E03:            0.8266  ★

Tổng: +0.181 macro-F1 = +28% tương đối.
```

---

## Slide 48 — 5 bài học cốt lõi

1. **Augmentation là đòn bẩy lớn nhất** — không phải kiến trúc.
   Phase E +0.044 = nhiều hơn phase B (+0.045) trong khi rẻ hơn 10×.

2. **Augmentation phải khớp với invariance hợp lệ của miền**.
   Rotation đúng cho IMU; jitter/scale/mixup sai vì xoá thông tin định danh.

3. **"Vùng vàng" hyperparameter aug rất hẹp**.
   θ=0.1 rad tốt; θ=0.2 rad tệ. σ jitter=0.02 trung tính; σ=0.05 phá huỷ.

4. **Loss/class-weight chỉ là yếu tố phụ** khi K nhỏ và mất cân bằng nhẹ (1:7).

5. **Đánh giá nghiêm (group-by-file)** quan trọng hơn cả mô hình — nó định nghĩa "chiến thắng" có nghĩa hay không.

---

## Slide 49 — Cấu hình production khuyến nghị

```yaml
# Sao chép từ E03_rotation_only.yaml
name: production
phase: deploy
n_splits: 3
epochs: 80
batch_size: 128
seed: 42

model:
  type: resnet            # ResNet1D
  filters: [64, 128, 256]
  dropout: 0.3

optim:   {type: adam,  lr: 0.0001, weight_decay: 0.0001}
sched:   {type: onecycle, max_lr: 0.003}
loss:    {type: ce, class_weight: invfreq}

augment:
  enabled: true
  use_rotation: true        # ← KEY
  use_jitter:   false       # ← KEY (tắt!)
  use_scale:    false       # ← KEY (tắt!)
  rot_theta:    0.1         # ±5.7° — vùng vàng
```

Lệnh chạy lại:
```bash
python -m scripts.run_experiment \
       --config experiments/configs/E03_rotation_only.yaml
```

---

## Slide 50 — Q&A có thể bị hỏi

**Q1. Sao không dùng Transformer?**
> 39k mẫu, K=12. Transformer cần dữ liệu lớn hoặc pretrain. ResNet1D đủ và rẻ hơn nhiều.

**Q2. Std E03 cao (0.035) có đáng lo?**
> Chấp nhận được. Less aug ⇒ mô hình bám phân phối train sát hơn ⇒ fold lệch chịu phạt mạnh. F1 trung bình vẫn vượt trội. Fold 2 đạt 0.870 (max campaign).

**Q3. Vì sao open-set chỉ 0.66?**
> CNN baseline embedding chưa tách lớp đủ. Hướng cải thiện: contrastive learning + label smoothing + chạy lại trên backbone E03.

**Q4. Có rò rỉ dữ liệu không?**
> Không. Group-by-file đảm bảo file train không bao giờ ở val. Augment chỉ chạy trên train. Scaler fit chỉ trên train rồi áp lên val.

**Q5. Vì sao 3 fold thay vì 5?**
> userQ chỉ có 3 file. k=5 ⇒ fold thiếu userQ trong val ⇒ không đánh giá đủ 12 class.

**Q6. Augment rotation ±0.1 rad nghĩa là gì?**
> ~5.7°. Mô phỏng người dùng cầm máy nghiêng nhẹ giữa các phiên. Vượt quá (E04 θ=0.2) bắt đầu phá vì không còn vật lý hợp lệ.

**Q7. RF (0.785) có thua CNN (0.83) không?**
> Trước phase E thì RF còn thắng. Sau khi tìm ra rotation-only, CNN vượt. Nhưng RF vẫn là baseline mạnh, đáng giữ làm điểm so sánh.

**Q8. Vì sao OneCycleLR thắng Cosine?**
> OneCycle có pha warm-up đẩy `lr` lên cao giữa training → buộc mô hình tìm minimum rộng (flat); Cosine chỉ đơn giản giảm từ đầu.

**Q9. Tại sao ResNet thắng CNN thẳng?**
> Skip connection cho gradient chảy thẳng về tầng đầu ⇒ triệt vanishing gradient ⇒ có thể tăng độ sâu hiệu quả.

**Q10. Mixup tốt cho ImageNet, sao thua ở đây?**
> Bài identity cần boundary sắc nét. Trộn 2 user thành "user lai" phá tính rời rạc. Mixup chỉ tốt khi K rất lớn và mỗi class đông mẫu.

---

## Phụ lục — Stack công nghệ

| Lớp | Công cụ | File chính |
|---|---|---|
| Python 3.12 | – | – |
| DSP | scipy.signal (`butter`, `filtfilt`, `resample_poly`) | `src/preprocess.py` |
| Data | pandas 2.2, numpy 2.2 | `src/io.py`, `src/datasets.py` |
| ML cổ điển | scikit-learn 1.6 (RF, StratifiedGroupKFold, metrics) | `src/evaluate.py`, `src/train.py` |
| Deep learning | PyTorch 2.6 (Conv1d, BatchNorm1d, LSTM, AdaptiveAvgPool1d) | `src/models.py`, `src/train.py` |
| Augmentation | numpy random + scipy interp | `src/datasets.py` |
| Logging | csv + json (no DB) | `src/experiment.py` |
| Config | YAML | `experiments/configs/*.yaml` |

---

*Tổng 36 runs · ~5.2 giờ compute · Best E03 = 0.8266 ± 0.0354 · Cập nhật 2026-05-18*
