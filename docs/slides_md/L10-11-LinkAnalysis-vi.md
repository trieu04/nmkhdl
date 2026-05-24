# L10-11-LinkAnalysis-vi


## Slide 1

## Slide 2
- Nhập môn Khoa học dữ liệu (IT4142)

## Slide 3
- Nội dung môn học
- Lecture 1: Tổng quan về Khoa học dữ liệu
- Lecture 2: Thu thập và tiền xử lý dữ liệu
- Lecture 3: Làm sạch và tích hợp dữ liệu
- Lecture 4: Phân tích và khám phá dữ liệu
- Lecture 5: Trực quan hoá dữ liệu
- Lecture 6: Trực quan hoá dữ liệu đa biến
- Lecture 7: Học máy
- Lecture 8: Phân tích dữ liệu lớn
- Lecture 9: Báo cáo tiến độ bài tập lớn và hướng dẫn
- Lecture 10+11: Phân tích một số kiểu dữ liệu
- Lecture 12: Đánh giá kết quả phân tích

## Slide 4
- Các bài toán chính trong phân tích liên kết
- Xếp hạng đồ thị: Phân tích vai trò của các đỉnh trong đồ thị
- Nhận diện cộng đồng: Phát hiện các cộng đồng bao gồm các thành viên có tính chất tương tự
- Dự đoán liên kết: Dự đoán sự tiến hóa của đồ thị theo thời gian
- Phân loại đồ thị: Phân loại các đỉnh và các cạnh của đồ thị vào các lớp cho trước

## Slide 5
- Nội dung
- 1. Xếp hạng đồ thị
- 2. Nhận diện cộng đồng
- 3. Học biểu diễn đồ thị

## Slide 6
- 1. Xếp hạng đồ thị	1.1 Các khái niệm cơ bản của đồ thị
- `
- a) Đồ thị vô hướng
- b) Đồ thị có hướng

## Slide 7
- Ma trận kề
- a[i, j]    =  1 nếu tồn tại cạnh (i,j)
- =  0 nếu ngược lại
- =  2 nếu tồn tại cạnh từ một đỉnh đến chính nó
- `

## Slide 8
- Bậc của đỉnh
- di(i) = số nút trỏ tới i
- do(i) = số nút i trỏ tới

## Slide 9
- 1.2 Thuật toán Dijkstra
- Tìm đường đi ngắn nhất từ một đỉnh s tới các đỉnh còn lại của đồ thị
- d(v): Khoảng cách từ đỉnh v tới đỉnh s
- B1: Khởi tạo d(s) = 0; d(v) = oo
- B2: Sắp xếp các đỉnh v theo một trật tự xác định trên hàng đợi Q
- B3: Lấy một đỉnh u thuộc hàng đợi Q và cập nhật khoảng cách d(v) (nếu cần) với mỗi đỉnh v liền kề với u
- Quay lại B2 cho đến khi xử lý hết các đỉnh

## Slide 10
- VD

## Slide 11
- VD (tiếp)
- `

## Slide 12
- VD (tiếp)

## Slide 13
- VD (tiếp)

## Slide 14
- VD (tiếp)

## Slide 15
- VD (tiếp)

## Slide 16
- VD (tiếp)

## Slide 17
- VD (tiếp)

## Slide 18
- VD (tiếp)

## Slide 19
- VD (tiếp)

## Slide 20
- VD (tiếp)

## Slide 21
- VD (tiếp)

## Slide 22
- d(i, j): Khoảng cách ngắn nhất từ nút i tới nút j
- 1.3 Độ trung tâm	Độ trung tâm lân cận

## Slide 23
- Độ trung tâm trung gian
- pjk(i): Số lượng đường đi ngắn nhất từ j tới k mà đi qua i
- CB(1) = 15, CB(2) = CB(3) = CB(4) = CB(5) = CB(6) = CB(7) = 0

## Slide 24
- 1.4 Độ quan trọng	Độ quan trọng theo bậc
- di(i): Số nút trỏ tới i

## Slide 25
- Độ quan trọng lân cận
- Ii: Các nút có thể đi tới i

## Slide 26
- 1.5 Thuật toán Pagerank
- Xếp hạng đồ thị dựa trên cấu trúc tổng quát
- Đối với các đồ thị lớn, thứ hạng được tính xấp xỉ bằng thuật toán lặp dựa trên ‘random walk’
- Có ứng dụng quan trọng trong máy tìm kiếm web
- Nhược điểm: Không phụ thuộc vào câu truy vấn

## Slide 27
- Ma trận chuyển tiếp
- `

