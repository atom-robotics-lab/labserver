#include <SPI.h>
#include <MFRC522.h>
#include <WiFi.h>
#include <ESP32Servo.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

Servo myservo;
String name;
WiFiClient client;
String StringVariable;
constexpr uint8_t RST_PIN = 5;
constexpr uint8_t SS_PIN = 26;
MFRC522 mfrc522(SS_PIN, RST_PIN);
MFRC522::MIFARE_Key key;
MFRC522::StatusCode status;
int blockNum = 2;
byte bufferLen = 18;
byte readBlockData[18];
byte blockData[16] = { "Name" };
int pos = 0;
String myurl = "/";
String line = "";
#define SCREEN_WIDTH 128     // OLED display width, in pixels
#define SCREEN_HEIGHT 64     // OLED display height, in pixels
#define OLED_RESET -1        // Reset pin # (or -1 if sharing Arduino reset pin)
#define SCREEN_ADDRESS 0x3C  ///< See datasheet for Address; 0x3D for 128x64, 0x3C for 128x32
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

String IotClientSendWithAnswer(String IPcache, String monmessagecache) {
  line = "";
  client.print(String("GET ") + myurl + monmessagecache + " HTTP/1.1\r\n" + "Host: " + IPcache + "\r\n" + "Connection: close\r\n\r\n");
  unsigned long timeout = millis();
  while (client.available() == 0) {
    if (millis() - timeout > 1000) {
      return "Client Timeout!";
    }
  }
  while (client.available()) { line += client.readStringUntil('\r'); }
  return line;
}

void setup() {
  pinMode(4, OUTPUT);   //yellow
  pinMode(2, OUTPUT);   //red
  pinMode(27, OUTPUT);  //blue
  pinMode(15, OUTPUT);  //green
  myservo.attach(13);
  StringVariable = "";
  Serial.begin(115200);
  SPI.begin();
  mfrc522.PCD_Init();
  if (!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
    for (;;)
      ;
  }
  display.clearDisplay();
  // WiFi.begin("A.T.O.M_LABS", "Atom281121");
  WiFi.begin("HRHK", "Ha9868598102@");
  while ((!(WiFi.status() == WL_CONNECTED))) {}
}

void loop() {
  StringVariable = "";
  int ch = 0;
  digitalWrite(27, LOW);
  digitalWrite(2, LOW);
  digitalWrite(4, HIGH);
  digitalWrite(15, LOW);
  myservo.write(0);
  display.setTextSize(2);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(25, 0);
  display.println(F("A.T.O.M"));
  display.setCursor(20, 20);
  display.print(F("ROBOTICS"));
  display.setCursor(0, 40);
  display.setTextColor(WHITE, BLACK);
  display.setCursor(0, 40);
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
  //  digitalWrite(4,LOW);
  digitalWrite(15, LOW);
  ReadDataFromBlock(blockNum, readBlockData);
  for (int j = 0; j < 16; j++) {
    StringVariable = StringVariable + String((char)readBlockData[j]);
    Serial.write(readBlockData[j]);
  }
  if (client.connect("192.168.1.2", 8080)) {
    String m = IotClientSendWithAnswer("192.168.1.2", "Done");
    if (m != "NULL" && m != "Client Timeout!") {
      m.getBytes(blockData, 16);
      display.setCursor(0, 40);
      display.setTextColor(WHITE, BLACK);
      display.setCursor(0, 40);  // Start at top-left corner
      display.print(F("  Issuing "));
      display.display();
      delay(500);
      Serial.println("Writing to Data Block...");
      WriteDataToBlock(blockNum, blockData);
      ch = 1;
    }
  }
  if (ch != 1) {
    if (client.connect("192.168.1.2", 8000)) {

      display.setCursor(0, 40);
      display.setTextColor(WHITE, BLACK);
      display.setCursor(0, 40);  // Start at top-left corner
      display.print(F(" Checking "));
      display.display();
      String m = IotClientSendWithAnswer("192.168.1.2", StringVariable);
      if (m == "Marked") {
        digitalWrite(15, HIGH);
        myservo.write(90);
        display.setCursor(0, 40);
        display.setTextColor(WHITE, BLACK);
        display.setCursor(0, 40);  // Start at top-left corner
        display.print(F("   Member "));
        display.display();
        delay(500);
      } else if (m == "NotMarked") {
        digitalWrite(2, HIGH);
        display.setCursor(0, 40);
        display.setTextColor(WHITE, BLACK);
        display.setCursor(0, 40);  // Start at top-left corner
        display.print(F(" Not Member"));
        display.display();
        delay(500);
      }
    }
  }

  delay(1000);
  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();
}

void ReadDataFromBlock(int blockNum, byte readBlockData[]) {
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
  display.setTextColor(WHITE, BLACK);
  display.setCursor(0, 40);  // Start at top-left corner
  display.print(F("   Issued "));
  display.display();
  delay(500);
  digitalWrite(27, HIGH);
}