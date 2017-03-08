const float pi = 3.141596;

#include <Servo.h>

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
const int dir3 = 27;

//back right
const int en4 = 5;
const int dir4 = 24;

//5th one (hopper movement)
const int en5 = 6;
const int dir5 = 53;


//6th one (arm)
const int en6 = 7;
const int dir6 = 52;

//Servos*****************************************************************
Servo wall;
const int wall_pin = 8;
bool wall_state; //setting wall state to 1 to indicate up

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

  pinMode(en5, OUTPUT);
  pinMode(dir5, OUTPUT);

  pinMode(en6, OUTPUT);
  pinMode(dir6, OUTPUT);

  pinMode(wall_pin, OUTPUT);

  wall.attach(wall_pin, 900, 2100);
  wall.write(0); //set servo to initial position
  wall_state = 1; //set state to 1
  

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

  move_hopper(stateL2 - stateR2);
//  Serial.println(stateR2 - stateL2);
//  release_wall();
//  delay(1000);
//wall.write(0);
//delay(1000);
//wall.write(180);
//delay(1000);
//  if (Xbox.getButtonClick(A)) {
//    release_wall();
//  }
//  Serial.println(wall_state);
  
}





