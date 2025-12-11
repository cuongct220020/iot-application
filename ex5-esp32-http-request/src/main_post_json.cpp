/*
 * BÀI 5C: ESP32 HTTP POST REQUEST - JSON FORMAT
 * Gửi dữ liệu nhiệt độ/độ ẩm dạng JSON qua POST body
 * Server: https://postman-echo.com/post
 */

#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

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
  Serial.println("\n=== BÀI 5C: HTTP POST REQUEST (JSON) ===");
  
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("HTTP POST Demo");
  lcd.setCursor(0, 1);
  lcd.print("JSON Format");
  
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
      
      // Tạo JSON sử dụng ArduinoJson
      DynamicJsonDocument doc(1024);
      JsonObject root = doc.to<JsonObject>();
      root["temperature"] = temperature;
      root["humidity"] = humidity;
      root["device"] = "ESP32";
      root["sensor"] = "DHT22";
      root["location"] = "Hanoi, Vietnam";
      root["timestamp"] = millis() / 1000; // Thời gian tính bằng giây
      
      String httpRequestData;
      serializeJson(doc, httpRequestData);
      
      // Tạo HTTP POST request với JSON
      HTTPClient http;
      http.begin(serverName);
      http.addHeader("Content-Type", "application/json");
      
      Serial.println("\nSENDING HTTP POST REQUEST (JSON)");
      Serial.println("==========================================");
      Serial.println("Content-Type: application/json");
      Serial.print("JSON Data: ");
      Serial.println(httpRequestData);
      
      // In JSON đẹp hơn
      Serial.println("\nFormatted JSON:");
      serializeJsonPretty(doc, Serial);
      Serial.println();
      
      lcd.setCursor(0, 1);
      lcd.print("JSON sending... ");
      
      int httpResponseCode = http.POST(httpRequestData);
      
      if (httpResponseCode > 0) {
        Serial.println("\nREQUEST SUCCESSFUL!");
        Serial.print("Response Code: ");
        Serial.println(httpResponseCode);
        
        lcd.setCursor(0, 1);
        lcd.print("JSON OK! ");
        lcd.print(httpResponseCode);
        
        String payload = http.getString();
        Serial.println("\nRESPONSE PAYLOAD:");
        Serial.println("------------------------------------------");
        Serial.println(payload);
        Serial.println("------------------------------------------");
        
        // Parse response JSON
        DynamicJsonDocument responseDoc(2048);
        DeserializationError error = deserializeJson(responseDoc, payload);
        
        if (!error) {
          Serial.println("\nPARSED RESPONSE DATA:");
          Serial.println("------------------------------------------");
          Serial.print("Echo Temperature: ");
          Serial.println(responseDoc["data"]["temperature"].as<float>(), 2);
          Serial.print("Echo Humidity: ");
          Serial.println(responseDoc["data"]["humidity"].as<float>(), 2);
          Serial.print("Echo Device: ");
          Serial.println(responseDoc["data"]["device"].as<String>());
          Serial.print("Echo Location: ");
          Serial.println(responseDoc["data"]["location"].as<String>());
          Serial.println("------------------------------------------");
        } else {
          Serial.println("Failed to parse JSON response");
        }
        
        // Nhấp nháy LED
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