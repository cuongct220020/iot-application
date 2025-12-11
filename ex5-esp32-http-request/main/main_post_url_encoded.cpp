/*
 * BÀI 5B: ESP32 HTTP POST REQUEST - URL-ENCODED
 * Gửi dữ liệu nhiệt độ/độ ẩm qua POST body (application/x-www-form-urlencoded)
 * Server: https://postman-echo.com/post
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
String serverName = "https://postman-echo.com/post";

// --- Biến toàn cục ---
unsigned long previousMillis = 0;
const long interval = 5000;

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n=== BÀI 5B: HTTP POST REQUEST (URL-ENCODED) ===");
  
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("HTTP POST Demo");
  lcd.setCursor(0, 1);
  lcd.print("URL-Encoded");
  
  dht.begin();
  
  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password, 6);
  
  int wifiAttempts = 0;
  while (WiFi.status() != WL_CONNECTED && wifiAttempts < 20) {
    delay(500);
    Serial.print(".");
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
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
    delay(2000);
  } else {
    Serial.println("\nWiFi Connection Failed!");
    lcd.clear();
    lcd.print("WiFi Failed!");
    while(1) { delay(1000); }
  }
}

void loop() {
  unsigned long currentMillis = millis();
  
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    
    if (WiFi.status() == WL_CONNECTED) {
      float temperature = dht.readTemperature();
      float humidity = dht.readHumidity();
      
      if (isnan(temperature) || isnan(humidity)) {
        Serial.println("DHT22 Sensor Error!");
        lcd.clear();
        lcd.print("Sensor Error!");
        return;
      }
      
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
      
      // Tạo HTTP POST request với URL-encoded data
      HTTPClient http;
      http.begin(serverName);
      http.addHeader("Content-Type", "application/x-www-form-urlencoded");
      
      String httpRequestData = "temp=" + String(temperature, 2) + "&humid=" + String(humidity, 2);
      
      Serial.println("\n SENDING HTTP POST REQUEST");
      Serial.println("==========================================");
      Serial.println("Content-Type: application/x-www-form-urlencoded");
      Serial.print("Request Data: ");
      Serial.println(httpRequestData);
      
      lcd.setCursor(0, 1);
      lcd.print("POST sending... ");
      
      int httpResponseCode = http.POST(httpRequestData);
      
      if (httpResponseCode > 0) {
        Serial.println("\n REQUEST SUCCESSFUL!");
        Serial.print("Response Code: ");
        Serial.println(httpResponseCode);
        
        lcd.setCursor(0, 1);
        lcd.print("POST OK! ");
        lcd.print(httpResponseCode);
        
        String payload = http.getString();
        Serial.println("\n RESPONSE PAYLOAD:");
        Serial.println("------------------------------------------");
        Serial.println(payload);
        Serial.println("------------------------------------------");
        
        // Nhấp nháy LED
        for(int i = 0; i < 3; i++) {
          digitalWrite(LED_PIN, LOW);
          delay(150);
          digitalWrite(LED_PIN, HIGH);
          delay(150);
        }
      } else {
        Serial.println("\n REQUEST FAILED!");
        Serial.print("Error Code: ");
        Serial.println(httpResponseCode);
        
        lcd.setCursor(0, 1);
        lcd.print("Error: ");
        lcd.print(httpResponseCode);
      }
      
      http.end();
      Serial.println("==========================================\n");
      
    } else {
      Serial.println("WiFi Disconnected!");
      lcd.clear();
      lcd.print("WiFi Lost!");
      digitalWrite(LED_PIN, LOW);
    }
  }
}