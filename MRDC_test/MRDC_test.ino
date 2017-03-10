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
const int en3 = 11;
const int dir3 = 29;

//back right
const int en4 = 5;
const int dir4 = 24;

//5th one (hopper movement)
const int en5 = 6;
const int dir5 = 36;


//6th one (arm)
const int en6 = 7;
const int dir6 = 37;

//Servos*****************************************************************
Servo wall;
Servo arm;
const int wall_pin = 8;
const int arm_pin = 12;
bool wall_state; //setting wall state to 1 to indicate up
int arm_servo_state; //position of arm servo

//if RT or LT is pressed
int analogR2;
int analogL2;
int arm_motor_state = 0; //0 is off 1 is on
int initial_pos = 80;

void setup() {
  pinMode(en1, INPUT);
  pinMode(en2, INPUT);
  pinMode(en3, INPUT);
  pinMode(en4, INPUT);
  pinMode(en5, INPUT);
  pinMode(en6, INPUT);
  pinMode(wall_pin, INPUT);
  pinMode(arm_pin, INPUT);

  delay(1000);

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
  pinMode(arm_pin, OUTPUT);

  wall.attach(wall_pin, 900, 2100);
  wall.write(initial_pos); //set servo to initial position
  wall_state = 1; //set state to high

  arm.attach(arm_pin, 900, 2100);
  arm_servo_state = 90;
  arm.write(arm_servo_state);


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

  Usb.Task();
  if (Xbox.XboxReceiverConnected) {
    analogL2 = Xbox.getButtonPress(L2);
    analogR2 = Xbox.getButtonPress(R2);
    move_hopper((analogR2 - analogL2) * 0.5);

    arm_motion();

    move_all_motors();

    if (Xbox.getButtonClick(LEFT)) {
      arm_servo_state = arm_servo_state - 10;
      if (arm_servo_state < 0) {
        arm_servo_state = 0;
      }
      arm.write(arm_servo_state);
    }

    if (Xbox.getButtonClick(RIGHT)) {
      arm_servo_state = arm_servo_state + 10;
      if (arm_servo_state > 180) {
        arm_servo_state = 180;
      }
      arm.write(arm_servo_state);
    }
    //    Serial.println(arm_servo_state);

    if (Xbox.getButtonClick(A)) {
      release_wall();
    }

  } else {

    move_motor1(0);
    move_motor2(0);
    move_motor3(0);
    move_motor4(0);
    move_hopper(0);
    move_arm(0);
  }
}