## Slide 28
- `
- Chuẩn hóa:
- Ma trận chuyển tiếp (tiếp)

## Slide 29
- Công thức xếp hạng
- R(A) = (1 – d)  / N + d * ΣB:(B,A) ∈ E R(B) / do(B)
- R(A): Thứ hạng của đỉnh A
- d: damping factor
- N: số đỉnh của đồ thị
- (B,A) cạnh của đồ thị
- do(B) bậc ra của đỉnh B

## Slide 30
- VD (d = 1)

## Slide 31
- VD (d = 0.85)

## Slide 32
- Thuật toán lặp
- Algorithm PageRank(d, E)
- 1.	Khởi tạo thứ hạng các trang R(0);
- 2.	i = 1;
- 3.	repeat
- 4.		for mỗi trang A do
- 5.			R(i)(A) = (1 – d)  / N + d * ΣB:(B,A) ∈ E R(i-1)(B) / do(B);
- 6.		endfor
- 7.		i++;
- 8.	until hội tụ

## Slide 33
- Tốc độ hội tụ

## Slide 34
- Ứng dụng: Tìm kiếm Web

## Slide 35
- Guan et al. 2008. “Bringing Page-Rank to the  Citation Analysis”
- Ứng dụng: Phân tích trích dẫn

## Slide 36
- Ứng dụng: Phân tích trích dẫn (tiếp)

## Slide 37
|  | Spam filtering | Query relevance | Execution |
| HIST |  |  | Online |
| PageRank |  |  | Offline |
- Hypertext Induced Topic Search
- J. Kleinberg. “Authoritative Sources in a Hyperlinked Environment.” In Proc. of the 9th ACM SIAM Symposium on Discrete Algorithms (SODA’98), pp. 668–677, 1998.
- 1.6 Thuật toán HITS

## Slide 38
- Authority/Hub
- Authority: Trang được trỏ tới nhiều
- Hub: Trang trỏ tới nhiều trang khác
- Authority và hub có mối quan hệ tương hỗ

## Slide 39
- Bigraph
- - Các nút chia thành hai tập không giao nhau
- - Mỗi cạnh đều nối hai nút thuộc hai tập

## Slide 40
- Thuật toán
- Đầu vào: Câu truy vấn q
- Đầu ra: Điểm authority và hub của các trang liên quan đến q
- Thuật toán:
- 1 - Truy hồi thông tin
- 2 - Mở rộng đồ thị
- 3 - Tính ranking

## Slide 41
- 1-Truy hồi thông tin
- Y/c một máy tìm kiếm có chứa các văn bản liên quan đến câu truy vấn q (vd Google, Coccoc)
- Đưa q vào máy tìm kiếm và lấy về tập root W gồm k trang liên quan nhất đến q (vd k = 200)

## Slide 42
- 2- Mở rộng đồ thị
- Từ tập root W, mở rộng ra tập base S
- Với mỗi trang p trong W
- Bổ sung các trang mà p trỏ tới
- Bổ sung các trang trỏ tới p

## Slide 43
- 3- Tính thứ hạng
- Authority score (a)
- Hub score (h)
- G = (V,E)

## Slide 44
- 3- Tính thứ hạng (tiếp)
- `

## Slide 45
- Thank you for​ your attentions!​