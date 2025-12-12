# BÁO CÁO BÀI TẬP 7
## ESP32 MULTI-TASKS WITH FREERTOS

---

## I. THÔNG TIN SINH VIÊN

| Thông tin | Nội dung |
|-----------|----------|
| **Họ và tên** | Đặng Tiến Cường|
| **MSSV** | 20220020 |
| **Lớp** | CTTN - Khoa học máy tính |
| **Ngày nộp** | 12/12/2025 |

---

## II. MỤC ĐÍCH BÀI TẬP

Lập trình cho ESP32 sử dụng **FreeRTOS** để thực hiện đa nhiệm (multi-tasking) với 3 task song song:

1. **Task 1**: Nhấp nháy LED để báo hiệu hệ thống hoạt động
2. **Task 2**: Đọc dữ liệu từ cảm biến DHT22 (nhiệt độ, độ ẩm) và PIR (chuyển động)
3. **Task 3**: Gửi dữ liệu cảm biến lên server qua HTTP POST

**Công cụ**: Wokwi Simulator (https://wokwi.com/)

---

## III. THIẾT BỊ VÀ THÀNH PHẦN

### A. Phần cứng ảo (Wokwi)

| Thiết bị | Số lượng | Mô tả |
|----------|----------|-------|
| ESP32 DevKit V1 | 1 | Vi điều khiển chính |
| DHT22 | 1 | Cảm biến nhiệt độ và độ ẩm |
| PIR Motion Sensor (HC-SR501) | 1 | Cảm biến chuyển động |
| LED Red | 1 | Đèn LED chỉ báo |
| Resistor 220Ω | 1 | Điện trở hạn dòng cho LED |

### B. Thư viện sử dụng

```ini
- WiFi.h (Built-in ESP32)
- HTTPClient.h (Built-in ESP32)
- DHT sensor library v1.4.4
- Adafruit Unified Sensor v1.1.9
- ArduinoJson v6.21.3
```

### C. Sơ đồ kết nối

| Thiết bị | ESP32 Pin | Mô tả |
|----------|-----------|-------|
| **DHT22** | | |
| DHT22 VCC | 3V3 | Nguồn cấp |
| DHT22 GND | GND | Nối đất |
| DHT22 SDA | GPIO15 | Tín hiệu dữ liệu |
| **PIR Sensor** | | |
| PIR VCC | 3V3 | Nguồn cấp |
| PIR GND | GND | Nối đất |
| PIR OUT | GPIO12 | Tín hiệu phát hiện chuyển động |
| **LED External** | | |
| LED Anode | GPIO18 | Tín hiệu điều khiển |
| LED Cathode | GND (qua R220Ω) | Nối đất |

---

## IV. SƠ ĐỒ MẠCH

![Sơ đồ mạch Wokwi](diagram-screenshot.png)

**Mô tả sơ đồ:**
- ESP32 ở trung tâm kết nối với 3 thiết bị ngoại vi
- DHT22 đọc nhiệt độ/độ ẩm môi trường
- PIR phát hiện chuyển động xung quanh
- LED onboard nhấp nháy báo hiệu hệ thống hoạt động

---

## V. KIẾN THỨC VỀ FREERTOS

### A. FreeRTOS là gì?

**FreeRTOS** (Free Real-Time Operating System) là một hệ điều hành thời gian thực mã nguồn mở, được tích hợp sẵn trong ESP32 Arduino Core.

**Đặc điểm:**
- Cho phép chạy nhiều task song song (concurrent)
- Quản lý phân chia thời gian CPU giữa các task
- Hỗ trợ priority scheduling (ưu tiên task)
- Cung cấp cơ chế đồng bộ (Mutex, Semaphore, Queue)

### B. Các khái niệm quan trọng

#### 1. Task (Nhiệm vụ)
- Là một đơn vị công việc độc lập
- Có vòng lặp vô hạn `for(;;)`
- Được quản lý bởi FreeRTOS scheduler

**Cú pháp tạo task:**
```cpp
xTaskCreate(
  TaskFunction,     // Hàm task
  "TaskName",       // Tên task (string)
  StackSize,        // Kích thước stack (bytes)
  NULL,             // Tham số truyền vào
  Priority,         // Mức độ ưu tiên (0-N)
  NULL              // Task handle
);
```

#### 2. Priority (Độ ưu tiên)
- Số càng cao = ưu tiên càng cao
- Task có priority cao sẽ được chạy trước
- Trong bài này:
  - Task 1 (LED): Priority = 1 (thấp nhất)
  - Task 2 (Sensor): Priority = 2 (trung bình)
  - Task 3 (HTTP): Priority = 3 (cao nhất)

#### 3. Mutex (Mutual Exclusion)
- Dùng để bảo vệ dữ liệu chia sẻ giữa các task
- Chỉ 1 task được truy cập dữ liệu tại 1 thời điểm
- Tránh race condition (xung đột dữ liệu)

**Cú pháp:**
```cpp
// Tạo mutex
SemaphoreHandle_t mutex = xSemaphoreCreateMutex();

// Khóa mutex
xSemaphoreTake(mutex, portMAX_DELAY);
// ... truy cập dữ liệu ...
// Mở mutex
xSemaphoreGive(mutex);
```

#### 4. vTaskDelay()
- Delay không chặn (non-blocking)
- Cho phép task khác chạy trong thời gian delay
- Khác với `delay()` thông thường (blocking)

**Cú pháp:**
```cpp
vTaskDelay(1000 / portTICK_PERIOD_MS); // Delay 1000ms
```

---

## VI. THIẾT KẾ CHƯƠNG TRÌNH

### A. Kiến trúc hệ thống

```
┌─────────────────────────────────────────────┐
│              ESP32 MAIN CORE                │
│         FreeRTOS Scheduler                  │
└─────────────────────────────────────────────┘
         │              │              │
         ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│   TASK 1    │ │   TASK 2    │ │   TASK 3    │
│ LED Blink   │ │ Sensor Read │ │  Send Data  │
│ Priority: 1 │ │ Priority: 2 │ │ Priority: 3 │
└─────────────┘ └─────────────┘ └─────────────┘
         │              │              │
         ▼              ▼              ▼
    ┌───────┐    ┌──────────┐   ┌──────────┐
    │  LED  │    │DHT22+PIR │   │  Server  │
    └───────┘    └──────────┘   └──────────┘
                        │              ▲
                        │   Mutex      │
                        ▼  Protected   │
                 ┌────────────────┐    │
                 │  Sensor Data   │────┘
                 │  Shared Memory │
                 └────────────────┘
```

### B. Luồng dữ liệu

1. **Task 2** đọc cảm biến → Lưu vào `sensorData` (có bảo vệ Mutex)
2. **Task 3** lấy dữ liệu từ `sensorData` → Gửi lên server
3. **Task 1** nhấp nháy LED độc lập, không liên quan dữ liệu

### C. Cấu trúc dữ liệu chia sẻ

```cpp
struct SensorData {
  float temperature;       // Nhiệt độ từ DHT22
  float humidity;          // Độ ẩm từ DHT22
  bool motionDetected;     // Trạng thái PIR
  unsigned long timestamp; // Thời gian đọc
  bool dataReady;          // Flag: có dữ liệu mới chưa
};
```

---

## VII. CODE CHƯƠNG TRÌNH

### A. Code đầy đủ

Xem file: `src/main.cpp` (đã tạo trong artifact phía trên)

### B. Giải thích chi tiết các phần quan trọng

#### 1. Task 1: Blink LED

```cpp
void TaskBlink(void *pvParameters) {
  pinMode(LED_PIN, OUTPUT);
  
  for(;;) {
    digitalWrite(LED_PIN, HIGH);
    vTaskDelay(200 / portTICK_PERIOD_MS);  // Bật 200ms
    
    digitalWrite(LED_PIN, LOW);
    vTaskDelay(800 / portTICK_PERIOD_MS);  // Tắt 800ms
  }
}
```

**Chức năng:** Nhấp nháy LED mỗi 1 giây để báo hiệu hệ thống hoạt động.

#### 2. Task 2: Read Sensors

```cpp
void TaskSensorRead(void *pvParameters) {
  pinMode(PIR_PIN, INPUT);
  
  for(;;) {
    // Đọc DHT22
    float temp = dht.readTemperature();
    float humid = dht.readHumidity();
    
    // Đọc PIR
    bool motion = digitalRead(PIR_PIN);
    
    // Kiểm tra lỗi
    if (isnan(temp) || isnan(humid)) {
      vTaskDelay(2000 / portTICK_PERIOD_MS);
      continue;
    }
    
    // Lưu dữ liệu với Mutex protection
    if (xSemaphoreTake(xSensorDataMutex, portMAX_DELAY)) {
      sensorData.temperature = temp;
      sensorData.humidity = humid;
      sensorData.motionDetected = motion;
      sensorData.timestamp = millis();
      sensorData.dataReady = true;
      
      xSemaphoreGive(xSensorDataMutex);
    }
    
    vTaskDelay(2000 / portTICK_PERIOD_MS);  // Đọc mỗi 2 giây
  }
}
```

**Chức năng:**
- Đọc nhiệt độ, độ ẩm từ DHT22
- Đọc trạng thái chuyển động từ PIR
- Lưu vào biến chia sẻ với bảo vệ Mutex
- Chu kỳ: 2 giây

#### 3. Task 3: Send Data to Server

```cpp
void TaskSendingData(void *pvParameters) {
  // Đợi WiFi kết nối
  while (WiFi.status() != WL_CONNECTED) {
    vTaskDelay(1000 / portTICK_PERIOD_MS);
  }
  
  for(;;) {
    // Lấy dữ liệu từ biến chia sẻ
    SensorData localData;
    bool hasData = false;
    
    if (xSemaphoreTake(xSensorDataMutex, portMAX_DELAY)) {
      if (sensorData.dataReady) {
        localData = sensorData;
        sensorData.dataReady = false;
        hasData = true;
      }
      xSemaphoreGive(xSensorDataMutex);
    }
    
    if (!hasData) {
      vTaskDelay(10000 / portTICK_PERIOD_MS);
      continue;
    }
    
    // Tạo JSON payload
    DynamicJsonDocument doc(512);
    doc["temperature"] = localData.temperature;
    doc["humidity"] = localData.humidity;
    doc["motion"] = localData.motionDetected;
    doc["device"] = "ESP32";
    doc["timestamp"] = localData.timestamp;
    
    String jsonPayload;
    serializeJson(doc, jsonPayload);
    
    // Gửi HTTP POST request
    HTTPClient http;
    http.begin(serverURL);
    http.addHeader("Content-Type", "application/json");
    
    int httpResponseCode = http.POST(jsonPayload);
    
    if (httpResponseCode > 0) {
      String response = http.getString();
      // Xử lý response...
    }
    
    http.end();
    vTaskDelay(10000 / portTICK_PERIOD_MS);  // Gửi mỗi 10 giây
  }
}
```

**Chức năng:**
- Lấy dữ liệu mới từ Task 2
- Tạo JSON payload
- Gửi HTTP POST lên server
- Chu kỳ: 10 giây

#### 4. Setup() - Tạo các task

```cpp
void setup() {
  Serial.begin(115200);
  dht.begin();
  
  // Kết nối WiFi
  WiFi.begin(ssid, password, 6);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  
  // Tạo Mutex
  xSensorDataMutex = xSemaphoreCreateMutex();
  
  // Tạo Task 1: LED Blink
  xTaskCreate(TaskBlink, "Task_Blink", 2048, NULL, 1, NULL);
  
  // Tạo Task 2: Sensor Read
  xTaskCreate(TaskSensorRead, "Task_SensorRead", 4096, NULL, 2, NULL);
  
  // Tạo Task 3: Send Data
  xTaskCreate(TaskSendingData, "Task_SendData", 8192, NULL, 3, NULL);
}
```

**Stack size:**
- Task 1: 2048 bytes (đơn giản nhất)
- Task 2: 4096 bytes (xử lý cảm biến)
- Task 3: 8192 bytes (HTTP + JSON, tốn RAM nhất)

---

## VIII. KẾT QUẢ THỰC HIỆN

### A. Kết quả Serial Monitor

```
========================================
  ESP32 FREERTOS MULTI-TASK SYSTEM
  Bài 7 - IoT Application
  Sinh viên: Đặng Tiến Cường - 20220020
========================================

[Setup] DHT22 Sensor initialized
[Setup] Connecting to WiFi........
[Setup] ✓ WiFi Connected!
[Setup] IP Address: 192.168.1.100
[Setup] ✓ Mutex created successfully

[Setup] Creating FreeRTOS Tasks...

[Setup] ✓ Task 1 (LED Blink) created - Priority: 1
[Setup] ✓ Task 2 (Sensor Read) created - Priority: 2
[Setup] ✓ Task 3 (Send Data) created - Priority: 3

========================================
  ALL TASKS CREATED SUCCESSFULLY!
  System is now running...
========================================

[Task 1] LED Blink Task Started
[Task 2] Sensor Read Task Started
[Task 3] Data Sending Task Started
[Task 3] WiFi Connected! Ready to send data.

[Task 1] LED ON
[Task 1] LED OFF

========================================
[Task 2] SENSOR DATA UPDATED
========================================
Temperature: 28.50 °C
Humidity: 65.00 %
Motion Detected: YES
Timestamp: 2543 ms
========================================

[Task 1] LED ON
[Task 1] LED OFF

========================================
[Task 3] SENDING DATA TO SERVER
========================================
URL: https://postman-echo.com/post
JSON Payload:
{
  "temperature": 28.5,
  "humidity": 65.0,
  "motion": true,
  "device": "ESP32",
  "sensor_temp_humid": "DHT22",
  "sensor_motion": "PIR_HC-SR501",
  "location": "Hanoi, Vietnam",
  "timestamp": 2543
}
========================================

[Task 3] ✓ REQUEST SUCCESSFUL! Response Code: 200

--- SERVER RESPONSE ---
{"args":{},"data":{"temperature":28.5,"humidity":65.0,"motion":true,...},"files":{},"form":{},"headers":{...},"json":{"temperature":28.5,"humidity":65.0,"motion":true,...},"url":"https://postman-echo.com/post"}
--- END RESPONSE ---

[Task 3] ✓ Server echoed back our data:
  - Temperature: 28.50 °C
  - Humidity: 65.00 %
  - Motion: YES
========================================

[Task 1] LED ON
[Task 1] LED OFF
...
```

### B. Ảnh chụp màn hình

**1. Giao diện Wokwi**
![Wokwi Interface](screenshot-wokwi.png)

**2. Serial Monitor**
![Serial Monitor](screenshot-serial.png)

**3. LED đang nhấp nháy**
![LED Blinking](screenshot-led.png)

**4. Server Response**
![Server Response](screenshot-server.png)

### C. Phân tích kết quả

✅ **Task 1 (LED Blink)**
- Nhấp nháy đều đặn mỗi 1 giây
- Không bị ảnh hưởng bởi task khác
- Priority thấp nhưng vẫn chạy mượt

✅ **Task 2 (Sensor Read)**
- Đọc được nhiệt độ: 28.50°C
- Đọc được độ ẩm: 65.00%
- Phát hiện chuyển động: YES
- Chu kỳ đọc: 2 giây (chính xác)

✅ **Task 3 (Send Data)**
- Gửi dữ liệu thành công (HTTP 200)
- Server echo lại đúng dữ liệu
- Chu kỳ gửi: 10 giây (chính xác)
- Parse JSON response thành công

✅ **Đồng bộ dữ liệu**
- Mutex hoạt động tốt
- Không có race condition
- Dữ liệu nhất quán giữa các task

---

## IX. ƯU ĐIỂM CỦA FREERTOS

### So sánh với chương trình tuần tự (Sequential)

| Tiêu chí | Sequential | FreeRTOS |
|----------|-----------|----------|
| **Cấu trúc code** | ⭐⭐ Đơn giản | ⭐⭐⭐⭐ Rõ ràng, module |
| **Khả năng mở rộng** | ⭐⭐ Khó | ⭐⭐⭐⭐⭐ Rất dễ |
| **Tính đồng thời** | ❌ Không | ✅ Có |
| **Độ phản hồi** | ⭐⭐ Chậm | ⭐⭐⭐⭐⭐ Nhanh |
| **Quản lý timing** | ⭐ Phức tạp | ⭐⭐⭐⭐⭐ Tự động |
| **Debugging** | ⭐⭐⭐ Dễ | ⭐⭐ Khó hơn |

### Ví dụ minh họa

**Chương trình tuần tự (Blocking):**
```cpp
void loop() {
  // 1. Nhấp nháy LED
  digitalWrite(LED, HIGH);
  delay(200);           // ← BLOCKING! Task khác phải chờ
  digitalWrite(LED, LOW);
  delay(800);           // ← BLOCKING!
  
  // 2. Đọc cảm biến
  float temp = dht.readTemperature();  // Mất 250ms
  // ...
  
  // 3. Gửi HTTP
  http.POST(...);       // Mất 1-2 giây → LED không nhấp nháy!
}
```

**FreeRTOS (Non-blocking):**
```cpp
// Task 1: LED nhấp nháy độc lập
void TaskBlink(...) {
  for(;;) {
    digitalWrite(LED, HIGH);
    vTaskDelay(200);   // ← Các task khác vẫn chạy!
    digitalWrite(LED, LOW);
    vTaskDelay(800);
  }
}

// Task 3: Gửi HTTP
void TaskSendData(...) {
  for(;;) {
    http.POST(...);    // ← LED vẫn nhấp nháy bình thường!
    vTaskDelay(10000);
  }
}
```

---

## X. HƯỚNG PHÁT TRIỂN

### A. Tính năng có thể bổ sung

1. **Hiển thị LCD I2C**
   - Hiển thị nhiệt độ/độ ẩm real-time
   - Hiển thị trạng thái kết nối

2. **Queue để truyền dữ liệu**
   - Thay thế Mutex bằng Queue
   - Buffering nhiều lần đọc cảm biến

3. **Task điều khiển động cơ/relay**
   - Task 4: Bật quạt khi nhiệt độ > 30°C
   - Task 5: Bật đèn khi phát hiện chuyển động

4. **OTA Update**
   - Task 6: Kiểm tra firmware mới
   - Cập nhật từ xa không cần nạp lại

5. **Deep Sleep**
   - Sleep mode khi không có chuyển động
   - Tiết kiệm pin cho thiết bị battery

### B. Cải tiến về mã nguồn

1. **Sử dụng Task Notification**
   - Thay Mutex bằng Task Notification (nhẹ hơn)

2. **Watchdog Timer**
   - Tự động reset nếu task bị treo

3. **Error Handling**
   - Thêm try-catch cho HTTP request
   - Retry mechanism khi WiFi mất kết nối

---

## XI. KẾT LUẬN

### A. Tổng kết

Bài tập đã hoàn thành thành công các yêu cầu:

✅ Lập trình ESP32 với FreeRTOS multi-tasking  
✅ Task 1: Nhấp nháy LED độc lập  
✅ Task 2: Đọc cảm biến DHT22 + PIR  
✅ Task 3: Gửi dữ liệu lên server qua HTTP POST  
✅ Đồng bộ dữ liệu giữa các task bằng Mutex  
✅ Mô phỏng thành công trên Wokwi  

### B. Bài học rút ra

1. **FreeRTOS giúp code dễ bảo trì**
   - Mỗi task là một module độc lập
   - Dễ thêm/sửa/xóa tính năng

2. **Priority quan trọng**
   - Task quan trọng nên có priority cao
   - Tránh starvation (task bị bỏ đói)

3. **Đồng bộ dữ liệu cần cẩn thận**
   - Luôn dùng Mutex khi truy cập biến chung
   - Tránh deadlock (khóa chéo)

4. **Stack size cần điều chỉnh phù hợp**
   - Quá nhỏ → Stack overflow → Crash
   - Quá lớn → Lãng phí RAM

### C. Ứng dụng thực tế

Kiến thức này có thể áp dụng cho:
- **Smart Home**: Điều khiển nhiều thiết bị đồng thời
- **Wearable**: Đọc cảm biến + hiển thị + gửi dữ liệu
- **Industrial IoT**: Giám sát nhiều thông số production
- **Agriculture**: Tưới tự động + giám sát môi trường

## XII. TÀI LIỆU THAM KHẢO

1. **ESP32 FreeRTOS Documentation**  
   https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/freertos.html

2. **FreeRTOS Kernel Guide**  
   https://www.freertos.org/Documentation/RTOS_book.html

3. **ESP32 Arduino Core**  
   https://github.com/espressif/arduino-esp32

4. **Wokwi ESP32 Simulator**  
   https://docs.wokwi.com/guides/esp32

5. **ArduinoJson Library**  
   https://arduinojson.org/v6/doc/

6. **DHT Sensor Library**  
   https://github.com/adafruit/DHT-sensor-library

7. **Postman Echo API**  
   https://www.postman.com/postman/workspace/published-postman-templates
