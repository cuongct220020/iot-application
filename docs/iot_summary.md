# IOT Summary


## Chương 1. Kiến trúc hệ thống và các trụ cột nền tảng

### 1.1. Định nghĩa chuyên sâu và các thành phần cốt lõi

Một định nghĩa chính xác và đầy đủ về IoT là nền tảng cho mọi phân tích sâu hơn. 
Theo tài liệu học phần, IoT là "mạng lưới của sự vật (things), với sự nhận dạng phần tử rõ ràng, được nhúng với trí tuệ phần mềm, các cảm biến và kết nối phổ biến với Internet".
Định nghĩa này hàm chứa bốn thành phân kỹ thuật không thể tách rời:
1. **Sensors (Cảm biến):** Đóng vai trò "giác quan", thu thập thông tin từ môi trường vật lý (nhiệt độ, ánh sáng, chuyển động).
2. **Identifiers (Định danh):** Mỗi thiết bị phải có một danh tính duy nhất (như địa chỉ MAC, IPv6, URI) để xác định nguồn gốc dữ liệu và đích đến của lệnh điều khiển.
3. **Software (Phần mềm):** Trí tuệ nhân tạo hoặc các thuật toán xử lý nhúng giúp phân tích dữ liệu sơ bộ hoặc ra quyết định cục bộ.
4. **Internet Connectivity (Kết nối Internet):** Phương tiện để giao tiếp, truyền tải dữ liệu và nhận thông báo.

Khái niệm "Things" trong IoT được mở rộng tối đa, bao trùm từ các thiết bị gia dụng, phương tiện giao thông, toà nhà đến cả sinh vật sống như cây cối, động vật (thông qua gắn chip theo dõi). 
Cisco thậm chí còn mở rộng khái niệm này thành **Internet of Everything (IoE)**, bao gồm bốn yếu tố: Con người, Quy trình, Dữ liệu và Sự vật.

### 1.2. Phân tích bốn trụ cột nền tảng (The Four Pillars)

Để đánh giá giá trị của một hệ thống IoT, ta có thể xem xét qua lăng kính của bốn trụ cột chính. Đây là những yếu tố toạ nên sự khác biệt giữa hệ thống nhúng truyền thống và môt hệ thống IoT hiện đại:

| Trụ cột                 | Mô tả chi tiết và ý nghĩa                                                                                                                                                                                                                                               |
|-------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Connection (Kết nối)    | Đây là nền tảng cơ bản nhất. IoT chuyển đổi các thiết bị từ trạng thái "đảo thông tin" cô lập sang trạng thái kết nối liên tục. Sự kết nối này không chỉ là vật lý (qua sóng vô tuyến/dây dẫn) mà còn là logic, cho phép các thiết bị "nhìn thấy" và giao tiếp với nhau |
| Collection (Thu thập)   | Với hàng tỷ cảm biến được triển khai, IoT tạo ra khả năng thu thập dữ liệu khổng lồ (Big Data) theo thời gian thực. Dữ liệu này không còn là các mẫu rời rạc mà là các dòng (streams) liên tục, phản ánh chính xác trạng thái của thế giới thực.                        |
| Computation (Tính toán) | Dữ liệu thô (raw data) vô nghĩa nếu không được xử lý. Trụ cột này đề cập đến khả năng tính toán tại biên (Edge Computing) và trên đám mây (Cloud Computing) để chuyển đổi dữ liệu thành thông tin (information) và tri thức (knowledge), từ đó hỗ trợ ra quyết định     |
| Creation (Sáng tạo)     | Đây là mục tiêu cuối cùng. Sự kết hợp giữa kết nối, dữ liệu và tính toán cho phép tạo ra các mô hình kinh doanh mới, các dịnh vụ chưa từng tồn tại (ví dụ: bảo trì tiên đoán, xe tự lái, nhà thông minh học thói quen người dùng).                                      |

### 1.3. Kiến trúc hệ thống: Từ đơn giản đến phức tạp
Việc hiểu rõ kiến trúc hệ thống là cực kỳ quan trọng để trả lời câu hỏi về luồng dữ liệu, và thiết kế hệ thống.
Học phần đề cập đến ba mô hình kiến trúc chính, phản ánh sự phát triển của công nghệ. 

