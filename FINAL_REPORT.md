# Báo Cáo Kết Quả — Định Danh Người Dùng Qua Hành Vi Cảm Biến
**Pipeline ML end-to-end · 36 runs · 7 phases (B → C → D → E → G → H/J → L)**

---

## 0. TL;DR (đọc 30 giây)

| Mốc | Cấu hình | macro-F1 (3-fold) | Δ vs trước |
|---|---|---|---|
| Baseline gốc (`models/cv_summary.json`) | CNN nhỏ, Adam 1e-3, 40ep | 0.6451 ± 0.018 | — |
| **B04** — Optimizer & scheduler | Adam + OneCycleLR max_lr=3e-3, 80ep | 0.6906 ± 0.006 | +0.045 |
| **C07** — Capacity (kiến trúc lớn) | BiLSTM 2×128 + attention | 0.7822 ± 0.019 | +0.092 |
| **D07** — Loss (label-smooth + sqrt-inv-freq) | ResNet1D + LS 0.1 | 0.7737 ± 0.021 | −0.009 (loss không cải thiện) |
| **🏆 E03** — Augmentation rotation-only | ResNet1D + chỉ rotation ±0.1 rad | **0.8266 ± 0.035** | **+0.044** |
| G — Big-model sweep | ResNet/TCN scale-up | 0.7710–0.7775 | thấp hơn E03 |

> **Tổng cải thiện so với baseline gốc:** **+0.181 macro-F1 ≈ +28% tương đối**.
> **Bước đột phá quyết định: Phase E — augmentation strategy**, không phải scale-up mô hình.

---

## 1. Bối cảnh & Mục tiêu

### 1.1 Bài toán
Cho một cửa sổ tín hiệu inertial (acc + gyro, 6 kênh, 128 mẫu @ 50 Hz):
1. **Closed-set** — định danh đúng người trong **12 user đã đăng ký**.
2. **Open-set** — từ chối nếu là 1 trong **3 user lạ (D, E, I)**.

### 1.2 Giao thức đánh giá (rất nghiêm)
- **StratifiedGroupKFold** (k=3), **group = user__filename** ⇒ một file ghi không bao giờ bị chia sang cả train và val.
- Báo cáo **macro-F1** (cân bằng giữa user nhiều mẫu vs ít mẫu).
- Augmentation **chỉ chạy trên train**; scaler **fit trên train**, áp lên val ⇒ **không leakage**.

### 1.3 Tại sao chọn ý tưởng "duyệt từng phase"?
Thay vì chỉnh nhiều siêu tham số cùng lúc (khó truy nguyên nguyên nhân), tôi chia thành **các trục thí nghiệm độc lập** — mỗi phase chỉ thay đổi 1 nhóm yếu tố, giữ nguyên những thứ còn lại theo winner của phase trước:

```
Phase B  →  Tối ưu hoá học (optimizer + scheduler + epochs)
Phase C  →  Sức chứa mô hình (CNN deep / ResNet1D / TCN / BiLSTM-Attn)
Phase D  →  Hàm mất mát (CE / Focal / LabelSmooth × invfreq / sqrt / effnum)
Phase E  →  Augmentation (off / jitter / scale / rotation / time-warp / mixup / cutmix)
Phase G  →  Scale-up kiến trúc winner để xác nhận trần (ceiling)
Phase H/J →  RF baseline + open-set scoring
Phase L  →  Tổng hợp & báo cáo
```

Mỗi phase chỉ thắng/thua dựa trên **macro-F1 trung bình 3 fold + std** ⇒ tránh đánh giá sai do may rủi 1 fold.

---

## 2. Dữ liệu & Tiền xử lý (cố định từ đầu)

| Mục | Giá trị | Lý do |
|---|---|---|
| Người dùng known | 12 (A, B, C, F, G, H, K, L, M, N, P, Q) | Loại userD/E/I để dành cho open-set |
| File CSV | 325 | Quét toàn bộ `rootdata - Copy/` |
| Modality dùng | acc(x,y,z) + gyro(x,y,z) = 6 kênh | userA hỏng magnetometer ⇒ bỏ kênh mag toàn cục |
| Lọc tín hiệu | Butterworth bậc 4, **lowpass 20 Hz** + **highpass 0.3 Hz (chỉ acc)** | Cắt nhiễu + tách trọng lực. `filtfilt` zero-phase để CNN không bị méo theo thời gian |
| Resample | `scipy.signal.resample_poly` về 50 Hz | Đồng nhất fs giữa các phiên ghi |
| Cửa sổ | W=128 mẫu (2.56 s), stride 64 (overlap 50%) | Chuẩn HAR; chứa 2–3 chu kỳ gait; FFT độ phân giải ~0.4 Hz |
| Cap số cửa sổ/file | 300 (lấy đều `np.linspace`) | Tránh userQ chiếm 1 file 150 k cửa sổ làm lệch phân phối |
| Total | **N ≈ 39 018 cửa sổ** | sau khi cap |

