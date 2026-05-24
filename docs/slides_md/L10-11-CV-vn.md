# L10-11-CV-vn


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
- Nội dung
- Thị giác máy tính và một số ứng dụng
- Khái niệm cơ bản về ảnh số
- Ảnh số, lược đồ xám, độ sáng độ tương phản, màu,…
- Thư viện : Opencv
- Nhân chập và một số bộ lọc cơ bản
- lọc nhiễu
- phát hiện biên
- Biểu diễn nội dung ảnh / trích chọn đặc trưng: đặc trưng cục bộ và đặc trưng toàn cục

## Slide 5
- Thị giác máy tính ?
- Xử lý ảnh
- Làm việc trên ảnh như một ma trận số
- Đầu vào: ảnh số   đầu ra: ảnh số (ma trận)
- Hỗ trợ kiểm tra và sửa đổi ảnh
- Thị giác máy tính
- Làm máy tính hiểu nội dung ảnh số và video số
- Ảnh và video coi như dữ liệu đầu vào
- Đầu ra: thông tin ngữ nghĩa, thông tin 3D
- What kind of scene?
- Where are the cars?
- How far is the building?
- …

## Slide 6
- Ứng dụng của thị giác máy tính
- Ảnh, video:
- Nguồn dữ liệu dồi dào, môi trường đa dạng
- Giàu thông tin
- Lĩnh vực thu hút nhiều quan tâm đặc biệt trong kỷ nguyên mới ..

## Slide 7
- Ứng dụng của thị giác máy tính
- Hiểu nội dung ảnh

## Slide 8
- Ứng dụng của thị giác máy tính
- Hiểu nội dung bức ảnh
- Facebook's suggestion

## Slide 9
- Ứng dụng của thị giác máy tính
- Earth View, Google earth (mô hình 3D từ nhiều ảnh 2D): mô hình được sinh tự động + các công trình tiêu biểu cần chi tiết: mô hình được thiết kế thủ công (Golden Gate bridge or Sydney Opera house)
- Microsoft's Virtual Earth

## Slide 10
- Ứng dụng của thị giác máy tính
- OCR (Optical character recognition)
- Technology to convert scanned docs to text: each scanner came with an OCR software
- Licence plate detection
- and character recognition
- Digit recognition, AT&T labs
- http://yann.lecun.com/exdb/lenet/

## Slide 11
- Ứng dụng của thị giác máy tính
- Phát hiện mặt người: được tích hợp trong hầu hết các camera để focus tự động, cho phép có các bức ảnh đẹp
- Source: Derek Hoiem, Computer vision, CS 543 / ECE 549, University of Illinois

## Slide 12
- Ứng dụng của thị giác máy tính
- Phát hiện mặt cười: smart camera
- Camera có thể tự động chọn thời điểm chụp để có bức ảnh có biểu cảm hoàn hảo
- Source: Derek Hoiem, Computer vision, CS 543 / ECE 549, University of Illinois