#### 1.3.1. Các mô hình kết nối

- **Mô hình đơn giản (Direct to Cloud):** Thiết bị kết nối trực tiếp đến Cloud Server. Mô hình này phù hợp với các thiết bị có khả năng IP mạnh mẽ (như Camera IP) hoặc các ứng dụng quy mô nhỏ. Tuy nhiên, nó gặp thách thức về độ trễ và băng thông khi số lượng thiết bị tăng lên.
- **Mô hình phân cấp (Hierarchical):** Đây là mô hình phổ biến nhất hiện nay. Dữ liệu từ thiết bị đi qua các tầng trung gian như **Gateway, Frog Node,** hoặc **Edge Node** trước khi lên Server. Lớp trung gian này đóng vai trò tiền xử lý, lọc dữ liệu, chuyển đổi giao thức và bảo mật. Nó giải quyết vấn đề về độ trễ và giảm tải cho Cloud.
- **Mô hình tương lai (Mesh/Ad-hoc):** Các "Things" kết nối trực tiếp với nhau (Device-to-Device) để tự tổ chức và ra quyết định mà không phụ thuộc hoàn toàn vào hạ tầng trung tâm. Đây là xu hướng mạng lưới bầy đàn (swarm) hoặc xe tự hành.


#### 1.3.2. Kiến trúc phân lớp (Layered Architecture)

Để chuẩn hoá việc thiết kế, hệ thống IoT thường được mô tả qua mô hình 5 lớp chi tiết:

1. **Presentation/Sensing Layer (Lớp cảm nhận):** Lớp vật lý đáy cùng, bao gồm các cảm biến (thu thập thông tin) và cơ chế chấp hành (thực hiện lệnh). Nhiệm vụ chính là số hoá thế giới thực và nhận diện các đối tượng.
2. **Network Layer (Lớp mạng):** Chịu trách nhiệm truyền tải dữ liệu từ lớp cảm nhận lên các lớp trên. Bao gồm các công nghệ truyền dẫn (WiFi, 4G, LoRa) và các thiết bị định tuyến, Gateway. Đây là "Đường cao tốc" của dữ liệu.
3. **Middleware/Service Layer (Lớp dịch vụ):** Cung cấp các công cụ để lưu trữ, tính toán và xử lý dữ liệu. Nó ẩn đi sự phức tạp của phần cứng bên dưới và cung cấp API chuẩn cho lớp ứng dụng. Các nền tảng IoT (IoT Platforms) thường nằm ở lớp này.
4. **Application Layer (Lớp ứng dụng):** Nơi tương tác với người dùng cuối, cung cấp các giao diện và logic nghiệp vụ cụ thể (như ứng dụng Smart Home trên điện thoại).
5. **Business Layer (Lớp kinh doanh):** : Lớp cao nhất, tập trung vào việc quản lý toàn bộ hệ thống, xây dựng các mô hình kinh doanh, phân tích lợi nhuận và chiến lược dựa trên dữ liệu thu được.

## Chương 2. Công nghệ IoT cốt lõi và các giao thức truyền thông

Đây là chương trọng tâm nhất về mặt kỹ thuật, chứa đựng lượng kiến thức lớn về các giao thức và tiêu chuẩn mà sinh viên cần nắm vững cho bài thi trắc nghiệm.

### 2.1. Thiết bị và cảm biến
Trong IoT, thiết bị (device) là một khái niệm rộng, thường là sự kết hợp của phần cứng xử lý (vi điều khiển/vi xử lý) và các thành phần ngoại vi.


#### 2.1.1. Phân loại dữ liệu thiết bị
Để thiết kế cơ sở dữ liệu và giao thức truyền thông hiệu quả, cần phân biệt rõ ba loại dữ liệu mà một thiết bị IoT xử lý:

