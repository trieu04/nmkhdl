# L10-11-NLPIntro-vi


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
- Giới thiệu về XLNNTN
- NLP là gì?
- Các vấn đề chính trong NLP
- Các thách thức của NLP

## Slide 5
- Giới thiệu về XLNNTN	NLP là gì?
- Ngôn ngữ tự nhiên: công cụ để giao tiếp giữa con người với con người, giữa con người với máy tính
- Định dạng: tiếng nói, văn bản, hình ảnh, video
- Thể loại: các ngôn ngữ trên thế giới, các ngôn ngữ lập trình

## Slide 6
- Giới thiệu về XLNNTN	NLP là gì?
- Hiểu, mô hình hóa được ngôn ngữ tự nhiên
- Làm cho máy tính và con người giao tiếp bằng ngôn ngữ tự nhiên
- Làm cho con người sử dụng các ngôn ngữ khác nhau có thể giao tiếp được
- Khai thác thông tin và tri thức được thể hiện qua ngôn ngữ để phục vụ các lĩnh vực của đời sống con người

## Slide 7
- Giới thiệu về XLNNTN	NLP là gì?
- 1950: Turing test

## Slide 8
- Giới thiệu về XLNNTN	NLP là gì?
- NLP liên quan đến:
- Ngôn ngữ học, tâm lý học, triết học
- Trí tuệ nhân tạo, học máy, dữ liệu lớn

## Slide 9
- Giới thiệu về XLNNTN	Các vấn đề chính trong NLP
- INFORMATION EXTRACTION
- NATURAL LANGUAGE UNDERSTANDING
- NATURAL LANGUAGE GENERATION
- DATA + LINGUISTICS + MACHINE LEARNING
- END-TO-END
- APPLICATIONS

## Slide 10
- Giới thiệu về XLNNTN	Các vấn đề chính trong NLP
- Tách từ
- “xử_lý ngôn_ngữ tự_nhiên”
- (process  language  natural)

## Slide 11
- Giới thiệu về XLNNTN	Các vấn đề chính trong NLP
- Gán nhãn từ loại
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

## Slide 12
- Giới thiệu về XLNNTN	Các vấn đề chính trong NLP
- Phân cụm
- [The cat]NP [sat]VP [on]PP [the mat]NP

## Slide 13
- Giới thiệu về XLNNTN	Các vấn đề chính trong NLP
- Phân tích cú pháp
- thành phần
- The cat  sat  on the mat
- DT NN VBD IN DT NN
- NP
- PP
- NP          VP
- S

## Slide 14
- Giới thiệu về XLNNTN	Các vấn đề chính trong NLP
- Phân tích cú pháp phụ thuộc
- The
- cat
- sat
- on
- the
- mat
- det
- det
- case
- nmod:on
- nsubj

## Slide 15
- Giới thiệu về XLNNTN	Các vấn đề chính trong NLP
- The cat  sat  on the mat
- DT NN  VB  IN DT NN
- NP (mat)
- PP (on)
- NP (cat)   VP (sat)
- S (sat)

## Slide 16
- Giới thiệu về XLNNTN	Các vấn đề chính trong NLP
- Alexis Sanchez stepped up his preparations for Manchester United’s FA Cup clash against Yeovil when he checked in for training on Thursday. The Chile star is in line to make his debut for the Red Devils in the fourth round tie at Huish Park following his move to Old Trafford. Sanchez met his new team-mates for the first time on Wednesday and could go straight into the matchday squad to face the Glovers. Jose Mourinho has so far given no indication on the strength of team that he will take to Somerset, but Sanchez will be keen to make his debut.
- Alexis Sanchez checks in for training as he prepares for his Manchester United debut
- doc#1
- doc#2
- Phân giải đồng tham chiếu

## Slide 17
- Giới thiệu về XLNNTN	Các vấn đề chính trong NLP
- Phân tích ngữ nghĩa
- “Mouse love Rice”
- “The history of computer mouse”

## Slide 18
- Giới thiệu về XLNNTN	Các vấn đề chính trong NLP
- Multilingual concept net

## Slide 19
- Giới thiệu về XLNNTN	Các vấn đề chính trong NLP
- Mô hình ngôn ngữ
- `
- From Dan Jurafsky 2018

## Slide 20
- Giới thiệu về XLNNTN	Các vấn đề chính trong NLP
- Nhận diện thực thể có tên
- [GM]ORG sold the company in [Nov 1998]TIME to [LLC]ORG

## Slide 21
- Giới thiệu về XLNNTN	Các vấn đề chính trong NLP
- Trích rút sự kiện
- GM sold the company in Nov 1998 to LLC
- participants
- trigger
- attribute

## Slide 22
- Liên kết thực thể
- Giới thiệu về XLNNTN	Các vấn đề chính trong NLP
- Alexis Sanchez stepped up his preparations for Manchester United’s FA Cup clash against Yeovil when he checked in for training on Thursday. The Chile star is in line to make his debut for the Red Devils in the fourth round tie at Huish Park following his move to Old Trafford. Sanchez met his new team-mates for the first time on Wednesday and could go straight into the matchday squad to face the Glovers. Jose Mourinho has so far given no indication on the strength of team that he will take to Somerset, but Sanchez will be keen to make his debut.

## Slide 23
- Giới thiệu về XLNNTN	Các thách thức chính trong NLP
- Đặc tính cố hữu của ngôn ngữ là nhập nhằng
- Ngôn ngữ đa dạng và liên tục biến đổi
- Ngôn ngữ dưới tư cách đối tượng xử lý của các mô hình học máy thông kê, học sâu

## Slide 24
- Thank you for​ your attentions!​