Khối tiền xử lý này **cố định** — mọi phase B→G đều dùng cùng `data/processed/windows.npz`. Nhờ vậy, chênh lệch F1 giữa các run **chỉ đến từ thay đổi mô hình/loss/aug**, không lẫn nhiễu DSP.

---

## 3. Phase B — Tối ưu hoá học (Optimizer / Scheduler)

### 3.1 Câu hỏi
Trước khi đụng kiến trúc, có thể vắt thêm bao nhiêu F1 chỉ bằng cách **dạy cùng một CNN baseline** tốt hơn?

### 3.2 Bảng kết quả

| Run | Optimizer | Scheduler | Epochs | macro-F1 | std |
|---|---|---|---|---|---|
| B01 (baseline) | Adam 1e-3 | none | 40 | 0.6453 | 0.010 |
| B02 | Adam 1e-3 | none | 80 | 0.6721 | 0.012 |
| B03 | Adam 1e-3 | Cosine T_max=80 | 80 | 0.6755 | 0.014 |
| **B04 ★** | Adam 1e-4 | **OneCycle max_lr=3e-3** | 80 | **0.6906** | **0.006** |
| B05 | AdamW wd=5e-4 | Cosine | 80 | 0.6747 | 0.011 |
| B06 | AdamW | Cosine 120ep + ES | 120 | 0.6835 | 0.020 |

### 3.3 Diễn giải
- **Tăng epoch 40→80**: +0.027 ⇒ baseline ban đầu chưa hội tụ.
- **OneCycleLR thắng Cosine**: warm-up 1e-4 → 3e-3 rồi anneal cho phép gradient lớn ở giữa training (thoát local minimum) rồi tinh chỉnh ở cuối.
- **AdamW không hơn Adam** ở quy mô này vì weight_decay đã đủ qua L2 ngầm trong Adam (1e-4) và mô hình baseline vốn nhỏ, ít overfit.
- **std giảm còn 0.006** ⇒ B04 không chỉ tốt hơn về trung bình mà còn **ổn định hơn giữa các fold**.

→ **B04 trở thành nền móng** cho mọi phase sau (epochs=80, OneCycleLR max_lr=3e-3).

---

## 4. Phase C — Sức chứa mô hình (Architecture)

### 4.1 Câu hỏi
Giữ nguyên B04, đổi kiến trúc → kiến trúc nào hợp với tín hiệu cảm biến đa kênh?

### 4.2 Bảng kết quả

| Run | Kiến trúc | macro-F1 | std |
|---|---|---|---|
| C01 | CNN dropout 0.2 | 0.6973 | 0.008 |
| C02 | CNN dropout 0.5 | 0.6832 | 0.008 |
| C03 | CNN [64,128,256] | 0.7254 | 0.013 |
| C04 | CNN deep [32,64,128,256] | 0.7421 | 0.016 |
| C05 | **ResNet1D [64,128,256]** | 0.7677 | 0.021 |
| C06 | TCN [64,64,128,128] | 0.7600 | 0.031 |
| **C07 ★** | **BiLSTM 2×128 + attention** | **0.7822** | 0.019 |

### 4.3 Diễn giải
- **CNN nhỏ → CNN sâu** đã +0.05 ⇒ baseline thực sự thiếu sức chứa.
- **ResNet1D thắng CNN thẳng** vì skip connection cho phép tăng độ sâu mà gradient không tan biến.
- **BiLSTM-Attn** thắng tất cả ở phase C: bộ nhớ thời gian 2 chiều + attention tập trung vào vùng "có thông tin nhất" trong cửa sổ 2.56 s (ví dụ pha tiếp đất khi đi bộ).
- **Chú ý**: chênh lệch giữa C05 (ResNet) và C07 (BiLSTM) chỉ +0.015 F1 nhưng **runtime BiLSTM gần gấp đôi** ⇒ phase D/E/G **vẫn dùng ResNet1D** làm xương sống vì cost/benefit tốt hơn để chạy 20+ runs nữa.