- **Metadata (Siêu dữ liệu):** Là các thông tin định danh và cấu hình tĩnh của thiết bị. Ví dụ: Device ID, Serial Number, Model, Firmware Version, Ngày sản xuất. Dữ liệu này ít thay đổi và thường chỉ được gửi một lần khi khởi động hoặc khi có yêu cầu truy vấn.
- **Telemetry (Dữ liệu đo xa):** Là dữ liệu "trái tim" của hệ thống IoT, được thu thập từ các cảm biến. Đặc điểm của Telemetry là tính thời gian thực (real-time), thay đổi liên tục và thường là dữ liệu chỉ đọc (Read-Only) từ góc độ Cloud. Ví dụ: Nhiệt độ 25.5°C, Độ ẩm 60%, Toạ độ GPS.
- **State (Trạng thái):** Là thông tin mô tả tình trạng hoạt động hiện tại của thiết bị, có tính chất hai chiều (Read/Write). Ví dụ: Trạng thái đèn (ON/OFF), tốc độ quạt (Level 1-5). Cloud có thể gửi lệnh để thay đổi State, và thiết bị phải cập nhật State mới nhất trên Cloud. 



#### 2.1.2. Phân loại cảm biến

Các cảm biến có thể được phân loại dựa trên nhiều tiêu chí kỹ thuật:

- **Theo nguồn năng lượng:**
  * _Passive (Thụ động):_ Không cần nguồn cung cấp năng lượng riêng để hoạt động cảm biến, mà biến đổi trực tiếp năng lượng từ môi trường thành tín hiệu điện (Ví dụ: Thermocouple, Piezoelectric).
  * _Active (Chủ động):_ Cần nguồn điện bên ngoài để hoạt động mạch đo (ví dụ: Cảm biến siêu âm, cảm biến hồng ngoại, Camera).
- **Theo tín hiệu đầu ra:** Analog (cần bộ chuyển đổi ADC) và Digital (giao tiếp qua I2C, SPI, UART).
- **Theo bản chất đại lượng đo:** Cơ học, Nhiệt, Điện, Quang, Hoá học, Sinh học.


### 2.2. Phân tích chuyên sâu các giao thức truyền thông

Sự lựa chọn giao thức truyền thông quyết định hiệu năng, độ trễ và mức tiêu thủ năng lượng của hệ thống IoT. 
Ba giao thức truyền thông được giảng dạy là HTTP, MQTT, AMQP. 

#### 2.2.1. HTTP/HTTPS (HyperText Transfer Protocol)
Mặc dù được thiết kế cho Web, HTTP vẫn được sử dụng rộng rãi trong IoT nhờ tính phổ biến và khả năng tương thích với các tường lửa (firewall).

- **Mô hình:** Client-Server (Request-Response). Kết nối thường ngắn hạn (short-lived), đóng lại sau khi hoàn tất yêu cầu.
- **Overhead:** Rất lớn. Mỗi gói tin HTTP mang theo nhiều header (User-Agent, Content-Type, Authorization...) dưới dạng văn bản (text-based), gây tốn băng thông và năng lượng xử lý.
- **Các phương thức (Methods) trong ngữ cảnh IoT:**
  * `GET`: Thiết bị yêu cầu cấu hình và trạng thái từ Server. Dữ liệu tham số nằm trong URL.
  * `POST`: Thiết bị gửi dữ liệu Telemetry lên Server. Dữ liệu nằm trong Body (thường là JSON).
  * `PUT`: Cập nhật trạng thái đầy đủ.
- **Mã phản hồi (Response Code) cần ghi nhớ:**
  * `2xx`: Thành công (`200 OK`, `201 Created`) - tạo tài nguyên mới, `204 No Content` - thành công nhưng không trả về Body.
  * `4xx`: Lỗi phía Client (`400 Bad Request`, `401 Unauthorized` - thiếu access token, `403 Forbidden` - có access token nhưng không đủ quyền, `404 Not Found`).
  * `5xx`: Lỗi phía Server (`500 Internal Server Error`, `502 Bad Gateway`, `503 Service Unavailable`).

#### 2.2.2. MQTT (Message Queuing Telemetry Transport)

MQTT là giao thức được tối ưu hoá riêng cho IoT, hoạt động trên nền tảng TCP/IP.

- **Mô hình:** Publish/Subscribe
  * **Broker:** Máy chủ trung gian, chịu trách nhiệm nhận tin, lọc và phân phối tin nhắn. Broker nắm giữ "bảng định tuyến" logic giữa các topic.
  * **Client:** Có thể là Publisher (người gửi) hoặc Subscriber (người nhận). Client không biết về sự tồn tại của các Client khác, chỉ biết Broker.

