#include <SoftwareSerial.h>
SoftwareSerial mySerial(3,2);
void setup() {
  mySerial.begin (9600);
  Serial.begin(9600);
}
 
void loop() {
  delay(500);
  mySerial.println(2);
  mySerial.println(30);
  mySerial.println(40);
}
