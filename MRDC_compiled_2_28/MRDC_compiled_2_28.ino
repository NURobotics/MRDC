const float pi = 3.141596;
const int led = 13;

//Xbox Controller **********************************************************************
#include <XBOXRECV.h>
// Satisfy the IDE, which needs to see the include statment in the ino too.
#ifdef dobogusinclude
#include <spi4teensy3.h>
#include <SPI.h>
#endif
USB Usb;
XBOXRECV Xbox(&Usb);

//Motor**********************************************************************

//front left
const int en1 = 2;
const int dir1 = 23;

//front right
const int en2 = 3;
const int dir2 = 22;

//back left
const int en3 = 4;
const int dir3 = 25;

//back right
const int en4 = 5;
const int dir4 = 24;

//if RT or LT is pressed
int stateR2;
int stateL2;

void setup() {
  pinMode(en1, OUTPUT);
  pinMode(dir1, OUTPUT);

  pinMode(en2, OUTPUT);
  pinMode(dir2, OUTPUT);

  pinMode(en3, OUTPUT);
  pinMode(dir3, OUTPUT);

  pinMode(en4, OUTPUT);
  pinMode(dir4, OUTPUT);

  // enable diagnostic output
  Serial.println("\n\n\n");
  Serial.println("Ready.");

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

  stateL2 = Xbox.getButtonPress(L2);
  stateR2 = Xbox.getButtonPress(R2);


  Usb.Task();
  //    if (Xbox.XboxReceiverConnected) {
  //      Serial.println(Xbox.getAnalogHat(RightHatY));
  //      Serial.println(Xbox.getAnalogHat(RightHatX));
  //      }

  move_all_motors();

}