- **Cấu trúc gói tin (Packet Structure):** Được thiết kế tối giản để tiết kiệm băng thông.
  * **Fixed Header (bắt buộc):** Tối thiểu 2 bytes. Byte 1 chứa loại gói tin (Control Packet Type - 4 bits) và Các cờ (Flags - 4 bits). Byte 2 trở đi chứa Reamining Length.
  * **Variable Header:** Tuỳ chọn, chứa thông tin như Packet Identifier.
  * **Payload:** Nội dung thực sự của tin nhắn.

- **Các mức chất lượng dịch vụ (QoS):** Đây là phần kỹ thuật phức tạp nhất cần nắm vững. 
  * **QoS 0 (At Most Once - Fire and Forget):** Gửi đi và không cần xác nhận. Tin nhắn có thể bị mất nếu mạng rớt. Dựa hoàn toàn vào độ tin cậy của TCP bên dưới. Không có gói tin ACK ở tầng ứng dụng.
  * **QoS 1 (At Least Once):** Đảm bảo tin nhắn đến ít nhất một lần.
    * Sender gửi `PUBLISH`.
    * Receiver nhận và gửi lại `PUBACK`.
    * Nếu Sender không nhận được `PUBACK` sau một khoảng thời gian, nó sẽ gửi lại gói tin với cờ `DUP` được bật. Điều này có thể dẫn đến Receiver nhận được nhiều bản sao của cùng một tin nhắn.
  * **QoS 2 (Exactly Once):** Đảm bảo tin nhắn đến chính xác một lần. Quy trình bắt tay 4 bước (4-way handshake) để loại bỏ trùng lặp.
    * **Sender** gửi `PUBLISH` (lưu message lại).
    * **Receiver** nhận, lưu message identifier, gửi `PUBREC` (Publish Received).
    * **Sender** nhận `PUBREC`, xoá message gốc, gửi `PUBREL` (Publish Release) để báo cho Receiver biết là Sender đã xác nhận.
    * **Receiver** nhận `PUBREL`, chuuyển message tới ứng dụng xử lý, xoá identifier đã lưu, và gửi `PUBCOMP` (Publish Complete).
    * **Sender** nhận `PUBCOMP` và hoàn tất giao dịch. 

- **Các tính năng đặc biệt:**
  * **Retained Messages:** Broker lưu giữ tin nhắn cuối cùng của một Topic và gửi ngay cho Subcriber mới vừa kết nối. Hữu ích để cập nhật trạng thái thiết bị ngay khi mở app.
  * **Last Will and Testament (LWT):** Một tin nhắn được Client gửi sẵn cho Broker khi kết nối. Nếu Client mất kết nối đột ngột (không gửi lệnh `DISCONNECT`), Broker sẽ tự động publish tin nhắn LWT đến một topic quy định, giúp hệ thống phát hiện sự cố thiết bị. 

    
#### 2.2.3. AMQP (Advanced Message Queuing Protocol)

Giao thức hướng tin nhắn doanh nghiệp, hỗ trợ độ tin cậy cao và các kịch bản định tuyến phức tạp.
RabbitMQ là broker phổ biến nhất sử dụng AMQP.

- **Các thực thể chính:**
  * **Producer:** Ứng dụng gửi tin nhắn.
  * **Consumer:** Ứng dụng nhận và xử lý tin nhắn. 
  * **Queue:** Vùng đệm lưu trữ tin nhắn. Tin nhắn ở trong Queue cho đến khi Consumer lấy đi.
  * **Exchange:** Bưu điện trung tâm. Producer không bao giờ gửi thẳng vào Queue mà gửi vào Exchange. Exchange sẽ định tuyến tin nhắn vào các Queue dựa trên quy tắc (Bindings).

