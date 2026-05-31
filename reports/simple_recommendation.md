# Hướng đơn giản đề xuất

## Mục tiêu

Giữ pipeline dễ giải thích cho đồ án nhập môn: không sweep nhiều phase, không BiLSTM/TCN/ResNet, không scheduler lạ, không mixup/cutmix. Chỉ dùng hai mô hình chính:

- **Random Forest** trên đặc trưng thống kê thủ công từ cửa sổ cảm biến.
- **CNN 1D** trên chuỗi cảm biến 6 kênh acc/gyro.

## Pipeline nên trình bày

1. Tiền xử lý dữ liệu cảm biến:
   - Chuẩn hoá tần số về 50 Hz.
   - Chia cửa sổ 2.56 giây, overlap 50%.
   - Mỗi mẫu là ma trận `(128, 6)` gồm acc_x/y/z và gyro_x/y/z.
2. Chia đánh giá:
   - Giữ `userD`, `userE`, `userI` cho open-set.
   - 12 user còn lại dùng 3-fold StratifiedGroupKFold.
3. Mô hình 1 - Random Forest:
   - Trích 65 đặc trưng thống kê/FFT/correlation/SMA trên mỗi cửa sổ.
   - RandomForest 300 cây, class_weight balanced_subsample.
4. Mô hình 2 - CNN 1D:
   - 3 lớp Conv1D `[32, 64, 128]`, kernel `[7, 5, 3]`.
   - Adam lr=0.001, CrossEntropy, 40 epoch.
   - Không scheduler, không augmentation, không sweep.

## Kết quả train lại

File kết quả: `reports/simple_results.json`.

| Mô hình | Macro-F1 trung bình | Độ lệch chuẩn | Ghi chú |
| --- | ---: | ---: | --- |
| CNN 1D simple | 0.6881 | 0.0077 | 3-fold CV, train lại ngày 2026-05-24 |
| Random Forest | 0.7845 | 0.0204 | 3-fold CV, feature thủ công |

## Biểu đồ minh hoạ cần đưa vào báo cáo

### 1. So sánh kết quả tổng thể

Hình này dùng để trả lời nhanh câu hỏi: mô hình nào tốt hơn?

![So sánh Macro-F1 giữa CNN 1D và Random Forest](figures/simple_model_comparison.png)

### 2. Độ ổn định qua 3 fold

Hình này cho thấy kết quả không chỉ tốt ở một lần chia dữ liệu.

![Macro-F1 từng fold](figures/simple_fold_macro_f1.png)

### 3. Accuracy của Random Forest

Hình này bổ sung góc nhìn dễ hiểu hơn Macro-F1 cho người nghe không chuyên.

![Random Forest accuracy từng fold](figures/simple_rf_accuracy.png)

## Kết luận đề xuất

Trong báo cáo nên chọn **Random Forest là baseline chính tốt nhất** vì điểm cao hơn và dễ giải thích với người mới. **CNN 1D là mô hình học sâu bổ sung** để chứng minh pipeline có thể học trực tiếp từ chuỗi cảm biến, nhưng không cần đưa các thử nghiệm phức tạp vào phần chính. Các thử nghiệm ResNet/TCN/BiLSTM có thể bỏ hoặc chỉ nhắc rất ngắn ở phụ lục nếu cần.

Lệnh chạy lại:

```bash
source venv/bin/activate
python -m scripts.run_simple_pipeline --config experiments/configs/SIMPLE_CNN.yaml
```
