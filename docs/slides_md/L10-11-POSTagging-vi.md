# L10-11-POSTagging-vi


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
- Gán nhãn từ loại
- PennTreebank
- Hidden Markov model
- Đánh giá

## Slide 5
- Gán nhãn từ loại	PennTreebank
- Tạo ra bởi University of Pennsylvania
- Dự án 8 năm: 1989 – 1996
- 7 triệu từ
- Tập nhãn dựa trên bộ dữ liệu Brown

## Slide 6
- Gán nhãn từ loại	PennTreebank

## Slide 7
- Gán nhãn từ loại	PennTreebank
- CC
- He bought a car and a house.
- CD
- Five years later, autocar will be popular.
- DT
- Pierre Vinken will join the board.
- EX
- There is no asbestos in our product now.

## Slide 8
- Gán nhãn từ loại	PennTreebank
- IN
- Mr Vinken is chairman of Elsevier N.V.
- JJ
- Rudolph	Agnew was named an executive director.
- JJR
- The number of death was higher than expected

## Slide 9
- Gán nhãn từ loại	PennTreebank
- JJS
- The percentage of lung cancer appears to be highest.
- MD
- US should regulate the class of asbestos.
- NN
- It’s more than three times the expected number.
- NNS
- Portfolio managers expect further declines in interest rates.

## Slide 10
- Gán nhãn từ loại	PennTreebank
- NNP
- Alexis Sanchez joined Manchester United yesterday.
- NNPS
- … the Japan Automobile Dealers’ Association...
- POS
- … at Monday’s auction

## Slide 11
- Gán nhãn từ loại	PennTreebank
- PRP
- It expects to obtain regulatory approval.
- PP$
- Shareholders approve its acquisition by Royal Trustco Ltd.
- RB
- … depends heavily on creativity
- RBR
- … worked for the project for more than six years

## Slide 12
- Gán nhãn từ loại	PennTreebank
- RBS
- the most mundane aspect of its workers
- TO
- He decided to stay

## Slide 13
- Gán nhãn từ loại	PennTreebank
- VB
- … to return home
- VBD
- the executives joined Mayor William
- VBG
- … before boarding the buses again
- VBN
- A buffet breakfast was held in the museum

## Slide 14
- Gán nhãn từ loại	PennTreebank
- VBP
- Plans that give advertisers disscount
- VBZ
- The plan is not an attempt
- WDT
- a project that did not include Seymor
- WP
- who couldn’t be reach for comment

## Slide 15
- Gán nhãn từ loại	PennTreebank
- WRB
- where employees are assigned lunch partners

## Slide 16
- corenlp.run

## Slide 17
- http://45.117.171.213/bknlptool/

## Slide 18
- Gán nhãn từ loại	Hidden Markov Models
- DT
- NN
- VBD
- IN
- DT
- NN
- The
- cat
- sat
- on
- the
- mat

## Slide 19
- Gán nhãn từ loại	Hidden Markov Models
- Xác suất chuyển đổi
- Pr(xt = NN | xt-1 = DT)
- Xác suất sinh quan sát
- Pr(ot = cat | xt = NN)

## Slide 20
- Gán nhãn từ loại	Hidden Markov Models
- Học tham số theo tiêu chí MLE
- argmaxtheta	Pr(O, X | theta)
- Thuật toán Baum–Welch
- Giải mã:
- argmaxX		Pr(X | theta, O)
- Thuật toán Viterbi

## Slide 21
- Gán nhãn từ loại	Thuật toán Baum-Welch
- Bước E
- Pha tiến
- Pha lùi
- `

## Slide 22
- Gán nhãn từ loại	Thuật toán Baum-Welch
- Bước M

## Slide 23
- Gán nhãn từ loại	Giải mã Viterbi

## Slide 24
- Gán nhãn từ loại	Giải mã Viterbi
- The
- cat
- sat
- on
- the
- mat
- DT
- IN
- NN
- <S>
- <E>
- ...
- argmaxX P(X | O, theta)
- VBD
- DT
- IN
- NN
- ...
- VBD
- DT
- IN
- NN
- ...
- VBD
- DT
- IN
- NN
- ...
- VBD
- DT
- IN
- NN
- ...
- VBD
- DT
- IN
- NN
- ...
- VBD

## Slide 25
- Gán nhãn từ loại	Giải mã Viterbi
- The
- cat
- sat
- on
- the
- mat
- DT
- IN
- NN
- <S>
- <E>
- ...
- argmaxX P(X | O, theta)
- VBD
- DT
- IN
- NN
- ...
- VBD
- DT
- IN
- NN
- ...
- VBD
- DT
- IN
- NN
- ...
- VBD
- DT
- IN
- NN
- ...
- VBD
- DT
- IN
- NN
- ...
- VBD

## Slide 26
- Gán nhãn từ loại	Ước lượng tham số
- Xác suất chuyển đổi
- Pr(xt=NN|xt-1=DT)
- Xác suất sinh quan sát
- Pr(ot=cat|xt=NN)
- Ước lượng tham số
- Pr(xt=NN|xt-1=DT)=(count(DT,NN)+1)/(count(DT)+L)
- Pr(ot=cat|xt=NN)=(count(cat,NN)+1)/(count(NN)+V)

## Slide 27
- So sánh dự đoán của mô hình với gán nhãn chuẩn
- Các tập dữ liệu:
- Train: Huấn luyện mô hình
- Dev: Lựa chọn siêu tham số
- Test: Đánh giá mô hình
- Gán nhãn từ loại	Đánh giá

## Slide 28
- Precision
- Recall
- F1 = 2PR / (P+R)
- Gán nhãn từ loại	Đánh giá

## Slide 29
- Thank you for​ your attentions!​