- **Các loại Exchange (Exchange Types) - Cân phân biệt chi tiết:**
  * **Direct Exchange:** Định tuyến dựa trên sự trùng khớp chính xác của khoá định tuyến (`routing_key`).
    * Ví dụ: Queue A bind với khoá "orange". Tin nhắn có khoá "orange" sẽ vào Queue A. Tin nhắn khoá "black" sẽ bị loại bỏ (nếu không có queue nào khớp). Direct Exchange mặc định (Default Exchange) có tên rỗng, tự động route tin nhắn đến Queue có tên trùng với routing key.
  * **Fanout Exchange:** Định tuyến kiểu quảng bá (Broadcast). Nó bỏ qua `routing_key` và sao chép tin nhắn gửi đến tất cả các Queue đang bind với nó.
    * Ví dụ: Hệ thống thông báo khẩn cấp, bảng tỷ số thể thao trực tuyến. 
  * **Topic Exchange:** Định tuyến dựa trên mẫu (Pattern Matching) của `routing_key`. Khoá định tuyến là một chuỗi các từ phân cách bởi dấu chấm (ví dụ: `agri.sensor.temp`).
    * Ký tự `*` (sao): Thay thế cho chính xác một từ. (Ví dụ: `agri.*.temp` khớp `agri.sensor.temp` nhưng không khớp `agri.sensor.hanoi.temp`).
    * Ký tự `#` (thăng): Thay thế cho không hoặc nhiều từ. (Ví dụ: `agri.#` khớp tất cả tin bắt đầu bằng `agri`).
  * **Header Exchange:** Định tuyến không dựa trên `routing_key` mà dựa trên cặp key-value trong phần **Header** của tin nhắn. 
    * Tham số `x-match`:
      * `all`: Tất cả các cặp header trong binding phải khớp với header của tin nhắn.
      * `any`: Chỉ cần một cặp header khớp là đủ. 

### 2.3. So sánh tổng hợp: HTTP, MQTT, AMQP


| Đặc tính | HTTP (REST) | MQTT | AMQP |
|--------|-------------|------|------|
| **Mô hình kiến trúc** | Request/Response (Đồng bộ) | Publish/Subscribe (Bất đồng bộ) | Publish/Subscribe & Queue-based |
| **Vai trò các bên** | Client – Server | Client – Broker – Client | Producer – Exchange – Queue – Consumer |
| **Định dạng dữ liệu** | Text-based (Header lớn) | Binary (Header rất nhỏ, tối thiểu 2 bytes) | Binary (Header cố định ~8 bytes) |
| **QoS (Độ tin cậy)** | Không hỗ trợ (dựa vào TCP) | Hỗ trợ 3 mức (0, 1, 2) | Hỗ trợ qua ACK và Transactions |
| **Duy trì kết nối** | Connectionless (ngắn hạn) | Connection-oriented (dài hạn, Keep-alive) | Connection-oriented |
| **Mức tiêu thụ năng lượng** | Cao (overhead lớn, kết nối lại nhiều) | Thấp (giữ kết nối, gói tin nhỏ) | Trung bình – Cao (tính năng phức tạp) |
| **Trường hợp sử dụng** | Web API, tải file, gửi dữ liệu lớn không thường xuyên | Thiết bị pin, mạng yếu, dữ liệu thời gian thực | Backend doanh nghiệp, yêu cầu độ tin cậy cao |


# Chương 3: Lập trình Ứng dụng IoT và Nền tảng

Chương này chuyển hóa các kiến thức lý thuyết thành kỹ năng thực hành, tập trung vào việc lập trình thiết bị đầu cuối và xây dựng hệ thống backend.

## 3.1. Lập trình Thiết bị (Device Side) với ESP32

Học phần sử dụng ESP32 làm nền tảng phần cứng chính do tính năng mạnh mẽ và giá thành rẻ.

### Kiến trúc Phần cứng

ESP32 là vi điều khiển 32-bit lõi kép (Dual-core), tích hợp sẵn WiFi (2.4GHz) và Bluetooth (Classic + BLE). Điều này cho phép nó vừa xử lý tác vụ mạng, vừa đọc cảm biến mà không bị nghẽn.

### Môi trường Lập trình

Sử dụng Arduino IDE hoặc PlatformIO.

### Các kỹ thuật Lập trình Cơ bản

- **GPIO:** Điều khiển kỹ thuật số (Digital I/O). Cần lưu ý các chân đặc biệt (Input only, Strapping pins).

- **ADC (Analog to Digital Converter):** ESP32 có 2 bộ ADC với độ phân giải lên đến 12-bit (giá trị 0-4095), dùng để đọc cảm biến analog như cảm biến độ ẩm đất, quang trở. Lưu ý đặc tuyến ADC của ESP32 không hoàn toàn tuyến tính.