## Slide 13
- Ứng dụng của thị giác máy tính
- Đăng nhập với thông tin sinh trắc học (vân tay, mống mắt, mặt,…
- Source: Derek Hoiem, Computer vision, CS 543 / ECE 549, University of Illinois
- Nhận dạng mặt được xuất hiện rộng rãi hơnhttp://www.sensiblevision.com/
- Bộ quét vân tay được trang bị trên nhiều máy tính cũng như cac thiết bị khác

## Slide 14
- Ứng dụng của thị giác máy tính
- Phát hiện đối tượng (trên mobiles)
- Source: Derek Hoiem, Computer vision, CS 543 / ECE 549, University of Illinois
- Point & Find, Nokia
- Google Goggles

## Slide 15
- Ứng dụng của thị giác máy tính
- Truy vấn ảnh dựa trên nội dung

## Slide 16
- Ứng dụng của thị giác máy tính
- Smart cars  autonomous vehicles
- Source: Derek Hoiem, Computer vision, CS 543 / ECE 549, University of Illinois
- Mobileye: vision systems currently in many cars
- “In mid 2010 Mobileye will launch a world's first application of full emergency braking for collision mitigation for pedestrians where vision is the key technology for detecting pedestrians

## Slide 17
- Ứng dụng của thị giác máy tính
- Ghép ảnh toàn cảnh:
- Source:http://miseaupoint.org/blog/en/wp-content/uploads/2014/01/photo_stitching.jpg

## Slide 18
- Ứng dụng của thị giác máy tính
- Games / robots:
- http://www.robocup.org/
- Robot vacuum cleaner
- Vision-based interaction game
- (Microsoft's Kinect)

## Slide 19
- Ứng dụng của thị giác máy tính
- Tìm hiểu thêm về các ứng dụng và công ty trong lĩnh vực thị giác máy tính, tham khảo trang của D.Lowe:
- https://www.cs.ubc.ca/~lowe/vision.html

## Slide 20
- Một số topics trong CV
- Camera giám sát:
- Đếm số lượng khách hàng trong cửa hàng
- Phát hiện hành động bất thường
- Đo mức độ hải long của khách hàng
- Object tracking: Someone ran a red light?
- Phát hiện và nhận dạng đối tượng
- Phát hiện mặt/mắt/người
- Nhận dạng hoạt động
- Phát hiện lỗi
- Gán nhãn ảnh số
- Phát hiện nhận dạng ký tự
- Đọc card visite, CMT, biển số, …
- Xây dựng đối tượng 3D từ ảnh 2D

## Slide 21
- Nội dung chính sẽ đề cập
- 2 kiểu thông tin chúng ta trích chọn từ ảnh:
- Thông tin 3D
- Thông tin ngữ nghĩa
- 3D building?
- Where is it?
- Text in the picture,
- what does it means?
- Are there person
- in the picture?
- How to represent
- the content of images ?
- Pre-processing
- Feature extraction
- Learning
- Deep Learning
- Model

## Slide 22
- Ảnh số ?
- Con người nhìn thấy gì trong ảnh?
- Một chiếc oto?
- Máy tính có thể thấy gì?
- Ảnh là một ma trận các điểm ảnh
- Ảnh N x M : ma trận N xM
- 1 điểm ảnh (gray levels):
- Giá trị cường độ sáng
- 0-255
- Đen: 0
- Trắng: 255

## Slide 23
- Ảnh số ?
- Ảnh I:
- Chỉ số (0,0): góc trái trên
- I(x,y): cường độ sáng ở vị trí  (x,y)

## Slide 24
- Ảnh số ?
- Loại ảnh chính
- Ảnh nhị phân:
- I(x,y)  {0 , 1}
- 1 pixel: 1 bit
- Ảnh đa mức xám:
- I(x,y)  [0..255]
- 1 pixel: 8 bits (1 byte)
- Ảnh màu:
- IR(x,y), IG(x,y)  IB(x,y)  [0..255]
- 1 pixel: 24 bits (3 bytes )
- Khác : ảnh đa phổ, ảnh độ sâu,…

## Slide 25
- Ảnh màu trong không gian màu RGN
- Không gian màu khác:
- Lab, HSV, …

## Slide 26
- Lược đồ xám của ảnh (Image histogram)
- Là biểu diễn đồ thị sự phân bố màu sắc của các điểm ảnh trên ảnh số

## Slide 27
- Lược đồ xám của ảnh (Image histogram)
- Histogram
- Phải chuẩn hóa bằng cách chia cho tổng số điểm ảnh trên ảnh

## Slide 28
- Lược đồ xám của ảnh (Image histogram)
- Histogram
- Chỉ thông tin thống kê
- Không có thông tin về mặt không gian của các điểm ảnh
- Ảnh khác nhau có thể có histogram giống nhau

## Slide 29
- Độ sáng (Brightness)
- Là giá trị trung bình cường độ sáng trung bình của tất cả các điểm ảnh trên ảnh: độ sáng/tối của ảnh

## Slide 30
- Độ tương phản (Contrast)
- Độ tương phản của ảnh số thể hiện mức độ dễ dàng phân biệt của đối tượng trong ảnh
- Một số cách tính:
- Độ lệch chuẩn các giá trị điểm ảnh
- Khác biệt giữa giá trị lớn nhất và nhỏ nhất của điểm ảnh trên ảnh

## Slide 31
- Độ tương phản (Contrast)
- Contrast vs histogram

## Slide 32
- Ví dụ

## Slide 33
- Tăng cường độ tương phản
- Thay đổi giá trị điểm ảnh để có độ tương phản cao hơn
- Một số phương pháp:
- Kéo giãn dải động ảnh (Linear stretching of intensity range):
- Linear transform
- Linear transform with saturation
- Piecewise linear transform
- Biến đổi phi tuyến. VD: Gama correction
- Cân bằng histogram

## Slide 34
- Linear stretching
- Linear transform

## Slide 35
- Linear stretching
- No efficace?

## Slide 36
- Cân bằng histogram
- Histogram của ảnh sau thay đổi hướng tới phân phối đều
- Không tham số. OpenCV:cv2.equalizeHist(img)

## Slide 37
- Cân bằng histogram

## Slide 38
- Cân bằng histogram

## Slide 39
- Histogram trên ảnh màu
- Lược đồ xám:
- Chuyển ảnh màu sang ảnh xám
- => Tính hist của ảnh xám
- Histogram của các kênh màu riêng:
- 3 histograms cho (R,G,B)
- Histogram 3D:
- Một màu đc xđ bởi 3 giá trị
- Không thường được dung do kích thước lớn
- Source: https://web.cs.wpi.edu/~emmanuel

## Slide 40
- HSV (Hue – Saturation- Value)
- HSV: không gian màu tốt thường được sử dụng trong bài toán phân vùng hay nhận dạng
- Biến đổi phi tuyến từ RGB
- Biểu diễn trực quan màu sắc
- Mỗi pixel có:
- Cường độ sáng:intensity  (value)
- Màu sắc color  (hue + saturation)
- RGB không có sự phân tách như thế này

## Slide 41
- HSV (Hue – Saturation- Value)
- Hue (H) được mã hóa như 1 góc thay đổi giữa 0 và 360
- Saturation (S) được mã hóa như độ dài của bán kính, giá trị từ 0 đến 1
- S = 0  : xám
- S = 1  : màu tinh khiết
- Value (V)  = MAX (Red, Green,  Blue)

## Slide 42
- HSV (Hue – Saturation- Value)
- Nếu biết màu của đối tượng tìm kiếm  có thể biểu diễn sử dụng 1 khoảng giá trị H (Hue)
- Lưu ý: H có chu kỳ
- Hue < 60°  không có nghĩa
- 350° nhỏ hay lớn hơn 60°?
- Cần xác định H trong 1 khoảng giá trị. VD: 350° < H < 60°
- Khoảng giá trị H có ý nghĩa nếu Saturation > threshold   (nếu không là màu xám)
- H, S độc lập với Value, Value nhạy cảm hơn với điều kiện chiếu sáng

## Slide 43
- Không gian màu Lab
- Lab (thi thoảng gọi L*a*b*)  dựa trên một nghiên cứu về thị giác người
- Độc lập với tất cả các công nghệ
- Thể hiện màu sắc như mắt người nhìn thấy
- Màu được xác định bởi 3 giá trị
- L (luminance) – độ sáng: từ 0% (black) đến 100% (white)
- a* biểu diễn trục màu từ màu xanh lá (negative value, -127) tới màu đỏ (positive value, +127)
- b* biểu diễn trục màu từ xanh dương (negative value, -127) tới vàng (positive value,+127)

## Slide 44
- Không gian màu Lab

## Slide 45
- Không gian màu vs. Điều kiện chiếu sáng
- Thu thập 10 ảnh của khối lập phương trong điều kiện chiếu sáng khác nhau
- Cắt riêng từng màu để có 6 bộ cho 6 màu khác nhau
- Tính toán phân bố giá trị của màu sắc cụ thể trong các không gian màu khác nhau
- Changes in color due to varying Illumination conditions
- Source: Vikas Gupta, Learn OpenCV

## Slide 46
- Không gian màu vs. Điều kiện chiếu sáng
- Điều kiện chiếu sáng giống nhau: giá trị tập trung
- Fig.: Density Plot showing the variation of values in color channels for 2 similar bright images of blue color
- Source: Vikas Gupta, Learn OpenCV

## Slide 47
- Không gian màu vs. Điều kiện chiếu sáng
- Điều kiện chiếu sáng giống nhau: giá trị tập trung
- Fig.: Density Plot showing the variation of values in color channels for 2 similar bright images of yellow color
- Source: Vikas Gupta, Learn OpenCV

## Slide 48
- Không gian màu vs. Điều kiện chiếu sáng
- Điều kiện chiếu sáng khác nhau:
- Fig.:  Density Plot showing the variation of values in color channels under varying illumination for the blue color
- Source: Vikas Gupta, Learn OpenCV

## Slide 49
- Không gian màu vs. Điều kiện chiếu sáng
- Điều kiện chiếu sáng khác nhau:
- Fig.:  Density Plot showing the variation of values in color channels under varying illumination for the yellow color
- Source: Vikas Gupta, Learn OpenCV

## Slide 50
- Không gian màu vs. Điều kiện chiếu sáng
- Điều kiện chiếu sáng khác nhau:
- RGB : sự biến động giá trị ở các kênh lớn
- HSV: giá trị tập trung ở kênh H. Chỉ có kênh H chứa thông tin tuyệt đối về màu  1 lựa chọn
- YCrCb, LAB: giá trị tập trung ở kênh CrCb và kênh AB
- Giá trị tập trung tốt hơn ở không gian LAB
- Chuyển đổi giữa các không gian màu (OpenCV):
- cvtColor(bgr, ycb, COLOR_BGR2YCrCb);
- cvtColor(bgr, hsv, COLOR_BGR2HSV);
- cvtColor(bgr, lab, COLOR_BGR2Lab);

## Slide 51
- Nhân chập (Convolution)
- Lọc ảnh :  Với mỗi điểm ảnh, tính giá trị mới của điểm ảnh dựa trên 1 hàm theo các điểm trong lân cận của nó
- Cùng hàm được áp trên mỗi điểm ảnh
- Ảnh đầu vào và ra thường có cùng kích thước
- Nhân chập :  phép lọc tuyến tính, hàm số là tổng có trọng số của các điểm ảnh trong lân cận của điểm ảnh xét.
- I' = I * K
- Có vai trò quan trọng!
- Tăng cường ảnh: giảm nhiễu, làm trơn, tăng độ tương phản, …
- Trích chọn thông tin từ ảnh:
- Texture, edges, distinctive points, etc.
- Phát hiện mẫu
- Template matching

## Slide 52
- Nhân chập (Convolution)
- Original image
- Filtered image
- Mask (kernel)

## Slide 53
- Nhân chập (Convolution)
- K: convolution kernel, mask, filter, …

## Slide 54
- Nhân chập (Convolution)
- Source: http://machinelearninguru.com

## Slide 55
- Nhân chập (Convolution)
- I' = I * K

## Slide 56
- Nhân chập (Convolution)
- I' = I * K

## Slide 57
- Nhân chập (Convolution)
- I' = I * K

## Slide 58
- Nhân chập (Convolution)
- Vấn đề ở cạnh ảnh?
- Thêm dòng/cột 0 vào ma trận đầu vào
- Đối xứng gương:
- f(-x,y) = f(x,y)
- f(-x,-y) = f(x,y)
- …

## Slide 59
- Nhân chập (Convolution)
- Source: http://machinelearninguru.com

## Slide 60
- Một số bộ lọc (Some kernels)
- Nhân chập 2D
- Chủ yếu được sử dụng để trích chọn đặc trưng trên ảnh
- Được sử dụng như phép toán trong khối cơ sở của mạng Neuron tích chập: Convolutional Neural Networks (CNNs)
- Mỗi bộ lọc có hiệu ứng riêng và hữu ích cho các nhiệm vụ cụ thể như:
- Làm mờ (lọc nhiễu),
- Làm nét biên,
- Phát hiện cạnh,
- …..

## Slide 61
- Một số bộ lọc (Some kernels)
| 0 | 0 | 0 |
| 0 | 1 | 0 |
| 0 | 0 | 0 |
- *
| 0 | 0 | 0 |
| 1 | 0 | 0 |
| 0 | 0 | 0 |
- *
- Original image
- Original image
- Filtered image
- (no change)
- Filtered image
- (shifted left by 1 pixel)
- Source: David Lowe

## Slide 62
- Một số bộ lọc (Some kernels)
- Lọc trung bình (mean filter):
- Thay giá trị bởi giá trị trung bình của các hang xóm
- Ảnh được làm trơn
- Original image
- Filtered image
- with box size 5x5
- Filtered image
- with box size 11x11

## Slide 63
- Một số bộ lọc (Some kernels)
- Gaussian filter
| 0.003 | 0.013 | 0.022 | 0.013 | 0.003 |
| 0.013 | 0.059 | 0.097 | 0.059 | 0.013 |
| 0.022 | 0.097 | 0.159 | 0.097 | 0.022 |
| 0.013 | 0.059 | 0.097 | 0.059 | 0.013 |
| 0.003 | 0.013 | 0.022 | 0.013 | 0.003 |
- Gaussian function in 3D
- Gaussian image
- Gaussian filter with size 5 x5 , sigma =1
- Rule for Gaussian filter:
- set filter half-width to about 3σ

## Slide 64
- Một số bộ lọc (Some kernels)

## Slide 65
- Một số bộ lọc (Some kernels)
- Bộ lọc Gauss
- Original image
- Filtered image
- with box size 5x5
- Filtered image
- with box size 11x11

## Slide 66
- Một số bộ lọc (Some kernels)
- Sobel
- *
- Vertical Edge
- (absolute value)

## Slide 67
- Một số bộ lọc (Some kernels)
- Sobel
- *
- Horizontal Edge
- (absolute value)

## Slide 68
- Phát hiện biên
- Vị trí biên:
- Đạt cực trị trên đạo hàm bậc 1
- Đổi dấu qua không trên đạo hàm bậc 2

## Slide 69
- Phát hiện biên với đạo hàm bậc 1
- Tính kết quả nhân chập giữa ảnh vào bộ lọc để tính đạo hàm bậc 1
- Bộ lọc để tính đạo hàm bậc 1: Sobel, Prewitt, Robert
- Các bộ này này đều được cài đặt OpenCV library
- Tìm cực trị địa phương
- Biên bao gồm các điểm ảnh có giá trị cực đại/cực tiểu trên đạo hàm bậc 1 của ảnh.
- Có thể dung ngưỡng để phát hiện nhanh các cạnh
- Có thể gồm nhiều bước để tìm được cạnh tối ưu: Canny detector (cài đặt trong OpenCV)

## Slide 70
- Phát hiện biên với đạo hàm bậc 1
- Bộ lọc  dùng tính đạo hàm bậc 1 trên ảnh
- Robert
- Prewitt
- Ít nhạy cảm với nhiễu
- Làm trơn với bộ lọc trung bình + tính đạo hàm bậc 1
- Sobel:
- Ít nhảy cảm với nhiễu
- Làm trơn với Gauss + tính đạo hàm
- y
- x

## Slide 71
- Phát hiện biên với đạo hàm bậc 1

## Slide 72
- Đạo hàm (Image gradient)
- 1st derivatives :
- I *
- Đạo hàm bậc 1 theo x
- Ix
- I *
- Đạo hàm bậc 1 theo y
- Iy
- Image  gradient

## Slide 73
- Đạo hàm (Image gradient)
- Đường màu xanh thể hiện hướng của đạo hàm: từ sáng nhất đến tối nhất

## Slide 74
- Phát hiện biên với đạo hàm bậc 2
- Tính đạo hàm bậc 2
- Nhân chập ảnh với bộ lọc Laplace
- Tìm điểm đổi dấu qua không

## Slide 75
- Đạo hàm bậc 2
- Một mặt nạ xấp xỉ cho hàm Laplace

## Slide 76
- Trích chọn đặc trưng
- Hai loại đặc trưng được trích chọn từ ảnh:
- Đặc trưng cục bộ và toàn cục
- Đặc trưng toàn cục:
- Mô tả toàn bộ ảnh như 1 đối tượng
- Đặc trưng đường biên, đặc trưng hình dạng, đặc trưng kết cấu
- Ví dụ: Invariant Moments (Hu, Zernike), Histogram Oriented Gradients (HOG), PHOG, and Co-HOG,...
- Đặc trưng cục bộ:
- Mô tả đặc trưng cục bộ mô tả từng vùng nhỏ trong ảnh, từng vùng cục bộ của đối tượng (điểm đặc trưng trong ảnh).
- Biển diễn đặc trưng kết cấu/màu sắc trong mỗi vùng cục bộ ảnh
- Ví dụ: SIFT, SURF, LBP, BRISK, MSER và FREAK, …

## Slide 77
- Trích chọn đặc trưng
- Đặc trưng toàn cục
- Source:http://www.robots.ox.ac.uk/~vgg/research/caltech/phog.html
- 256 bins intensity histogram
- 16 bins intensity histogram
- Pyramid Histogram of Oriented Gradients

## Slide 78
- Feature extraction
- Global features : ? PCA (chưa được giới thiệu ở phần ML) hoặc tìm 1 đặc trung khác đã có trong OpenCV để sv dễ theo dõi

## Slide 79
- Trích chọn đặc trưng
- Đặc trưng cục bộ: xác định vùng cục bộ như thế nào?
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
- Image segmentation
- Keypoint detection
- Không cần biết nội dung của ảnh
- Dựa trên nội dung của ảnh
- Dividing into patches with  regular grid

## Slide 80
- Trích chọn đặc trưng
- Phân vùng ảnh
- Lấy ngưỡng (Thresholding)
- Chia và hợp (Split and merge)
- Phát triển vùng (Region growing)
- Watershed
- …

## Slide 81
- Trích chọn đặc trưng
- Phát hiện các điểm đặc trưng:
- DoG /SIFT detector
- Harris corner detector
- Moravec
- …
- Đặc trưng cục bộ: tính trên các vùng cục bộ xung quan điểm đặc trưng:
- SIFT,
- SURF(Speeded Up Robust Features),
- PCA-SIFT
- LBP, BRISK, MSER and FREAK, …

## Slide 82
- VD: Bộ phát hiện điểm đặc trưng DoG/SIFT
- Source: Distinctive Image Features from Scale-Invariant Keypoints – IJCV 2004
- A SIFT keypoint : {x, y, scale, dominant orientation}

## Slide 83
- VD: đặc trưng SIFT
- Source: Distinctive Image Features from Scale-Invariant Keypoints – IJCV 2004
- http://campar.in.tum.de/twiki/pub/Chair/TeachingWs13TDCV/feature_descriptors.pdf
- Compute gradients in
- respect to the keypoint
- orientation(rotation
- invariance)
- Compute orientation
- histogram in 8
- directions over 4x4
- sample regions
- Blur the image
- using the scale of
- the keypoint
- (scale invariance)

## Slide 84
- Trích chọn đặc trưng: Đặc trưng tốt?
- Gọn (Compact)
- Bất biến với
- Một số phép biến đổi hình học
- Góc nhìn camera
- Điều kiện chiếu sáng
- Một trong những đặc trưng tốt nhất: SIFT (David Lowe)

## Slide 85
- Một số bộ đặc trưng cục bộ khác
- Popular features: SURF, HOG, SIFT
- http://campar.in.tum.de/twiki/pub/Chair/TeachingWs13TDCV/feature_descriptors.pdf
- Summary some local features:
- http://www.cse.iitm.ac.in/~vplab/courses/CV_DIP/PDF/Feature_Detectors_and_Descriptors.pdf

## Slide 86
- Trích chọn đặc trưng: OpenCV
- SIFT & SURF:
- Đã đăng ký sở hữu trí tuệ
- Sử dụng tự do cho mục đích nghiên cứu/giảng dạy
- Sử dụng trong các ứng dụng thương mại: cần giấy phép
- Từ OpenCV 3.0, các thuật toán đã ddk sở hữu trí tuệ:
- Được loại bỏ khỏi gói cài đặt chuẩn,
- Được đặt trong gói "non-free" (opencv-contrib, không được cài đặt mặc định)
- Một số các thay thế cho sift, surf:
- ORB (Oriented FAST and Rotated Brief)
- BRIEF, BRISK, FREAK, KAZE and AKAZE

## Slide 87
- Trích chọn đặc trưng: OpenCV
- SIFT
- sift.detect() : tìm các điểm đặc trưng
- sift.compute() : tính đặc trưng cục bộ tại các điểm đặc trưng
- sift = cv.xfeatures2d.SIFT_create()
- kp = sift.detect(gray,None)
- kp,des = sift.compute(gray,kp)
- Tìm điểm đặc trưng và đặc trưng cục bộ: sift.detectAndCompute()
- sift = cv.xfeatures2d.SIFT_create()
- kp, des = sift.detectAndCompute(gray,None)
- https://docs.opencv.org/3.4/da/df5/tutorial_py_sift_intro.html
- SURF: tương tự

## Slide 88
- Trích chọn đặc trưng: OpenCV
- SURF:
- >>> img = cv.imread('fly.png',0)
- # Create SURF object. You can specify params here or later.
- # Here I set Hessian Threshold to 400
- >>> surf = cv.xfeatures2d.SURF_create(400)
- # Find keypoints and descriptors directly
- >>> kp, des = surf.detectAndCompute(img,None)
- >>> len(kp)
- 699
- https://docs.opencv.org/3.4/df/dd2/tutorial_py_surf_intro.html

## Slide 89
- Mô hình túi từ
- Xuất phát từ mô hình biểu diễn văn bản không tính đến thứ tự các từ: chỉ tính đến tần suất xuất hiện của từ trong văn bản  Salton & McGill (1983)

## Slide 90
- Mô hình túi từ (Bags of features) để nhận dạng đối tượng
- Hoạt động tốt cho phân loại ảnh cũng như bài toán nhận dạng các thể hiện của đối tượng
- Csurka et al. (2004), Willamowski et al. (2005), Grauman & Darrell (2005), Sivic et al. (2003, 2005)
- face, flowers, building

## Slide 91
- Mô hình túi từ: các bước chính
- Trích chọn đặc trưng
- Học từ điển trực quan (visual vocabulary)
- Xác định từ tương ứng cho các đặc trưng
- Biểu diễn ảnh bởi tần suất xuất hiện của các từ trực quan (“visual words” )

## Slide 92
- References
- CVIP tool to explore the power of computer processing of digital images: Many methods in image processing and computer vision have been implemented
- https://cviptools.ece.siue.edu/
- Library: OpenCV, with C/C++, Python and Java interfaces. OpenCV was designed for computational efficiency and with a strong focus on real-time application: https://opencv.org/
- Books:
- Rafael C. Gonzalez, Richard Eugene Woods, Digital Image Processing, 2nd edition, Prentice-Hall, 2002: Chap 3 (spatial operators), 6 (Color spaces)
- Richard Szeliski, Computer Vision: Algorithms and Applications, Springer, 2010. http://szeliski.org/Book/
- Articles:
- SIFT (DoG detector and SIFT descriptor): https://www.cs.ubc.ca/~lowe/keypoints/
- SURF: Herbert Bay, Andreas Ess, Tinne Tuytelaars, and Luc Van Gool, "Speeded Up Robust Features", ETH Zurich, Katholieke Universiteit Leuven
- GLOH: Krystian Mikolajczyk and Cordelia Schmid "A performance evaluation of local descriptors", IEEE Transactions on Pattern Analysis and Machine Intelligence, 10, 27, pp 1615--1630, 2005.
- PHOG: http://www.robots.ox.ac.uk/~vgg/research/caltech/phog.html
- https://www.learnopencv.com/ : many examples with code in C++/ Python and clear explanation

## Slide 93
- Exercises
- Feature extraction
- Visualization extracted features from a set of images (check with Mai Anh for visualizing multi-dimension features)
- Simple classification or detection? (global feature: PCA ?)

## Slide 94
- Thank you for​ your attentions!​