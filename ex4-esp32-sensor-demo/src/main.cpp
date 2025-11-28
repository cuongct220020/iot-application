#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>

// --- Định nghĩa chân kết nối (Hardware Mapping) ---
#define DHT_PIN 15      // Chân tín hiệu của cảm biến nhiệt độ/độ ẩm
#define PIR_PIN 12      // Chân tín hiệu của cảm biến chuyển động
#define LED_PIN 18      // Chân điều khiển đèn LED (Lưu ý: Đảm bảo nối đúng chân này trên mạch)
#define DHT_TYPE DHT22  // Định nghĩa loại cảm biến là DHT22

// --- Khởi tạo đối tượng ---
DHT dht(DHT_PIN, DHT_TYPE);
LiquidCrystal_I2C lcd(0x27, 16, 2); // Địa chỉ I2C 0x27, màn hình 16 cột 2 dòng

// --- Biến toàn cục ---
unsigned long previousMillis = 0; // Biến lưu thời gian để thay thế delay()
const long interval = 2000;       // Chu kỳ đọc cảm biến DHT (2000ms = 2 giây)
int motionState = 0;              // Biến lưu trạng thái hiện tại của PIR
int lastMotionState = 0;          // Biến lưu trạng thái cũ của PIR để so sánh

void setup() {
  // 1. Khởi động Serial để debug lỗi
  Serial.begin(115200);
  Serial.println("Hello, ESP32!");

  // 2. Cấu hình chế độ Input/Output cho các chân
  pinMode(PIR_PIN, INPUT);    // Cảm biến PIR là đầu vào
  pinMode(LED_PIN, OUTPUT);   // Đèn LED là đầu ra
  digitalWrite(LED_PIN, LOW); // Đảm bảo đèn tắt khi mới khởi động
  
  // 3. Khởi động cảm biến DHT
  dht.begin();
  
  // 4. Khởi động màn hình LCD
  lcd.init();
  lcd.backlight(); // Bật đèn nền
  lcd.clear();     // Xóa nội dung cũ
  
  // Hiển thị thông báo chào mừng
  lcd.setCursor(0, 0);
  lcd.print("  ESP32 System  ");
  lcd.setCursor(0, 1);
  lcd.print(" Initializing...");
  
  delay(2000); // Chờ 2s để người dùng kịp đọc thông báo
  lcd.clear();
}

void loop() {

  // --- PHẦN 1: Đọc cảm biến DHT22 (Sử dụng millis để không chặn chương trình) ---
  unsigned long currentMillis = millis(); // Lấy thời gian hiện tại của hệ thống
  
  // Kiểm tra nếu đã trôi qua 2000ms (2 giây) thì mới đọc dữ liệu
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis; // Cập nhật lại mốc thời gian
    
    // Đọc độ ẩm và nhiệt độ
    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature();
    
    // Kiểm tra xem việc đọc có bị lỗi không (isnan = is not a number)
    if (isnan(humidity) || isnan(temperature)) {
      Serial.println("Lỗi đọc dữ liệu từ DHT22");
      lcd.setCursor(0, 0);
      lcd.print("DHT22 Error! ");
      lcd.setCursor(0, 1);
      lcd.print("Check Sensor ");
      return; // Thoát khỏi hàm loop hiện tại nếu lỗi
    }
    
    // Hiển thị dữ liệu lên LCD
    lcd.clear(); // Xóa màn hình trước khi in mới
    lcd.setCursor(0, 0);
    lcd.print("Temp: ");
    lcd.print(temperature, 1); // In với 1 chữ số thập phân
    lcd.print((char)223);      // In ký tự độ (°) bằng mã ASCII
    lcd.print("C");
    
    lcd.setCursor(0, 1);
    lcd.print("Humidity: ");
    lcd.print(humidity, 1);
    lcd.print("%");
    
    // In log ra Serial Monitor
    Serial.print("Nhiệt độ: ");
    Serial.print(temperature, 1);
    Serial.print("°C | Độ ẩm: ");
    Serial.print(humidity, 1);
    Serial.println("%");
  }
  

  // --- PHẦN 2: Đọc cảm biến PIR (Xử lý thời gian thực) ---
  motionState = digitalRead(PIR_PIN);
  
  // So sánh trạng thái hiện tại với trạng thái cũ (State Change Detection)
  // Chỉ thực hiện lệnh khi có sự THAY ĐỔI trạng thái (từ Không->Có hoặc Có->Không)
  if (motionState != lastMotionState) {
    if (motionState == HIGH) {
      // Phát hiện chuyển động
      digitalWrite(LED_PIN, HIGH);
      Serial.println("Phát hiện chuyển động. LED ON");
    } else {
      // Chuyển động kết thúc
      digitalWrite(LED_PIN, LOW);
      Serial.println("Không có chuyển động. LED OFF");
    }
    
    // Cập nhật trạng thái cũ thành trạng thái hiện tại cho vòng lặp sau
    lastMotionState = motionState;
  }
  
  delay(100); // Delay nhỏ giúp ổn định, tránh nhiễu tín hiệu
}