- **Giao tiếp ngoại vi:** Sử dụng thư viện `Wire.h` cho giao tiếp I2C (kết nối màn hình OLED, cảm biến gia tốc MPU6050) và `SPI.h` cho giao tiếp tốc độ cao (thẻ nhớ SD, module LoRa).

### Hệ điều hành Thời gian thực (FreeRTOS)

Khác với Arduino Uno chạy vòng lặp `loop()` đơn tuần tự, ESP32 chạy trên FreeRTOS. Điều này cho phép lập trình đa nhiệm (Multi-tasking).

- **Tasks:** Có thể chia nhỏ chương trình thành các tác vụ chạy song song (ví dụ: Task 1 đọc cảm biến, Task 2 gửi dữ liệu WiFi).

- **Queues:** Dùng để truyền dữ liệu an toàn giữa các Task.

- **Semaphores/Mutexes:** Dùng để đồng bộ hóa và quản lý truy cập tài nguyên chia sẻ (tránh xung đột khi 2 task cùng truy cập 1 biến).

## 3.2. Lập trình Giao tiếp Mạng

### Thư viện WiFi

Sử dụng `WiFi.h` để kết nối vào Access Point (`WiFi.begin(ssid, password)`). Quan trọng nhất là xử lý sự kiện mất kết nối và tự động kết nối lại (`WiFi.reconnect()`).

### Thư viện HTTPClient

Dùng để gửi GET/POST request lên server.

### Thư viện PubSubClient

Dùng cho giao thức MQTT.

- Cần thiết lập `setServer` (địa chỉ Broker) và `setCallback` (hàm xử lý khi có tin nhắn đến).
- Vòng lặp `client.loop()` phải được gọi liên tục trong `loop()` để duy trì kết nối và xử lý gói tin Keep-Alive.

## 3.3. Nền tảng IoT (IoT Platforms): ThingsBoard

Học phần giới thiệu ThingsBoard như một nền tảng mã nguồn mở tiêu biểu để quản lý thiết bị và hiển thị dữ liệu.

### Device Provisioning

Quy trình đăng ký thiết bị mới vào hệ thống.

### Data Collection

Tiếp nhận dữ liệu Telemetry qua MQTT, HTTP hoặc CoAP.

### Visualization

Xây dựng Dashboard với các Widget (biểu đồ, đồng hồ đo, bản đồ) để trực quan hóa dữ liệu thời gian thực.

### Rule Engine

Thành phần mạnh mẽ nhất, cho phép định nghĩa các quy tắc xử lý logic (Ví dụ: Nếu nhiệt độ > 30 độ VÀ độ ẩm < 40% THÌ gửi email cảnh báo và kích hoạt máy bơm). Rule Engine giúp xử lý sự kiện phức tạp mà không cần viết code backend nhiều.


# Chương 4: An toàn và Bảo mật trong IoT

Đây là chương quan trọng đề cập đến "gót chân Achilles" của IoT. Do sự hạn chế về tài nguyên phần cứng và sự phân mảnh của các chuẩn công nghệ, thiết bị IoT thường là mục tiêu tấn công dễ dàng.

## 4.1. Tam giác Bảo mật Mở rộng (CIA + A)

Bảo mật IoT không chỉ dừng lại ở mô hình CIA truyền thống mà còn bổ sung thêm tính xác thực:

### Confidentiality (Tính bí mật)

Đảm bảo dữ liệu không bị lộ lọt cho bên thứ ba trái phép.

**Giải pháp:** Mã hóa dữ liệu đường truyền (TLS/SSL cho MQTT/HTTP), mã hóa dữ liệu lưu trữ (AES).

### Integrity (Tính toàn vẹn)

Đảm bảo dữ liệu không bị thay đổi, giả mạo trên đường truyền.

**Giải pháp:** Sử dụng hàm băm (Hashing), chữ ký số (Digital Signature), Message Integrity Code (MIC).

### Availability (Tính sẵn sàng)

Đảm bảo hệ thống và dịch vụ luôn truy cập được khi cần.

**Mối đe dọa:** Tấn công từ chối dịch vụ (DoS), gây nghẽn băng thông hoặc cạn kiệt pin thiết bị.

### Authenticity (Tính xác thực)

Đảm bảo danh tính của các bên tham gia giao tiếp là chính chủ.

