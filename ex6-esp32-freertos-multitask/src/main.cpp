/*
 * BÀI 7: ESP32 MULTI-TASKS WITH FREERTOS
 * Sinh viên: Đặng Tiến Cường - 20220020
 * 
 * Mô tả: Chương trình ESP32 sử dụng FreeRTOS với 3 task song song:
 * - Task 1: Nhấp nháy LED
 * - Task 2: Đọc dữ liệu từ cảm biến DHT22 và PIR
 * - Task 3: Gửi dữ liệu cảm biến lên server
 */

#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <ArduinoJson.h>

// ==================== CẤU HÌNH PHẦN CỨNG ====================
#define DHT_PIN 15        // Chân kết nối DHT22
#define DHT_TYPE DHT22    // Loại cảm biến DHT
#define LED_PIN 18        // LED external (theo diagram.json)
#define PIR_PIN 12        // Chân kết nối PIR Motion Sensor (theo diagram.json)

// ==================== CẤU HÌNH WIFI ====================
const char* ssid = "Wokwi-GUEST";      // Tên WiFi
const char* password = "";              // Mật khẩu WiFi (để trống cho Wokwi)

// ==================== CẤU HÌNH SERVER ====================
const char* serverURL = "https://postman-echo.com/post";

// ==================== KHỞI TẠO ĐỐI TƯỢNG ====================
DHT dht(DHT_PIN, DHT_TYPE);

// ==================== BIẾN CHIA SẺ GIỮA CÁC TASK ====================
// Sử dụng SemaphoreHandle_t để bảo vệ dữ liệu chia sẻ
SemaphoreHandle_t xSensorDataMutex;

// Cấu trúc dữ liệu cảm biến
struct SensorData {
  float temperature;
  float humidity;
  bool motionDetected;
  unsigned long timestamp;
  bool dataReady;
};

SensorData sensorData = {0, 0, false, 0, false};

// ==================== TASK 1: NHẤP NHÁY LED ====================
/*
 * Chức năng: Nhấp nháy LED onboard để báo hiệu hệ thống hoạt động
 * Chu kỳ: Bật 200ms, Tắt 800ms (nhấp nháy mỗi 1 giây)
 * Priority: 1 (Thấp nhất - không quan trọng)
 */
void TaskBlink(void *pvParameters) {
  (void) pvParameters;
  
  // Cấu hình LED_PIN là OUTPUT
  pinMode(LED_PIN, OUTPUT);
  
  Serial.println("[Task 1] LED Blink Task Started");
  
  for(;;) { // Vòng lặp vô hạn của FreeRTOS task
    digitalWrite(LED_PIN, HIGH);  // Bật LED
    Serial.println("[Task 1] LED ON");
    vTaskDelay(200 / portTICK_PERIOD_MS);  // Delay 200ms
    
    digitalWrite(LED_PIN, LOW);   // Tắt LED
    Serial.println("[Task 1] LED OFF");
    vTaskDelay(800 / portTICK_PERIOD_MS);  // Delay 800ms
  }
}

// ==================== TASK 2: ĐỌC DỮ LIỆU CẢM BIẾN ====================
/*
 * Chức năng: Đọc dữ liệu từ DHT22 (nhiệt độ, độ ẩm) và PIR (chuyển động)
 * Chu kỳ: Đọc mỗi 2 giây
 * Priority: 2 (Trung bình - quan trọng)
 */
void TaskSensorRead(void *pvParameters) {
  (void) pvParameters;
  
  // Cấu hình PIR_PIN là INPUT
  pinMode(PIR_PIN, INPUT);
  
  Serial.println("[Task 2] Sensor Read Task Started");
  
  for(;;) {
    // Đọc dữ liệu từ DHT22
    float temp = dht.readTemperature();
    float humid = dht.readHumidity();
    
    // Đọc trạng thái PIR (HIGH = có chuyển động)
    bool motion = digitalRead(PIR_PIN);
    
    // Kiểm tra lỗi đọc DHT22
    if (isnan(temp) || isnan(humid)) {
      Serial.println("[Task 2] ERROR: Failed to read from DHT sensor!");
      vTaskDelay(2000 / portTICK_PERIOD_MS);
      continue; // Bỏ qua vòng lặp này
    }
    
    // Lưu dữ liệu vào biến chia sẻ với bảo vệ Mutex
    if (xSemaphoreTake(xSensorDataMutex, portMAX_DELAY) == pdTRUE) {
      sensorData.temperature = temp;
      sensorData.humidity = humid;
      sensorData.motionDetected = motion;
      sensorData.timestamp = millis();
      sensorData.dataReady = true;
      
      xSemaphoreGive(xSensorDataMutex); // Giải phóng Mutex
    }
    
    // In thông tin ra Serial Monitor
    Serial.println("\n========================================");
    Serial.println("[Task 2] SENSOR DATA UPDATED");
    Serial.println("========================================");
    Serial.printf("Temperature: %.2f °C\n", temp);
    Serial.printf("Humidity: %.2f %%\n", humid);
    Serial.printf("Motion Detected: %s\n", motion ? "YES" : "NO");
    Serial.printf("Timestamp: %lu ms\n", millis());
    Serial.println("========================================\n");
    
    // Delay 2 giây trước khi đọc lại
    vTaskDelay(2000 / portTICK_PERIOD_MS);
  }
}

