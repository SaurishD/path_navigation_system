/*
 Example sketch for the Xbox Wireless Reciver library - developed by Kristian Lauszus
 It supports up to four controllers wirelessly
 For more information see the blog post: http://blog.tkjelectronics.dk/2012/12/xbox-360-receiver-added-to-the-usb-host-library/ or
 send me an e-mail:  kristianl@tkjelectronics.com
 */

#include <XBOXRECV.h>

// Satisfy the IDE, which needs to see the include statment in the ino too.
#ifdef dobogusinclude
#include <spi4teensy3.h>
#endif
#include <SPI.h>

String out = "";
int left = 0;
int right = 0;
String in = "";
int input = 0;

const int enA = 4;
const int enB = 3;
const int in1 = 5;
const int in2 = 12;
const int in3 = 6;
const int in4 = 7;

int in1Val = 0;
int in3Val = 0;

int mot1=0, mot2 = 0;



USB Usb;
XBOXRECV Xbox(&Usb);

void setup() {
  Serial.begin(115200);
#if !defined(__MIPSEL__)
  while (!Serial); // Wait for serial port to connect - used on Leonardo, Teensy and other boards with built-in USB CDC serial connection
#endif
  if (Usb.Init() == -1) {
    Serial.print(F("\r\nOSC did not start"));
    while (1); //halt
  }
  Serial.print(F("\r\nXbox Wireless Receiver Library Started"));
  
}
void loop() {
  delay(100);
  Usb.Task();
  if (Xbox.XboxReceiverConnected) {
    for (uint8_t i = 0; i < 4; i++) {
      if (Xbox.Xbox360Connected[i]) {
 
        left = Xbox.getAnalogHat(LeftHatY, i)/129;
        right = Xbox.getAnalogHat(RightHatX, i)/129;
       if(left < 50 && left > -50)
          left = 0;
        if(right < 50 && right > -50)
          right = 0;
        
        left = left;
        right = right/2.5;
        mot1 = left+right;
        mot2 = left - right;
        out = String(mot1)+ ',' + String(mot2);

        if (Xbox.getButtonClick(A, i))
          out = 'A';
        if (Xbox.getButtonClick(B, i))
          out = 'B';

              
        Serial.println(out);

        if(left <= 0){
          //Serial.println("IF");
          left = -left;
          digitalWrite(in1,HIGH);
          digitalWrite(in2,LOW);
          digitalWrite(in3,HIGH);
          digitalWrite(in4,LOW);
        }
        else{
          //Serial.println("Else");
          digitalWrite(in1,LOW);
          digitalWrite(in2,HIGH);
          digitalWrite(in3,LOW);
          digitalWrite(in4,HIGH);
        }
        
       if(mot1 < 0){
        mot1 = -mot1;
       }
       if(mot2 < 0){
        mot2 = -mot2;
       }
       if(mot1 > 254){
        mot1 = 254;
       }
       if(mot2 > 254){
        mot2 = 254;
       }
       analogWrite(enA,mot1/1.5);
       analogWrite(enB,mot2);
        

      
       /*digitalWrite(in1,in1Val);
       digitalWrite(in2,(1-in1Val));
       digitalWrite(in3,in3Val);
       digitalWrite(in4,(1-in3Val));*/

      }
    }
  }
  
}