**Giải pháp:** Xác thực hai chiều (Mutual Authentication), sử dụng Token (JWT), Certificates (X.509).

## 4.2. Các Dạng Tấn công Phổ biến vào Hạ tầng IoT

Hacker có thể tấn công vào bất kỳ lớp nào trong kiến trúc IoT:

### Physical Attacks (Tấn công vật lý)

Tiếp cận trực tiếp thiết bị để trích xuất firmware qua cổng debug (JTAG, UART), hoặc phá hoại cảm biến.

### Network Attacks (Tấn công mạng)

- **Sniffing (Nghe lén):** Bắt gói tin không mã hóa trong mạng WiFi/LAN.
- **Man-in-the-Middle (MitM):** Giả mạo trạm phát sóng hoặc DNS để đứng giữa thiết bị và server.

### Software Attacks (Tấn công phần mềm)

- **Malware/Botnets:** Tiêm mã độc (như Mirai) để biến thiết bị thành "zombie" phục vụ tấn công DDoS.
- **Buffer Overflow:** Khai thác lỗi tràn bộ đệm trong firmware để thực thi mã từ xa.

## 4.3. Phân tích Chi tiết 10 Điểm yếu Bảo mật Hàng đầu (OWASP IoT Top 10)

Tài liệu ôn tập yêu cầu nắm vững danh sách này từ dự án OWASP (Open Web Application Security Project):

### 1. Weak, Guessable, or Hardcoded Passwords

Sử dụng mật khẩu mặc định (admin/1234), mật khẩu yếu, hoặc mật khẩu bị code cứng trong firmware không thể thay đổi. Đây là nguyên nhân chính dẫn đến sự lây lan của botnet Mirai.

**Khắc phục:** Buộc người dùng đổi mật khẩu lần đầu, sử dụng xác thực đa yếu tố (MFA).

### 2. Insecure Network Services

Thiết bị chạy các dịch vụ mạng không cần thiết hoặc không an toàn (như Telnet, FTP, SSH phiên bản cũ) mở cổng ra Internet.

**Khắc phục:** Đóng các cổng không dùng, sử dụng tường lửa, chỉ dùng giao thức bảo mật (SSHv2, SFTP).

### 3. Insecure Ecosystem Interfaces

Các giao diện Web quản trị, API Cloud, hoặc ứng dụng Mobile đi kèm có lỗ hổng (như SQL Injection, XSS, thiếu xác thực).

**Khắc phục:** Kiểm thử bảo mật (Pentest) định kỳ các giao diện, áp dụng bộ lọc đầu vào chặt chẽ.

### 4. Lack of Secure Update Mechanism

Thiết bị không có khả năng cập nhật từ xa (OTA), hoặc quy trình cập nhật không xác thực chữ ký số của firmware, cho phép hacker cài firmware độc hại. Không có cơ chế chống rollback (cài lùi về phiên bản cũ có lỗi).

**Khắc phục:** Sử dụng Signed Firmware, mã hóa kênh truyền cập nhật, chỉ cho phép cập nhật phiên bản mới hơn.

### 5. Use of Insecure or Outdated Components

Sử dụng các thư viện phần mềm bên thứ ba, hệ điều hành cũ đã biết có lỗ hổng bảo mật mà không được vá.

**Khắc phục:** Quản lý danh sách phần mềm (SBOM), theo dõi các bản vá lỗi CVE.

### 6. Insufficient Privacy Protection

Thu thập dữ liệu cá nhân nhạy cảm quá mức cần thiết hoặc lưu trữ chúng mà không được bảo vệ/mã hóa.

**Khắc phục:** Áp dụng nguyên tắc "Privacy by Design", chỉ thu thập dữ liệu tối thiểu, ẩn danh hóa dữ liệu.

### 7. Insecure Data Transfer and Storage

Truyền dữ liệu nhạy cảm (mật khẩu, thông tin cá nhân) dưới dạng văn bản rõ (Plaintext) qua mạng công cộng.

**Khắc phục:** Bắt buộc sử dụng TLS/SSL cho mọi giao tiếp mạng. Mã hóa dữ liệu khi lưu trữ (At rest).

### 8. Lack of Device Management

Không quản lý được danh sách thiết bị trong hệ thống, không phát hiện được thiết bị lạ/thiết bị giả mạo.