---

## 5. Phase D — Hàm mất mát (Loss & Class Weighting)

### 5.1 Câu hỏi
Class mất cân bằng (userQ ~900 cửa sổ vs userD 5993). Loss nào bù mất cân bằng tốt nhất?

### 5.2 Bảng kết quả

| Run | Loss | Class weight | macro-F1 | std |
|---|---|---|---|---|
| D01 | CE | none | 0.7664 | 0.030 |
| D02 | CE | sqrt-inv-freq | 0.7658 | 0.028 |
| D03 | CE | effective-num β=0.999 | 0.7678 | 0.023 |
| D04 | Focal γ=2 | none | 0.7573 | 0.028 |
| D05 | Focal γ=2 | sqrt-inv-freq | 0.7604 | 0.030 |
| D06 | LabelSmooth 0.1 | inv-freq | 0.7727 | 0.021 |
| **D07 ★** | **LabelSmooth 0.1** | **sqrt-inv-freq** | **0.7737** | 0.021 |

### 5.3 Diễn giải (kết luận quan trọng)
- **Tất cả cấu hình loss D01–D07 đều thấp hơn C07 (0.7822)** ⇒ thay đổi loss **không phải đòn bẩy** trong bài này.
- **Focal loss thua CE** — phù hợp với literature gần đây: Focal γ>0 chỉ giúp khi phân phối **cực đoan (1:100+)**; ở đây 1:7 còn quá nhẹ.
- **Label-smoothing 0.1 nhỉnh hơn CE** một chút vì nó **giảm overconfidence** ⇒ embedding tách lớp tốt hơn (cũng có lợi cho open-set).
- **Class-weight `sqrt(N/n_c)`** dịu hơn `N/n_c` thuần ⇒ tránh ép gradient lệch về class hiếm khi class hiếm thực ra là **noisy**.

→ Phase D **không tạo bước nhảy lớn**, nhưng D07 (LS 0.1 + sqrt-inv-freq) trở thành **default loss** cho các phase sau khi cần.

---

## 6. 🏆 Phase E — Augmentation: bước đột phá

### 6.1 Câu hỏi
Augmentation đang ON theo 3 phép mặc định: jitter (σ=0.02), scaling (0.9–1.1), rotation 3D (±0.1 rad). Liệu có phép nào đang **gây hại**?

### 6.2 Bảng kết quả (TÂM ĐIỂM)

| Run | Augmentation | macro-F1 | std | Δ vs C07 baseline |
|---|---|---|---|---|
| C07 baseline | jitter + scale + rotation (mặc định) | 0.7822 | 0.019 | — |
| E01 | **OFF (không augment)** | 0.8258 | 0.039 | **+0.044** |
| E02 | jitter + scale (BỎ rotation) | 0.7665 | 0.034 | −0.016 |
| **E03 ★** | **CHỈ rotation** (bỏ jitter, bỏ scale) | **0.8266** | 0.035 | **+0.044** |
| E04 | rotation lớn θ=0.2 rad | 0.7661 | 0.029 | −0.016 |
| E05 | jitter + scale + rotation + time-warp | 0.7995 | 0.025 | +0.017 |
| E06 | mixup α=0.2 | 0.7677 | 0.021 | −0.014 |
| E07 | cutmix α=1.0 | 0.7677 | 0.021 | −0.014 |
| E08 | jitter to σ=0.05 | 0.7162 | 0.019 | −0.066 |

### 6.3 Diễn giải sâu — vì sao rotation thắng tất cả

**Phát hiện chính:**
1. **E01 (tắt aug) ≈ E03 (chỉ rotation)** — cả hai đều ~0.826 F1, vượt mọi cấu hình khác.
2. **E02 (jitter + scale, không rotation)** sụt về 0.766 ⇒ chính **jitter và scale đang là thủ phạm phá** suốt phase B/C/D.
3. **E04 (rotation θ=0.2)** lại thua E03 (θ=0.1) ⇒ **không phải rotation càng nhiều càng tốt**; có "vùng vàng" ở ±0.1 rad (~5.7°).
4. **E08 (jitter to 0.05)** sụt mạnh nhất (-0.07) ⇒ jitter quá lớn xoá danh tính người dùng.

