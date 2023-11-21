#include <SPI.h>
#include <MFRC522.h>
#include <WiFi.h>
#include <ESPmDNS.h>
#include <WiFiUdp.h>
#include <ArduinoOTA.h>
#include <ESP32Servo.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>

const char* ssid = "A.T.O.M_Labs";
const char* password = "atom281121";
//const char* ssid = "HRHK";
//const char* password = "Ha9868598102@";
const char* serverIP = "192.168.0.8";

constexpr uint8_t RST_PIN = 5;
constexpr uint8_t SS_PIN = 26;

MFRC522 mfrc522(SS_PIN, RST_PIN);
MFRC522::MIFARE_Key key;
MFRC522::StatusCode status;
WiFiClient client;

int blockNum = 2;
byte bufferLen = 18;
byte readBlockData[18];
byte blockData[16] = { "Name" };
String StringVariable;
String myurl = "/";
String line = "";

#define i2c_Address 0x3c 
#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels
#define OLED_RESET -1 
Adafruit_SH1106G display(128, 64, &Wire, -1);

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.println("Connection Failed! Rebooting...");
    delay(5000);
    ESP.restart();
  }

  // Initialize other components here
   ArduinoOTA
    .onStart([]() {
      String type;
      if (ArduinoOTA.getCommand() == U_FLASH)
        type = "sketch";
      else // U_SPIFFS
        type = "filesystem";

      // NOTE: if updating SPIFFS this would be the place to unmount SPIFFS using SPIFFS.end()
      Serial.println("Start updating " + type);
    })
    .onEnd([]() {
      Serial.println("\nEnd");
    })
    .onProgress([](unsigned int progress, unsigned int total) {
      Serial.printf("Progress: %u%%\r", (progress / (total / 100)));
    })
    .onError([](ota_error_t error) {
      Serial.printf("Error[%u]: ", error);
      if (error == OTA_AUTH_ERROR) Serial.println("Auth Failed");
      else if (error == OTA_BEGIN_ERROR) Serial.println("Begin Failed");
      else if (error == OTA_CONNECT_ERROR) Serial.println("Connect Failed");
      else if (error == OTA_RECEIVE_ERROR) Serial.println("Receive Failed");
      else if (error == OTA_END_ERROR) Serial.println("End Failed");
    });
  ArduinoOTA.begin();
  Serial.println("Ready");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  SPI.begin();
  mfrc522.PCD_Init();
  if (!display.begin(i2c_Address, true)) {
    Serial.println(F("SSD1306 allocation failed"));
    for (;;)
      ;
  }
  display.clearDisplay();
  pinMode(13, OUTPUT);
}

void loop() {
  ArduinoOTA.handle();
  StringVariable = "";
  int ch = 0;
  
  // Your main loop logic here
  digitalWrite(13, LOW);
  display.setTextSize(2);
  display.setTextColor(SH110X_WHITE);;
  display.setCursor(25, 0);
  display.println(F("A.T.O.M"));
  display.setCursor(20, 20);
  display.print(F("ROBOTICS"));
  display.setCursor(0, 45);
  display.setTextColor(SH110X_WHITE, SH110X_BLACK); 
  display.setCursor(0, 45);
  display.print(F(" Tap Card "));
  display.display();
  for (byte i = 0; i < 6; i++) {
    key.keyByte[i] = 0xFF;
  }
  if (!mfrc522.PICC_IsNewCardPresent()) {
    return;
  }
  if (!mfrc522.PICC_ReadCardSerial()) {
    return;
  }
   ReadDataFromBlock(blockNum, readBlockData);
  for (int j = 0; j < 16; j++) {
    StringVariable = StringVariable + String((char)readBlockData[j]);
    Serial.write(readBlockData[j]);
  }
  if (client.connect(serverIP, 8080)) {
    String m = IotClientSendWithAnswer(serverIP, "Done");
    if (m != "NULL" && m != "Client Timeout!") {
      m.getBytes(blockData, 16);
      display.setCursor(0, 45);
        display.setTextColor(SH110X_WHITE, SH110X_BLACK); 
      display.setCursor(24, 45);  // Start at top-left corner
      display.print(F("Issuing"));
      display.display();
      delay(500);
      Serial.println("Writing to Data Block...");
      WriteDataToBlock(blockNum, blockData);
      ch = 1;
    }
  }
  if (ch != 1) {
    if (client.connect(serverIP, 8000)) {
      display.setCursor(0, 45);
        display.setTextColor(SH110X_WHITE, SH110X_BLACK); 
      display.setCursor(0, 45);  // Start at top-left corner
      display.print(F(" Checking"));
      display.display();
      String m = IotClientSendWithAnswer(serverIP, StringVariable);
      if (m == "Marked") {
        digitalWrite(13,HIGH);
        display.setCursor(0, 45);
          display.setTextColor(SH110X_WHITE, SH110X_BLACK); 
        display.setCursor(0, 45);  // Start at top-left corner
//        display.print(F("Member"));
        display.print(F(" Door Open"));
        display.display();
        delay(500);
      } else if (m == "NotMarked") {
        display.setCursor(0, 45);
          display.setTextColor(SH110X_WHITE, SH110X_BLACK); 
        display.setCursor(0, 45);  // Start at top-left corner
        display.print(F("Not Member"));
        display.display();
        delay(500);
      }
    }
  }

  delay(1000);
  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();// Consider replacing with non-blocking techniques
}

void ReadDataFromBlock(int blockNum, byte readBlockData[]) {
  // Read data from block
  status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, blockNum, &key, &(mfrc522.uid));
  if (status != MFRC522::STATUS_OK) {
    return;
  }
  status = mfrc522.MIFARE_Read(blockNum, readBlockData, &bufferLen);
  if (status != MFRC522::STATUS_OK) {
    return;
  }
}

void WriteDataToBlock(int blockNum, byte blockData[]) {
  // Write data to block
  status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, blockNum, &key, &(mfrc522.uid));
  if (status != MFRC522::STATUS_OK) {
    Serial.print("Authentication failed for Write: ");
    return;
  }
  status = mfrc522.MIFARE_Write(blockNum, blockData, 16);
  if (status != MFRC522::STATUS_OK) {
    return;
  }
  display.setCursor(0, 40);
    display.setTextColor(SH110X_WHITE, SH110X_BLACK); ;
  display.setCursor(0, 40);  // Start at top-left corner
  display.print(F("   Issued "));
  display.display();
  delay(500);
  digitalWrite(27, HIGH);
}

String IotClientSendWithAnswer(String IPcache,String monmessagecache) {
  // Send HTTP GET request and return the response
  line = "";
  client.print(String("GET ") + myurl + monmessagecache + " HTTP/1.1\r\n" + "Host: " + IPcache + "\r\n" + "Connection: close\r\n\r\n");
  unsigned long timeout = millis();
  while (client.available() == 0) {
    if (millis() - timeout > 1000) {
      return "Client Timeout!";
    }
  }
  while (client.available()) {
    line += client.readStringUntil('\r');
  }
  return line;
}
