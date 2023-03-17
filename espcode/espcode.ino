#include <SPI.h>
#include <MFRC522.h>
#include <WiFi.h>
#include <ESP32Servo.h>
#include <LiquidCrystal_I2C.h>
int lcdColumns = 16;
int lcdRows = 2;
LiquidCrystal_I2C lcd(0x27, lcdColumns, lcdRows);  
Servo myservo;
int pos = 0;   
long  i;
String  StringVariable;
WiFiClient client;
String myurl = "/";
String line = "";
String IotClientSendWithAnswer(String IPcache, String monmessagecache) {
  line = "";
  client.print(String("GET ") + myurl + monmessagecache + " HTTP/1.1\r\n" +
               "Host: " + IPcache + "\r\n" +
               "Connection: close\r\n\r\n");
  unsigned long timeout = millis();
  while (client.available() == 0) {
    if (millis() - timeout > 1000) {
      return "Client Timeout!";
    }
  }
  while(client.available()) {line += client.readStringUntil('\r');}
  return line;
}
constexpr uint8_t RST_PIN = 5;    
constexpr uint8_t SS_PIN = 26;     
MFRC522 mfrc522(SS_PIN, RST_PIN); 
MFRC522::MIFARE_Key key;
String name;
int blockNum = 2;
byte bufferLen = 18;
byte readBlockData[18];
byte blockData[16] = { "Name" };
MFRC522::StatusCode status;

void setup()
{ pinMode(4,OUTPUT);//yellow
  pinMode(2,OUTPUT);//red
  pinMode(27,OUTPUT);//blue
  pinMode(15,OUTPUT);//green
  myservo.attach(13);
  lcd.init();                     
  lcd.backlight();
  StringVariable = "";
  Serial.begin(9600);
  WiFi.begin("A.T.O.M_LABS", "Atom281121");
//  WiFi.begin("HRHK", "Ha9868598102@");
  while ((!(WiFi.status() == WL_CONNECTED))) {
  }
  SPI.begin();
  mfrc522.PCD_Init();
}

void loop()
{ StringVariable = "";
  digitalWrite(27,LOW);
  digitalWrite(2,LOW);
  digitalWrite(4,HIGH);
  digitalWrite(15,LOW);
  myservo.write(0);  
  lcd.clear(); 
  lcd.setCursor(0, 0);
  lcd.print("Atom Labs");      
  for (byte i = 0; i < 6; i++)
  {
    key.keyByte[i] = 0xFF;
  }
  if ( ! mfrc522.PICC_IsNewCardPresent())
  {
    return;
  }
  if ( ! mfrc522.PICC_ReadCardSerial())
  {
    return;
  }
//  digitalWrite(4,LOW);
  digitalWrite(15,LOW);
  ReadDataFromBlock(blockNum, readBlockData);
  for (int j = 0 ; j < 16 ; j++)
  { StringVariable = StringVariable + String((char)readBlockData[j]);
    Serial.write(readBlockData[j]);
  }
  if (client.connect("192.168.0.132", 8000)) {
    String m=IotClientSendWithAnswer("192.168.0.132", StringVariable);
    if (m=="Marked"){  
    digitalWrite(15,HIGH);
    myservo.write(90); 
    lcd.setCursor(0, 1);
    lcd.print("Marked ");             
    delay(1000);
  }
  else if(m=="NotMarked"){
    digitalWrite(2,HIGH); 
    lcd.setCursor(0, 1);
    lcd.print("Not Marked");
    delay(1000);
    }
  }
  if (client.connect("192.168.0.132", 8080)) {
      String m=IotClientSendWithAnswer("192.168.0.132","Done");
      if (m!="NULL" && m!="Client Timeout!"){
    m.getBytes(blockData, 16);
    Serial.println("Writing to Data Block...");
    WriteDataToBlock(blockNum, blockData);
    loop();}
    }
  delay(1000);
  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();
}
void ReadDataFromBlock(int blockNum, byte readBlockData[])
{
    lcd.setCursor(0, 1);
    lcd.print("Reading"); 
  status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, blockNum, &key, &(mfrc522.uid));
  if (status != MFRC522::STATUS_OK)
  {
    return;
  }
  status = mfrc522.MIFARE_Read(blockNum, readBlockData, &bufferLen);
  if (status != MFRC522::STATUS_OK)
  {
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
    lcd.setCursor(0, 1);
    lcd.print("Writing"); 
  digitalWrite(27,HIGH);
  delay(2000);
}