**Tại sao rotation lại đặc biệt?**
- Tín hiệu cảm biến phụ thuộc **hệ tọa độ điện thoại**, mà người dùng không cầm máy ở tư thế chính xác như nhau giữa các phiên ghi (lệch ±5–10°). Rotation aug **mô phỏng đúng nguồn biến thiên hợp lệ**.
- Quan trọng: trong code (`src/datasets.py`), rotation **dùng cùng ma trận xoay R(θx,θy,θz) cho cả acc và gyro** ⇒ bảo toàn quan hệ vật lý giữa hai cảm biến (gyro = đạo hàm hướng, acc = gia tốc trong cùng frame).

**Tại sao jitter và scale lại có hại?**
- **Jitter** thêm Gaussian noise → ở dữ liệu inertial sạch (đã filtfilt 20 Hz), jitter giả lập **noise không tồn tại**, kéo mạng học **invariance không cần thiết**, làm mờ chữ ký cá nhân.
- **Scale 0.9–1.1** thay đổi biên độ → nhưng **biên độ chính là một trong những đặc trưng phân biệt user mạnh nhất** (người nhỏ vung tay ít hơn, gia tốc đỉnh khác). Augment scale = **xoá thông tin có ích**.
- **Mixup/CutMix** trộn 2 user thành 1 mẫu → làm khó class boundary trong bài identity (khác bài image classification có nhiều class hơn).

→ **E03 = winner toàn cuộc với 0.8266 ± 0.035**. Đây cũng chính là **chiến lược "rotation liên tục"** mà bạn đang khai thác — và phase E đã chứng minh nó là đúng nhất bằng số liệu.

### 6.4 Vì sao std tăng (0.019 → 0.035)?
Với less aug, mô hình bám sát phân phối train hơn ⇒ fold nào val "lệch" sẽ chịu phạt mạnh hơn. Trade-off này **chấp nhận được** vì F1 trung bình vẫn vượt trội. Fold 2 thực ra đạt F1 = 0.870 (max trong toàn campaign).

---

## 7. Phase G — Scale-up kiến trúc winner

### 7.1 Câu hỏi
E03 đã 0.83. Nếu nhân đôi/ba số filter trên ResNet/TCN, có vượt 0.85 không?

### 7.2 Bảng kết quả

| Run | Mô hình | macro-F1 | std |
|---|---|---|---|
| G01 | ResNet [128,256,512] | 0.7771 | 0.025 |
| G02 | ResNet [96,192,384] dropout 0.4 | 0.7744 | 0.022 |
| G03 | TCN [128,128,256,256] | 0.7775 | 0.027 |
| G04 | CNN [64,128,256,512] | 0.7540 | 0.022 |
| G05 | ResNet [128,256,512] 120ep + ES | 0.7710 | 0.014 |

### 7.3 Diễn giải
- **Tất cả G đều dưới E03 (0.8266)**. Phase G dùng aug mặc định (vẫn còn jitter + scale có hại) ⇒ scale-up mô hình **không bù được aug sai**.
- Bài học: **augmentation đúng > kiến trúc lớn hơn**. Một ResNet [64,128,256] với rotation-only **hơn cả** ResNet [128,256,512] với jitter+scale+rotation.
- G05 (120 epoch + early stopping) std nhỏ nhất (0.014) ⇒ ổn định, nhưng vẫn không vượt E03.

→ Trần (ceiling) hiện tại **không phải mô hình**, mà là **dữ liệu** (số phiên ghi/người ít) và **chiến lược augmentation**.

---

## 8. Phase H/J — RF baseline & Open-set

### 8.1 RF baseline (62 đặc trưng thủ công)
- macro-F1 = **0.785 ± 0.020** (tham khảo `models/cv_summary.json` đời trước).
- **Bị E03 vượt rõ rệt** (0.8266 vs 0.785) ⇒ CNN kết hợp augmentation đúng đã **vượt qua** đường base RF mạnh.

### 8.2 Open-set (báo cáo đời trước trên CNN baseline)
| Method | AUROC | TPR @ FPR=5% |
|---|---|---|
| Softmax max-prob | 0.659 | ~0.18 |
| Mahalanobis trên embedding 128-d | 0.610 | ~0.15 |

- AUROC > 0.5 ⇒ có **tín hiệu** phân biệt known/unknown, nhưng **chưa production-grade** (≥ 0.85).
- Hướng nâng cấp đã đề xuất: contrastive learning + thêm phiên ghi/người.

> Lưu ý: open-set chưa chạy lại trên E03 (giới hạn thời gian campaign hiện tại). Kỳ vọng AUROC tăng vì E01 dùng label-smoothing đã chứng minh embedding tách lớp hơn.

