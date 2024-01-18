#include <CAN.h>
#include <MFRC522.h>
 
#define SS_PIN 8
#define RST_PIN 9
#define nCards 2

String tst[nCards] = {" aa bc da 81", " d9 c4 8d 9d"};
MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(9600);
  while (!Serial);

  Serial.println("CAN Sender");

  // start the CAN bus at 500 kbps
  if (!CAN.begin(500E3)) {
    Serial.println("Starting CAN failed!");
    while (1);
  }
  SPI.begin();
  mfrc522.PCD_Init();
}

void loop() {
  if (!mfrc522.PICC_IsNewCardPresent()) 
  {
    return;
  }
  // Select one of the cards
  if (!mfrc522.PICC_ReadCardSerial()) 
  {
    return;
  }
  // Serial.print("UID tag :");
  String content= "";
  byte letter;
  for (byte i = 0; i < mfrc522.uid.size; i++) 
  {
    // Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
    // Serial.print(mfrc522.uid.uidByte[i], HEX);
    content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
    content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  Serial.println(content);
  Serial.println(checkCard(content));

  if (checkCard(content)) {
    String txt = "";
    // char res = Serial.read();

    // Serial.print("res = ");
    // Serial.print(res);
    // Serial.println();

    txt.concat(random(3) + 1);
    txt.concat(' ');
    txt.concat(checkUser(content));

    // Serial.println(txt);

    CAN.beginPacket(0x12);
    for (int i=0; i<txt.length(); i++) {
      CAN.write((char)txt[i]);
      // Serial.println(content[i]);
    }
    CAN.endPacket();
    // Serial.println("msg set");
  }
  // Serial.println(content.length());
  // CAN.beginPacket(0x12);
  // for (int i=0; i<content.length(); i++) {
  //   CAN.write((char)content[i]);
  //   // Serial.println(content[i]);
  // }
  // // CAN.write('8');
  // CAN.endPacket();
  // Serial.println("done");

  // delay(1000);
  // Serial.println();

  delay(1000);
}

int checkCard(String str) {
  for (int i=0; i<nCards; i++) {
    if (str == tst[i]) {
      return 1;
    }
  }

  return 0;
}

int checkUser(String str) {
  for (int i=0; i<nCards; i++) {
    if (str == tst[i]) {
      return i + 1;
    }
  }
}
