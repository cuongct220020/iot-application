# BÁO CÁO BÀI TẬP MQTT

## MÔ PHỎNG 100 THIẾT BỊ IOT

---

**Họ và tên:** [Điền tên của bạn]  
**MSSV:** [Điền MSSV]  
**Lớp:** [Điền lớp]  
**Ngày thực hiện:** [Điền ngày]

## 1. GIỚI THIỆU

Bài tập thực hiện mô phỏng hệ thống IoT với 100 thiết bị giao tiếp qua giao thức MQTT. Chương trình sử dụng:

- **Ngôn ngữ:** Python 3.13
- **Broker:** EMQX (local)
- **Công nghệ:** Multi-threading để mô phỏng 100 thiết bị đồng thời

## 2. CÀI ĐẶT MQTT BROKER

### 2.1. Lựa chọn Broker

**Broker đã chọn:** [Điền EMQX hoặc Mosquitto]

**Lý do lựa chọn:**

- EMQX: Giao diện quản lý trực quan, hỗ trợ dashboard web

### 2.2. Cài đặt

**Hệ điều hành:** [Windows/Linux/MacOS]

**Các bước cài đặt:**

[Mô tả ngắn gọn các bước cài đặt broker]

**Kiểm tra broker:**
 
[Chụp ảnh màn hình broker đang chạy - ví dụ: EMQX Dashboard, hoặc command line status của Mosquitto]

### 2.3. Thông số quản lý Broker

#### EMQX Dashboard (nếu dùng EMQX)

**URL truy cập:** http://localhost:18083  
**Username:** admin  
**Password:** public

**Các thông số quan trọng:**

| Thông số            | Mô tả                          | Vị trí xem                |
|---------------------|--------------------------------|---------------------------|
| Connections         | Số kết nối hiện tại            | Dashboard → Overview      |
| Subscriptions       | Số subscription đang hoạt động | Dashboard → Subscriptions |
| Topics              | Danh sách topics               | Dashboard → Topics        |
| Message In/Out Rate | Tốc độ tin nhắn                | Dashboard → Metrics       |
| Uptime              | Thời gian chạy                 | Dashboard → Overview      |
| Memory Usage        | Bộ nhớ sử dụng                 | Dashboard → Metrics       |

[Chụp ảnh Dashboard EMQX hiển thị Overview với các metrics]

#### Mosquitto (nếu dùng Mosquitto)

**File cấu hình:** `/etc/mosquitto/mosquitto.conf` (Linux) hoặc `C:\Program Files\mosquitto\mosquitto.conf` (Windows)

**Các thông số cấu hình:**

```conf
port 1883                      # Port mặc định
max_connections -1             # Số kết nối tối đa (-1 = unlimited)
allow_anonymous true           # Cho phép kết nối không cần authentication
log_dest file /var/log/mosquitto/mosquitto.log
```

## 3. KIẾN TRÚC HỆ THỐNG

### 3.1. Sơ đồ tổng quan