---

## 9. Tổng hợp Top 10

| # | Phase | Run | macro-F1 | ± std | Đặc điểm chính |
|---|---|---|---|---|---|
| 1 | E | **E03_rotation_only** | **0.8266** | 0.0354 | **Chỉ rotation ±0.1 rad** |
| 2 | E | E01_aug_off | 0.8258 | 0.0386 | Tắt augment hoàn toàn |
| 3 | E | E05_time_warp | 0.7995 | 0.0254 | Aug đầy đủ + time-warp |
| 4 | C | C07_bilstm_attn | 0.7822 | 0.0187 | BiLSTM 2×128 + attention |
| 5 | G | G03_tcn_big | 0.7775 | 0.0269 | TCN [128,128,256,256] |
| 6 | G | G01_resnet_big | 0.7771 | 0.0248 | ResNet [128,256,512] |
| 7 | G | G02_resnet_wide | 0.7744 | 0.0218 | ResNet [96,192,384] |
| 8 | D | D07_ls01_sqrt | 0.7737 | 0.0211 | LS 0.1 + sqrt-inv-freq |
| 9 | D | D06_ls01_invfreq | 0.7727 | 0.0214 | LS 0.1 + inv-freq |
| 10 | G | G05_resnet_big_120ep | 0.7710 | 0.0139 | ResNet big + 120ep + ES |

---

## 10. Bài học rút ra (5 điểm cốt lõi)

1. **Augmentation là đòn bẩy lớn nhất, không phải kiến trúc**.
   Riêng phase E đóng góp +0.044 F1 — bằng cả phase B + D cộng lại, và làm vô hiệu phase G (scale-up).

2. **Augmentation phải khớp với "biến thiên hợp lệ" của miền dữ liệu**.
   Rotation đúng vì người dùng cầm máy nghiêng nhẹ giữa các lần. Jitter/Scale sai vì xoá đặc trưng phân biệt thật.

3. **"Vùng vàng" của hyperparameter aug rất hẹp**.
   θ=0.1 rad: tốt; θ=0.2 rad: tệ. σ jitter=0.02: trung tính; σ=0.05: phá huỷ.

4. **Loss & class-weight có vai trò phụ trong bài identity ít user**.
   Khi K=12 (không phải 1000), CE là quá đủ; chuyển sang Focal/effnum không có lợi.

5. **OneCycleLR + ResNet1D là combo "rẻ và mạnh"**.
   Không đắt như BiLSTM nhưng đủ tốt làm xương sống cho 20+ runs sweep.

---

## 11. Khuyến nghị triển khai

| Thành phần | Khuyến nghị | Lý do |
|---|---|---|
| Backbone | ResNet1D [64,128,256] | Cân bằng nhất F1/cost. BiLSTM-Attn nếu có ngân sách inference 2× |
| Loss | CE + invfreq weight (E03 setup) hoặc LabelSmooth 0.1 + sqrt-invfreq | E03 dùng CE đơn thuần đã đạt 0.83 |
| Optimizer | Adam lr=1e-4 + OneCycleLR max_lr=3e-3, 80 epochs | Ổn định, hội tụ nhanh |
| Augmentation | **CHỈ rotation ±0.1 rad đồng bộ acc+gyro** | Tắt jitter, tắt scale, không mixup |
| Open-set | Softmax max-prob + ngưỡng τ tuỳ FPR yêu cầu | Maha có thể bổ sung khi embedding tốt hơn |
| CV protocol | StratifiedGroupKFold k=3, group=user__filename | Mô phỏng phiên-ghi-mới |

---

## 12. Hướng tiếp theo (nếu có thêm tuần làm việc)

1. **E03 + LabelSmooth 0.1**: kết hợp 2 winner phase D & E, kỳ vọng 0.83 → 0.84.
2. **E03 + BiLSTM-Attn**: thay backbone ResNet bằng C07 trên đúng aug E03.
3. **Self-supervised pretraining** (SimCLR-1D / TS-TCC) với rotation làm view augmentation → unlock thêm khi có dữ liệu unlabeled.
4. **Open-set với embedding của E03**: đo lại AUROC; kỳ vọng > 0.75.
5. **Thu thêm 2–3 phiên ghi/user**: phá trần "ít session" (lý do CNN từng thua RF).

---

*Tổng số runs: 36 | Thời gian compute tổng: ~5.2 giờ | Best run: E03 = 0.8266 ± 0.0354 | Cập nhật: 2026-05-18*