**Khắc phục:** Sử dụng chứng chỉ số cho từng thiết bị, hệ thống giám sát tài sản IoT.

### 9. Insecure Default Settings

Thiết bị xuất xưởng với cấu hình mặc định kém an toàn (như bật sẵn UPnP, quyền truy cập root).

**Khắc phục:** Cấu hình mặc định phải là an toàn nhất (Secure by Default).

### 10. Lack of Physical Hardening

Thiết bị dễ dàng bị tháo mở, các cổng debug (USB, SD Card) dễ dàng truy cập để sao chép dữ liệu hoặc cài mã độc.

**Khắc phục:** Sử dụng vỏ chống cạy phá (Tamper-resistant), vô hiệu hóa các cổng debug trên mạch sản xuất.


# Chương 5: Thiết kế Hệ thống và Ứng dụng Thực tế

Chương này tổng hợp kiến thức để giải quyết bài toán thực tế. Sinh viên cần nắm vững quy trình từ ý tưởng đến triển khai.

## 5.1. Quy trình Thiết kế Hệ thống IoT

Quy trình chuẩn bao gồm các bước:

### 1. Xác định Vấn đề (Problem Definition)

Nhu cầu là gì? (Ví dụ: Giám sát cây trồng tự động).

### 2. Phân tích Yêu cầu (Requirements Analysis)

Yêu cầu phi chức năng (giá thành, năng lượng, độ bền) và chức năng (đo nhiệt độ, độ ẩm, điều khiển bơm).

### 3. Thiết kế Kiến trúc (Architecture Design)

Chọn mô hình (Cloud-centric hay Edge-centric?). Vẽ sơ đồ khối.

### 4. Lựa chọn Công nghệ (Technology Selection)

- **Cảm biến:** Chọn DHT11 (rẻ, kém chính xác) hay SHT30 (đắt, chính xác)?
- **Vi điều khiển:** ESP32 (WiFi) hay STM32 + LoRa (tầm xa)?
- **Giao thức:** MQTT (nhẹ) hay HTTP (dễ tích hợp)?

### 5. Triển khai (Implementation)

Lập trình Firmware, Backend, Mobile App.

### 6. Kiểm thử và Bảo trì (Testing & Maintenance)

## 5.2. Case Study: Hệ thống Nông nghiệp Thông minh (Smart Agriculture)

### Bài toán

Giám sát độ ẩm đất và điều khiển tưới cho một nông trại rộng lớn, không có WiFi phủ sóng toàn bộ.

### Giải pháp Thiết kế

- **Node cảm biến:** Sử dụng vi điều khiển tiết kiệm năng lượng (như STM32) kết nối cảm biến độ ẩm đất dung dung (Capacitive Soil Moisture). Sử dụng pin năng lượng mặt trời.

- **Truyền thông:** Sử dụng công nghệ LoRaWAN thay vì WiFi do cần truyền xa (km) và tiết kiệm pin.

- **Gateway:** Một thiết bị trung tâm (Raspberry Pi + LoRa Module) thu thập dữ liệu từ các node LoRa và gửi lên Cloud qua 4G/LTE.

- **Protocol:** Gateway dùng MQTT gửi dữ liệu lên ThingsBoard.

- **Ứng dụng:** Dashboard trên ThingsBoard hiển thị biểu đồ độ ẩm, Rule Engine tự động gửi lệnh xuống Gateway để bật máy bơm khi độ ẩm < 30%.

## 5.3. Case Study: Nhà Thông minh (Smart Home)

### Bài toán

Điều khiển đèn, rèm, giám sát an ninh trong nhà.

### Giải pháp Thiết kế

- **Cảm biến/Thiết bị:** Đèn thông minh, Cảm biến cửa, Camera IP.

- **Truyền thông:** Sử dụng Zigbee hoặc Z-Wave cho các cảm biến nhỏ (để tạo mạng Mesh, độ trễ thấp). Sử dụng WiFi cho Camera (băng thông lớn).

- **Hub trung tâm:** Home Assistant chạy trên Raspberry Pi, đóng vai trò Gateway kết nối Zigbee và WiFi.

- **Protocol:** MQTT được dùng làm trục xương sống (Backbone) để các thiết bị giao tiếp với Hub.