# L2-web-crawling-vi


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
- Trình thu thập dữ liệu
- Nền tảng Scrapy

## Slide 5
- Giới thiệu

## Slide 6
- Chu trình khai thác dữ liệu
- Data collection (scraping)

## Slide 7
- Thu thập dữ liệu là gì?
- Bước đầu tiên của làm khoa học dữ liệu
- Mục tiêu là lấy về đủ thông tin cần thiết để phân tích trong bước sau
- Có thể bao gồm dữ liệu nội bộ và dữ liệu từ bên ngoài
- INTERNAL DATA (inside the enterprise/organization)

## Slide 8
- Làm thế nào để truy cập tới dữ liệu?
- Tuỳ thuộc vào nguồn dữ liệu
- Nguồn dữ liệu nội bộ:
- CSDL, kho dữ liệu
- Các tệp tin
- Có cấu trúc (Excel, log files..)
- Phi cấu trúc
- Viết bằng ngôn ngữ tự nhiên
- Văn bản
- Các báo cáo
- Nguồn dữ liệu từ bên ngoài:
- API (SOAP or REST): https://youtu.be/bPNfu0IZhoE
- Các tệp tin có thể tải về trên Internet
- Các dữ liệu dưới dạng HTML trên các website

## Slide 9
- Các ví dụ về nguồn dữ liệu mở
- Global Health Facts (www.globalhealthfacts.org/)
- UNdata (http://data.un.org/)
- World Health Organization(www.who.int/research/en/) – Dữ liệu sức khoẻ
- OECD Statistics (http://stats.oecd.org/) – Các chỉ số kinh tế
- World Bank (http://data.worldbank.org/)
- Census Bureau (www.census.gov/) – Dữ liệu nhân khẩu học
- Data.gov (http://data.gov/) – Dữ liệu cung cấp bởi cơ quan chính phủ USA
- Data.gov.uk (http://data.gov.uk/)
- data.gouv.fr (http://data.gouv.fr)
- DataSF (http://datasf.org/) – Dữ liệu của SanFrancisco
- NYC DataMine (http://nyc.gov/data/) – Dữ liệu của New York.
- ParisData (http://opendata.paris.fr) – Dữ liệu của Paris
- OpenData La Rochelle (https://opendata.larochelle.fr/) – Dữ liệu của La Rochelle

## Slide 10
- Truy cập dữ liệu thông qua APIs
- Nhiều cổng dịch vụ cung cấp qua giao thức http
- Định dạng dữ liệu trao đổi, cung cấp được thống nhất, có cấu trúc để dễ dàng bóc tách và xử lý
- Định dạng dữ liệu có thể không dễ dàng để hiểu nếu không rõ mô tả
- Các giao thức thường sử dụng • SOAP: sử dụng XML• REST: sử dụng JSON
- Ví dụ: thông tin về số chô đỗ xe đang trống ở La Rochelle:
- https://opendata.larochelle.fr/dataset/stationnement-parking-tarifs-synthetiques/

## Slide 11
- Truy cập dữ liệu trong các log files (tệp nhật ký)
- Log files chứa chuỗi nhật ký của các sự kiện đã xảy ra
- API, network activity…
- Các mục nhật ký có nhãn thời gian và theo thứ tự thời gian
- Cho phép phân tích các hoạt động và tương tác đã diễn ra trong hệ thống

## Slide 12
- Truy cập dữ liệu trong các log files (tệp nhật ký)
- Định dạng chuẩn hoá phổ biến: syslog
- Date of emission
- Name of the device
- Process that triggered emission
- Priority Level
- Message contents
- Message category
- Seriousness level
- ELK là nền tảng mã nguồn mở phổ biến để xử lý dữ liệu log, cho phép trực quan hoá dễ dàng

## Slide 13
- Các định nghĩa
- Data scraping, screen scraping, report mining, web scraping

## Slide 14
- Thu thập dữ liệu thông qua cào dữ liệu (data scraping)
- Data scraping được sử dụng khi hệ thống có dữ liệu không cung cấp giao diện và API để truy cập dữ liệu
- Data scraping là một kỹ thuật để trích xuất dữ liệu từ nguồn dữ liệu được công khai thành dạng có cấu trúc
- Thường là các trang web
- Cũng có thể là các nguồn thông tin khác được hiển thị trên màn hình hoặc các giao diện khác

## Slide 15
- Một vài giới hạn của data scraping
- Chủ sở hữu của nguồn thông tin không ưa thích data scraping
- Gây quá tải cho hệ thống
- Mất mát doanh thu từ quảng cáo
- Mất kiểm soát tới dữ liệu, vi phạm bản quyền dữ liệu
- Data scraping thường là kỹ thuật được dùng khi không có phương án thay thế

## Slide 16
- Screen mining là gì?
- Trích xuất dữ liệu văn bản từ màn hình hiển thị của thiết bị
- Thường xử dụng kỹ thuật chụp ảnh và OCR
- Trong một vài trường hợp, thường sử dụng kèm với chương trình giả lập thao thác của người dùng để điều khiển UI
- Cho phép tự động chụp lại toàn bộ các màn hình

## Slide 17
- Report mining là gì?
- Bóc tách nội dung từ báo cáo, các văn bản ở ngôn ngữ tự nhiên (PDF, text, vvv)
- Không cần sử dụng API
- Ví dụ: Các công cụ Tabula, import in Tableau

## Slide 18
- Web scraping là gì?
- Trang web là các tệp dữ liệu văn bản được viết theo định dạng markup-based language (HTML and XHTML)
- Tuy nhiên định dạng này phục vụ để hiển thị cho con người, không dành cho xử lý dự động
- Để chống lại kỹ thuật cào web, một vài website sử dụng các cơ chế phòng thủ (Giới hạn số lượt truy cập theo IP, CAPTCHA…)

## Slide 19
- Trình thu thập Web (Web crawler)

## Slide 20
- Web crawler
- Là chương trình phần mềm, được gọi là con nhện, một robot, đi theo các links trên các websites, thu thập các thông tin và lưu vào CSDL
- Các tên gọi
- Crawler
- Spider
- Robot
- Web agent

## Slide 21
- Basic crawling operation
- Begin with known “seed” URLs
- Fetch and parse them
- Extract URLs they point to
- Place the extracted URLs on a queue
- Fetch each URL on the frontier (queue) and repeat

## Slide 22
- Chính sách cào dữ liệu
- Hành vi của một Web crawler là kết quả của sự kết hợp các chính sách sau
- Selection policy: Tải về trang nào
- Re-visit policy: Khi nào cần kiểm tra lại có hay không sự thay đổi ở các trang web
- Politeness policy: Chính sách tránh làm quá tải máy chủ
- Parallelization policy: Chính sách phối hợp giữa các web crawler phân tán

## Slide 23
- Thách thức đối với cào web
- Internet là rất rộng lớn, bao la
- Googlebot là trình cào web phân tán
- Lọc, phân biệt các trang quan tâm/ không quan tâm/ trang độc hại (đối với bot)
- Spam pages
- Spider traps – trang được sinh ra tự động dễ dụ bot
- Tính mới của dữ liệu (Content freshness)
- Crawler cần thu thập được dữ liệu mới, có yếu tố thời điểm
- Trùng lặp dữ liệu
- Các trang trùng lặp hoặc cả website được nhân bản

## Slide 24
- Cân bằng giữa exploitation vs. exploration
- Khai thác  - Exploitation
- Thu thập các trang mà có xác xuất cao có dữ liệu cần thu thập
- Khám phá - Exploration
- Khám phá các nguồn dữ liệu mới mà có thể có dữ liệu cần thu thập

## Slide 25
- Tính lịch thiệp - Politeness
- Mô tả rõ - Explicit
- Chỉ định bởi chủ trang web mô tả phần nào cảu website có thể được thu thập (robots.txt)
- Ngầm định - Implicit
- Tránh gây quá tải, thu thập quá thường xuyên dân tới tiêu tốn tài nguyên máy chủ, ảnh hưởng đến chất lượng cung cấp dịch vụ của máy chủ

## Slide 26
- Robots.txt
- Là giao thức đặc tả thể hiện sự giới hạn đối với các “robots”, đưa ra từ 1994
- www.robotstxt.org/wc/norobots.html
- Website chỉ định các nội dung không được thu thập
- Tạo tệp tin /robots.txt
- Chỉ định các giới hạn
- Ví dụ
- Sec. 20.2.1
- User-agent: *
- Disallow: /yoursite/temp/
- User-agent: searchengine
- Disallow:

## Slide 27
- Bóc tách thông tin khi thu thập (Web-scraping)

## Slide 28
- Kĩ thuật bóc tách
- Để bóc tách thông tin từ trang web, thường sử dụng XPath hoặc CSS Selector
- XPath là chuẩn của W3C để tìm kiếm một phần tử trong văn bản XML
- W3C là tổ chức xây dựng và quản lý các chuẩn web
- XPath sử dụng cấu trúc cây gồm các nút (và thuộc tính) trên tệp XML
- HTML là đặc tả tuân theo cấu trúc cây của XML

## Slide 29
- Cấu trúc mã HTML
- HTML có cấu trúc  của cây Document Object Model (DOM)
- DOM khác nhau tuỳ từng trang, thậm chí với cùng một dạng trang
- Do nội dung động, chèn quảng cáo, vvv.

## Slide 30
- Ví dụ về XPath
- Practice it yourself on https://www.w3schools.com/xml/xpath_examples.asp

## Slide 31
- Ví dụ về XPath

## Slide 32
- Các giới hạn về kỹ thuật
- Sự không nhất quán / hỗn loạn trong tổ chức thông tin
- Thông tin trong 1 website có bố cục HTML không giống nhau, ngay cả khi biểu diễn cùng một loại thông tin
- Sự thay đổi trong cấu trúc
- Các trình thu thập dữ liệu chạy liên tục
- Cấu trúc website cũng thay đổi theo thời gian, do cập nhật, chỉnh sửa
- Đặc biệt với các trang có trình quản lý themes, Content Management Systems (e.g. Wordpress)

## Slide 33
- Các giới hạn về kỹ thuật
- Giới hạn truy cập
- Nội dung bị giới hạn cho người dùng được xác thực
- Vẫn có thể tự động hoá được việc xác thực nhưng cần tài khoản
- Nội dung được sinh ra tự động
- Công nghệ web tiên tiến không tải về toàn bộ nội dung trong một lượt truy cập (request)
- Tuỳ theo tương tác người dùng mà tải về nội dung tương ứng
- Một vài công cụ có thể giả lập tương tác và trình duyệt, nhưng quá trình thu thập sẽ khó khăn hơn

## Slide 34
- Các giới hạn về kỹ thuật
- Chủ sở hữu của nguồn thông tin không ưa thích data scraping
- Gây quá tải cho hệ thống
- Mất mát doanh thu từ quảng cáo
- Mất kiểm soát tới dữ liệu, vi phạm bản quyền dữ liệu
- Chủ sở hữu website có thể sử dụng các kỹ thuật, công cụ để chặn truy cập từ trình thu thập
- Giới hạn lượt truy cập theo thời gian
- Con người thường không di chuyển giữa các trang quá nhanh

## Slide 35
- Các giới hạn về kỹ thuật
- Chủ sở hữu website có thể sử dụng các kỹ thuật, công cụ để chặn truy cập từ trình thu thập
- Chặn IP
- Tự động chặn khi quá nhiều request đến từ 1 IP
- DoS là một dạng của cyber-attacks
- Giới hạn băng thông
- Xác thực yêu cầu truy cập đến từ người
- Vd. CAPTCHA, vvv.

## Slide 36
- Khía cạnh đạo đức / pháp lý
- Pháp luật đối xử với việc thu thập thông tin
- Không rõ ràng với hầu hết các quốc gia
- European regulation « General Data Protection Regulation » (GDPR)
- Khác nhau tuỳ từng quốc gia
- Có OK không khi chúng ta đăng lại thông tin và vẫn chỉ rõ nguồn dữ liệu?
- Câu hỏi khó!
- Một mặt, quyền sở hữu trí tuệ được tôn trọng
- Mặt khác, nguồn dữ liệu gốc bị mất lượt truy cập (traffic), dẫn tới mất doanh thu

## Slide 37
- Khía cạnh đạo đức / pháp lý
- Chúng ta nên thông báo cho chủ sở hữu website về việc chúng ta có mong muôn sử dụng dữ liệu của họ
- Có thể nhận được sự cho phép từ đó tránh được các vấn đề về pháp lý
- Có thể nhận được API truy cập nếu có
- Chủ sở hữu website có thể yêu cầu đưa URL về trang của họ từ đó giúp cải thiện thứ hạng của họ trong máy tìm kiếm
- Lợi cả đôi bên, Win-win!

## Slide 38
- Thực hành
- Thu thập dữ liệu với Scrapy

## Slide 39
- Các công cụ thu thập dữ liệu
- Thư viện lập trình
- Scrapy, Beautifulsoup (Python), PhantomJS
- Cloud: ScrapingHub, Dexi.io...
- Phần mềm: ParseHub, OctoParse...
- Web-browser plugins:
- Data Scraper - Easy Web Scraping, Instant Data Scraper, Web Scraper

## Slide 40
- Giới thiệu về Scrapy
- Scrapy là một thư viện lập trình mã nguồn mở mạnh mẽ, viết bằng Python
- Scrapy có thể cài đặt sẵn mã chương trình cho các vấn đề của trình thu thập dữ liệu như
- Throttling
- Concurrency
- XML sitemaps
- Filtering duplicated URLs
- Retry on Error

## Slide 41
- Các thành phần của Scrapy

## Slide 42
- Các thành phần của Scrapy
- Scrapy Engine
- Điều khiển luồng giữa tất cả các thành phần
- Scheduler
- Nhận yêu cầu từ engine và đưa vào hàng đợi để xử lý
- Downloader
- Tải trang web và đưa về cho engine
- Spiders
- Bóc tách các trả lời gồm dữ liệu và các đường dẫn yêu cầu mới cần phải truy cập tới
- Item pipeline
- Xử lý dữ liệu sau khi được bóc bởi spider
- Downloader middlewares
- Xử lý các yêu cầu khi chúng đi từ engine tới downloader và ngược lại
- Spider middlewares
- Nằm giữa Engine và Spiders
- Xử lý các trả lời (responses) và các mục dữ liệu (items) và yêu cầu (requests)

## Slide 43
- Bài tập
- XPath
- Học trên https://www.w3schools.com/xml/xpath_examples.asp
- WebScraper tutorial
- https://www.webscraper.io/tutorials
- Scrapy
- https://doc.scrapy.org/en/latest/intro/tutorial.html
- https://doc.scrapy.org/en/latest/topics/media-pipeline.html
- «  Web Scraping in Python using Scrapy _ Codementor »: PDF  in the Google Teams

## Slide 44
- PageRank

## Slide 45
- Giới thiệu
- Thách  thực trong tìm kiếm thông tin trên World Wide Web.
- Số lượng các website khổng lồ: 150 million by1998, 1000 billion by 2008
- Thông tin trên các website rất đa dạng: đa dạng chủ đề và chất lượng, vv.
- PageRank là gì?
- Một phương pháp để đánh trọng số độ quan trọng của một trang web sử dụng cấu trúc liên kết giữa chúng.

## Slide 46
- Lịch sử của PageRank
- PageRank được phát triển bởi Larry Page và Sergey Brin
- Là một phần của dự án nghiên cứu về một máy tìm kiếm Internet. Dự án bắt đầu vào 1995 và có bản prototype nguyên mẫu vào 1998.
- Page và Brin sau đó sáng lập của Google.
- Ngày nay
- Có nhiều kỹ thuật dựng cấu trúc website và nội dung sao cho tối ưu hoá cho công cụ tìm kiếm, tăng thứ hạng (SEO).

## Slide 47
- Cấu trúc liên kết của Web
- 150 triệu trang web  1.7 tỷ liên kết (link)
- Backlinks and Forward links:
- A and B are C’s backlinks
- C is A and B’s forward link
- Một trang web là quan trọng nếu nó có nhiều backlinks.
- Một trang web có quan trọng không nếu có link từ www.cnn.com?

## Slide 48
- Giải thuật PageRank đơn giản hoá
- u: một trang web
- Bu: tập hợp các backlinks của u
- Nv: Số lượng các forward links của trang v
- c: Hệ số chuẩn hoá để đạt đựo
- ||R||L1 = 1 (||R||L1= |R1 + … + Rn|)

## Slide 49
- Giải thuật PageRank đơn giản hoá
- PageRank Calculation: first iteration

## Slide 50
- Giải thuật PageRank đơn giản hoá
- PageRank Calculation: second iteration

## Slide 51
- Giải thuật PageRank đơn giản hoá
- Convergence after some iterations

## Slide 52
- Vấn đề với PageRank đơn giản hoá
- Vòng lặp:
- Sau mỗi bước lặp, các trang nhận được thứ hạng nhưng không phân phối cho các trang khác!

## Slide 53
- Ví dụ

## Slide 54
- Ví dụ

## Slide 55
- Ví dụ

## Slide 56
- Random Walks in Graphs
- Mô hình duyệt ngẫu nhiên - Random Surfer Model
- Duyệt web liên tục đi theo các link với xác xuất ngẫu nhiên
- Mô hình duyệt có chỉnh sửa - The Modified Model
- Duyệt web liên túc theo các link với xác xuất ngẫu nhiên, nhưng định kỳ nhẩy vào một trang theo phân phối E

## Slide 57
- Một phiên bản cải tiến của PageRank
- E(u): a distribution of ranks of web pages that “users” jump to
- when  they “gets bored” after successive links at random.
- For uniform random jump: E(i) = 1/n

## Slide 58
- Ví dụ Modified PageRank

## Slide 59
- Dangling Links
- Link trỏ tới bất kỳ page nào mà không có link đi ra
- Phần lớn là các trang chưa được tải về xong
- Ảnh hưởng tới mô hình vì nó gây ra sự không rõ ràng về trọng số của nó sẽ được phân phối đi đâu
- Không ảnh hưởng tới tính thứ hạng của các trang khác
- Có thể đơn giản là bỏ đi trước khi tính pagerank và thêm vào sau đó

## Slide 60
- Cài đặt PageRank
- Chuyển đổi mỗi URL thành một số nguyên ID duy nhất, và lưu các hyperlink trong 1 cơ sở dữ liệu sử dụng ID để định danh các trang
- Sắp xếp cấu trúc liên kết bởi ID
- Xoá bỏ các dangling links
- Khởi tạo thứ hạng và bắt đầu các vòng lặp
- Giá trị khởi tạo tốt có thể tăng tốc hội tụ cho pagerank
- Thêm lại các dangling links.

## Slide 61
- Tính hội tụ Convergence Property
- PR (322 Million Links): 52 iterations
- PR (161 Million Links): 45 iterations
- Scaling factor is roughly linear in logn

## Slide 62
- Tìm kiếm với PageRank

## Slide 63
- Tìm kiếm với PageRank

## Slide 64
- Cá nhân hoá PageRank
- Một thành phần quan trọng trong tính toán PageRank là E
- E vector thể hiện phân phối của các trang web mà việc duyệt web liên túc theo các link với xác xuất ngẫu nhiên, nhưng định kỳ nhẩy vào một trang theo phân phối E
- Có thể sử dụng E vector để cá nhân hoá

## Slide 65
- Kết luận
- PageRank là giải thuật xếp hạng toàn cục cho tất cả các trang web dựa trên vị trí của trang web trên cấu trúc đồ thị web
- PageRank sử dụng thông tin để xếp hạng là các backlinks

## Slide 66