// ==================== TASK 3: GỬI DỮ LIỆU LÊN SERVER ====================
/*
 * Chức năng: Gửi dữ liệu cảm biến lên server qua HTTP POST (JSON)
 * Chu kỳ: Gửi mỗi 10 giây (nếu có dữ liệu mới)
 * Priority: 3 (Cao nhất - quan trọng nhất)
 */
void TaskSendingData(void *pvParameters) {
  (void) pvParameters;
  
  Serial.println("[Task 3] Data Sending Task Started");
  
  // Đợi WiFi kết nối xong
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("[Task 3] Waiting for WiFi connection...");
    vTaskDelay(1000 / portTICK_PERIOD_MS);
  }
  
  Serial.println("[Task 3] WiFi Connected! Ready to send data.");
  
  for(;;) {
    // Kiểm tra kết nối WiFi
    if (WiFi.status() != WL_CONNECTED) {
      Serial.println("[Task 3] ERROR: WiFi Disconnected!");
      vTaskDelay(5000 / portTICK_PERIOD_MS);
      continue;
    }
    
    // Lấy dữ liệu từ biến chia sẻ với bảo vệ Mutex
    SensorData localData;
    bool hasData = false;
    
    if (xSemaphoreTake(xSensorDataMutex, portMAX_DELAY) == pdTRUE) {
      if (sensorData.dataReady) {
        localData = sensorData;
        sensorData.dataReady = false; // Đánh dấu đã lấy
        hasData = true;
      }
      xSemaphoreGive(xSensorDataMutex);
    }
    
    // Nếu không có dữ liệu mới, chờ và thử lại
    if (!hasData) {
      Serial.println("[Task 3] No new data to send. Waiting...");
      vTaskDelay(10000 / portTICK_PERIOD_MS);
      continue;
    }
    
    // ===== TẠO JSON PAYLOAD =====
    DynamicJsonDocument doc(512);
    doc["temperature"] = localData.temperature;
    doc["humidity"] = localData.humidity;
    doc["motion"] = localData.motionDetected;
    doc["device"] = "ESP32";
    doc["sensor_temp_humid"] = "DHT22";
    doc["sensor_motion"] = "PIR_HC-SR501";
    doc["location"] = "Hanoi, Vietnam";
    doc["timestamp"] = localData.timestamp;
    
    String jsonPayload;
    serializeJson(doc, jsonPayload);
    
    // ===== GỬI HTTP POST REQUEST =====
    HTTPClient http;
    http.begin(serverURL);
    http.addHeader("Content-Type", "application/json");
    
    Serial.println("\n========================================");
    Serial.println("[Task 3] SENDING DATA TO SERVER");
    Serial.println("========================================");
    Serial.printf("URL: %s\n", serverURL);
    Serial.println("JSON Payload:");
    serializeJsonPretty(doc, Serial);
    Serial.println("\n========================================");
    
    int httpResponseCode = http.POST(jsonPayload);
    
    if (httpResponseCode > 0) {
      Serial.printf("\n[Task 3] ✓ REQUEST SUCCESSFUL! Response Code: %d\n", httpResponseCode);
      
      String response = http.getString();
      Serial.println("\n--- SERVER RESPONSE ---");
      Serial.println(response);
      Serial.println("--- END RESPONSE ---\n");
      
      // Parse response để verify
      DynamicJsonDocument responseDoc(1024);
      DeserializationError error = deserializeJson(responseDoc, response);
      
      if (!error) {
        Serial.println("[Task 3] ✓ Server echoed back our data:");
        Serial.printf("  - Temperature: %.2f °C\n", 
                     responseDoc["data"]["temperature"].as<float>());
        Serial.printf("  - Humidity: %.2f %%\n", 
                     responseDoc["data"]["humidity"].as<float>());
        Serial.printf("  - Motion: %s\n", 
                     responseDoc["data"]["motion"].as<bool>() ? "YES" : "NO");
      }
    } else {
      Serial.printf("\n[Task 3] ✗ REQUEST FAILED! Error Code: %d\n", httpResponseCode);
      Serial.printf("Error: %s\n", http.errorToString(httpResponseCode).c_str());
    }
    
    http.end();
    Serial.println("========================================\n");
    
    // Delay 10 giây trước khi gửi lần tiếp theo
    vTaskDelay(10000 / portTICK_PERIOD_MS);
  }
}

