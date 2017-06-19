#include <SoftwareSerial.h>
SoftwareSerial mySerial(3,2);
void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);
}
 
void loop() {
  while(mySerial.available() > 0){
    char c = mySerial.read();
    Serial.write(c);
  }
}