```
```
┌─────────────────────────────────────────────────────────────────┐
│                        MQTT BROKER (EMQX)                              │
│                                                       │
│                      localhost:1883                              │
└────────────┬────────────────────────────────────┬────────────────┘
             │ PUBLISH                            │ SUBSCRIBE
             │ (QoS 1)                            │ (Wildcard: iot/environment/#)
             │                                    │
    ┌────────┴─────────┐                  ┌───────┴─────────┐
    │  100 Publishers  │                  │  N Subscribers  │
    │   (Threading)    │                  │   (Threading)   │
    └──────────────────┘                  └─────────────────┘
           │                                       │
           │                                       │
    ┌──────┴──────┐                        ┌──────┴──────┐
    │ Device 1    │                        │  Nhận và    │
    │ Device 2    │                        │  xử lý dữ   │
    │ Device 3    │                        │  liệu từ    │
    │    ...      │                        │  100 thiết  │
    │ Device 100  │                        │  bị         │
    └─────────────┘                        └─────────────┘
         │
         │ Topic: iot/environment/city_center/temperature
         │ Topic: iot/environment/park_north/humidity
         │ Topic: iot/environment/industrial_zone/air_quality
         │        ...
         │ Topic: iot/environment/{location}/{sensor_type}
```

### 3.2. Luồng dữ liệu

1. **Khởi tạo:** Tạo 100 threads cho publishers và N threads cho subscribers.
2. **Kết nối:** Mỗi device và subscriber kết nối đến broker với Client ID riêng.
3. **Subscribe:** Mỗi subscriber subscribe wildcard `iot/environment/#` để nhận dữ liệu từ tất cả các thiết bị môi trường.
4. **Publish:** Mỗi device gửi 10 tin nhắn, mỗi 5 giây, đến các topic dạng `iot/environment/{location}/{sensor_type}`.
5. **Receive:** Các subscribers nhận và xử lý tất cả tin nhắn.
6. **Statistics:** Cập nhật thống kê real-time.

## 4. THIẾT KẾ CHƯƠNG TRÌNH

### 4.1. Cấu trúc file


### 4.2. Class DevicePublisher

**Chức năng:** Mô phỏng 1 thiết bị IoT gửi dữ liệu môi trường. Mỗi publisher sẽ được gán ngẫu nhiên một `location` và `sensor_type` từ danh sách cấu hình sẵn, và gửi dữ liệu đến topic tương ứng.

**Code chính:**

```python
class DevicePublisher:
    def __init__(self, device_id, broker, port, total_messages_per_device, publish_interval, statistics):
        self.device_id = device_id
        self.broker = broker
        self.port = port
        self.total_messages_per_device = total_messages_per_device
        self.publish_interval = publish_interval
        self.statistics = statistics
        self.client = mqtt.Client(client_id=f"publisher_{device_id}")
        
        # Gán ngẫu nhiên location và sensor_type
        self.location = random.choice(ENVIRONMENT_LOCATIONS)
        self.sensor_type = random.choice(ENVIRONMENT_SENSOR_TYPES)
        self.topic = f"{ENVIRONMENT_TOPIC_BASE}/{self.location}/{self.sensor_type}"
        
        self.packet_no = 0
        self.is_connected = False

    # ... (các phương thức khác)

    def generate_sensor_data(self):
        # Tạo dữ liệu cảm biến ngẫu nhiên dựa trên sensor_type và SENSOR_VALUE_RANGES
        # ...
        return {
            "id": self.device_id,
            "location": self.location,
            "sensor_type": self.sensor_type,
            "packet_no": self.packet_no,
            "value": sensor_value, # Giá trị cảm biến
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def run(self):
        # ... (logic chạy publisher)
```

### 4.3. Class DeviceSubscriber

**Chức năng:** Mỗi instance mô phỏng một subscriber nhận dữ liệu từ tất cả các thiết bị môi trường bằng cách subscribe wildcard `iot/environment/#`.

**Code chính:**

```python
class DeviceSubscriber:
    def __init__(self, subscriber_id, broker, port, statistics):
        self.subscriber_id = subscriber_id
        self.broker = broker
        self.port = port
        self.statistics = statistics
        self.client = mqtt.Client(client_id=f"subscriber_{subscriber_id}")
        self.received_messages = {}

    # ... (các phương thức khác)

    def on_connect(self, client, userdata, flags, rc):
        # Subscribe wildcard topic iot/environment/#
        # ...

    def on_message(self, client, userdata, msg):
        # Xử lý tin nhắn nhận được, parse JSON và cập nhật thống kê
        # ...

    def run(self):
        # ... (logic chạy subscriber)
```

### 4.4. Class Simulation

**Chức năng:** Quản lý toàn bộ quá trình mô phỏng, bao gồm khởi tạo và chạy các publishers và subscribers, cũng như thu thập và hiển thị thống kê.

**Code chính:**

```python
class Simulation:
    def __init__(self):
        self.statistics = Statistics()
        self.subscribers = []
        self.monitor_thread = None

    def run_full_simulation(self):
        # Khởi tạo và chạy nhiều subscribers
        self._run_subscribers()
        # Khởi tạo và chạy publishers
        self._run_publishers()
        # ... (logic quản lý và hiển thị thống kê)
```

### 4.5. Multi-threading

**Code khởi tạo threads:**

```python
def _run_publishers(self):
    threads = []
    for i in range(1, NUM_DEVICES + 1):
        publisher = DevicePublisher(...)
        thread = threading.Thread(target=publisher.run, daemon=True)
        threads.append(thread)
        thread.start()
    # ...

def _run_subscribers(self):
    subscriber_threads = []
    for i in range(1, NUM_SUBSCRIBERS + 1):
        subscriber = DeviceSubscriber(...)
        thread = threading.Thread(target=subscriber.run, daemon=True)
        subscriber_threads.append(thread)
        thread.start()
    # ...
```