// ==================== SETUP ====================
void setup() {
  // Khởi động Serial Monitor
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("\n\n");
  Serial.println("========================================");
  Serial.println("  ESP32 FREERTOS MULTI-TASK SYSTEM");
  Serial.println("  Bài 7 - IoT Application");
  Serial.println("  Sinh viên: Đặng Tiến Cường - 20220020");
  Serial.println("========================================\n");
  
  // Khởi động cảm biến DHT
  dht.begin();
  Serial.println("[Setup] DHT22 Sensor initialized");
  
  // Kết nối WiFi
  Serial.print("[Setup] Connecting to WiFi");
  WiFi.begin(ssid, password, 6);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n[Setup] ✓ WiFi Connected!");
    Serial.print("[Setup] IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n[Setup] ✗ WiFi Connection Failed!");
    Serial.println("[Setup] System will continue without WiFi...");
  }
  
  // Tạo Mutex để bảo vệ dữ liệu chia sẻ
  xSensorDataMutex = xSemaphoreCreateMutex();
  if (xSensorDataMutex == NULL) {
    Serial.println("[Setup] ERROR: Failed to create Mutex!");
    while(1) { delay(1000); } // Dừng hệ thống
  }
  Serial.println("[Setup] ✓ Mutex created successfully");
  
  Serial.println("\n[Setup] Creating FreeRTOS Tasks...\n");
  
  // ===== TẠO TASK 1: BLINK LED =====
  xTaskCreate(
    TaskBlink,          // Hàm task
    "Task_Blink",       // Tên task (để debug)
    2048,               // Stack size (bytes)
    NULL,               // Tham số truyền vào task
    1,                  // Priority (1 = thấp)
    NULL                // Task handle (không cần)
  );
  Serial.println("[Setup] ✓ Task 1 (LED Blink) created - Priority: 1");
  
  // ===== TẠO TASK 2: ĐỌC CẢM BIẾN =====
  xTaskCreate(
    TaskSensorRead,
    "Task_SensorRead",
    4096,               // Stack lớn hơn vì xử lý nhiều
    NULL,
    2,                  // Priority: 2 (trung bình)
    NULL
  );
  Serial.println("[Setup] ✓ Task 2 (Sensor Read) created - Priority: 2");
  
  // ===== TẠO TASK 3: GỬI DỮ LIỆU =====
  xTaskCreate(
    TaskSendingData,
    "Task_SendData",
    8192,               // Stack lớn nhất vì dùng HTTP + JSON
    NULL,
    3,                  // Priority: 3 (cao nhất)
    NULL
  );
  Serial.println("[Setup] ✓ Task 3 (Send Data) created - Priority: 3");
  
  Serial.println("\n========================================");
  Serial.println("  ALL TASKS CREATED SUCCESSFULLY!");
  Serial.println("  System is now running...");
  Serial.println("========================================\n");
}

// ==================== LOOP ====================
void loop() {
  // Loop() để trống vì FreeRTOS scheduler sẽ quản lý các task
  // Có thể thêm code khác ở đây nếu cần (ví dụ: debug info)
  
  // In thông tin trạng thái mỗi 30 giây
  static unsigned long lastReport = 0;
  if (millis() - lastReport > 30000) {
    lastReport = millis();
    Serial.println("\n[Loop] System Status Report:");
    Serial.printf("  - Uptime: %lu seconds\n", millis() / 1000);
    Serial.printf("  - Free Heap: %u bytes\n", ESP.getFreeHeap());
    Serial.printf("  - WiFi Status: %s\n", 
                 WiFi.status() == WL_CONNECTED ? "Connected" : "Disconnected");
    Serial.println();
  }
  
  vTaskDelay(1000 / portTICK_PERIOD_MS); // Delay 1 giây
}