/*
 * BÀI 5A: ESP32 HTTP GET REQUEST
 * Gửi dữ liệu nhiệt độ/độ ẩm qua URL parameters
 * Server: https://postman-echo.com/get
 */

#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>
#include <WiFi.h>
#include <HTTPClient.h>

// --- Định nghĩa chân kết nối ---
#define DHT_PIN 15
#define LED_PIN 2
#define DHT_TYPE DHT22

// --- Khởi tạo đối tượng ---
DHT dht(DHT_PIN, DHT_TYPE);
LiquidCrystal_I2C lcd(0x27, 16, 2);

// --- Cấu hình WiFi và Server ---
const char* ssid = "Wokwi-GUEST";
const char* password = "";
String serverName = "https://postman-echo.com/get";

// --- Biến toàn cục ---
unsigned long previousMillis = 0;
const long interval = 5000; // Gửi dữ liệu mỗi 5 giây

void setup() {
  // Khởi động Serial
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n=== BÀI 5A: HTTP GET REQUEST ===");
  
  // Cấu hình LED
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  
  // Khởi động LCD
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("HTTP GET Demo");
  lcd.setCursor(0, 1);
  lcd.print("Connecting WiFi");
  
  // Khởi động DHT
  dht.begin();
  
  // Kết nối WiFi
  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password, 6);
  
  int wifiAttempts = 0;
  while (WiFi.status() != WL_CONNECTED && wifiAttempts < 20) {
    delay(500);
    Serial.print(".");
    digitalWrite(LED_PIN, !digitalRead(LED_PIN)); // Nhấp nháy LED
    wifiAttempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    digitalWrite(LED_PIN, HIGH);
    Serial.println("\nWiFi Connected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
    
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("WiFi Connected!");
    lcd.setCursor(0, 1);
    lcd.print(WiFi.localIP());
    delay(2000);
  } else {
    Serial.println("\nWiFi Connection Failed!");
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("WiFi Failed!");
    while(1) { delay(1000); } // Dừng chương trình
  }
}

void loop() {
  unsigned long currentMillis = millis();
  
  // Gửi dữ liệu mỗi 5 giây
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    
    if (WiFi.status() == WL_CONNECTED) {
      // Đọc cảm biến
      float temperature = dht.readTemperature();
      float humidity = dht.readHumidity();
      
      // Kiểm tra lỗi
      if (isnan(temperature) || isnan(humidity)) {
        Serial.println("DHT22 Sensor Error!");
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Sensor Error!");
        return;
      }
      
      // Hiển thị lên LCD
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("T:");
      lcd.print(temperature, 1);
      lcd.print("C H:");
      lcd.print(humidity, 1);
      lcd.print("%");
      
      Serial.println("\n==========================================");
      Serial.println("SENSOR DATA");
      Serial.println("==========================================");
      Serial.print("Temperature: ");
      Serial.print(temperature, 2);
      Serial.println(" °C");
      Serial.print("Humidity: ");
      Serial.print(humidity, 2);
      Serial.println(" %");
      
      // Tạo HTTP GET request
      HTTPClient http;
      String serverPath = serverName + "?temp=" + String(temperature, 2) + "&humid=" + String(humidity, 2);
      
      Serial.println("\nSENDING HTTP GET REQUEST");
      Serial.println("==========================================");
      Serial.print("URL: ");
      Serial.println(serverPath);
      
      lcd.setCursor(0, 1);
      lcd.print("Sending GET...  ");
      
      http.begin(serverPath.c_str());
      int httpResponseCode = http.GET();
      
      if (httpResponseCode > 0) {
        Serial.println("\nREQUEST SUCCESSFUL!");
        Serial.print("Response Code: ");
        Serial.println(httpResponseCode);
        
        lcd.setCursor(0, 1);
        lcd.print("GET OK! ");
        lcd.print(httpResponseCode);
        
        String payload = http.getString();
        Serial.println("\nRESPONSE PAYLOAD:");
        Serial.println("------------------------------------------");
        Serial.println(payload);
        Serial.println("------------------------------------------");
        
        // Nhấp nháy LED khi thành công
        for(int i = 0; i < 3; i++) {
          digitalWrite(LED_PIN, LOW);
          delay(150);
          digitalWrite(LED_PIN, HIGH);
          delay(150);
        }
      } else {
        Serial.println("\nREQUEST FAILED!");
        Serial.print("Error Code: ");
        Serial.println(httpResponseCode);
        Serial.print("Error: ");
        Serial.println(http.errorToString(httpResponseCode));
        
        lcd.setCursor(0, 1);
        lcd.print("Error: ");
        lcd.print(httpResponseCode);
      }
      
      http.end();
      Serial.println("==========================================\n");
      
    } else {
      Serial.println("WiFi Disconnected!");
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("WiFi Lost!");
      digitalWrite(LED_PIN, LOW);
    }
  }
}