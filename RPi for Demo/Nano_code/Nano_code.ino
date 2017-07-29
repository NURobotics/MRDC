#include <Servo.h>

// Arduino nano taking control signals from a Raspberry Pi

// Motor pins ***********************************************************

// Drive
// Motor 1
const int en1 = 3;
const int ph1 = 2;

// Motor 2
const int en2 = 5;
const int ph2 = 4;

// Motor 3
const int en3 = 6;
const int ph3 = 7;

// Motor 4
const int en4 = 9;
const int ph4 = 8;

// Other
// Hopper
const int en5 = 11;
const int ph5 = 12;

// Servo
const int wall_pwm = 10;
Servo wall;
bool wall_state;

// Serial comms
char type = 'A';

int motor1 = 0;
int motor2 = 0;
int motor3 = 0;
int motor4 = 0;

int spd = 0;

void setup() {
  pinMode(en1, OUTPUT);
  pinMode(ph1, OUTPUT);

  pinMode(en2, OUTPUT);
  pinMode(ph2, OUTPUT);

  pinMode(en3, OUTPUT);
  pinMode(ph3, OUTPUT);

  pinMode(en4, OUTPUT);
  pinMode(ph4, OUTPUT);

  pinMode(en5, OUTPUT);
  pinMode(ph5, OUTPUT);

  pinMode(wall_pwm, OUTPUT);

  wall.attach(wall_pwm, 900, 2100);
  wall.write(0); // set servo to initial position
  wall_state = 1; // set state to 1

  Serial.begin(115200);
  while(!Serial); // wait until Serial is connected
  Serial.print("Connected!\n");
}

void loop() {
  if (Serial.available()>0) {
    type = Serial.read();
    
    if (type == 'D') {
      
      Serial.println(type); // echo to Pi
      motor1 = Serial.parseInt();
      motor2 = Serial.parseInt();
      motor3 = Serial.parseInt();
      motor4 = Serial.parseInt();

      Serial.println(motor1);
      Serial.println(motor2);
      Serial.println(motor3);
      Serial.println(motor4);

      move_motor1(motor1);
      move_motor2(motor2);
      move_motor3(motor3);
      move_motor4(motor4);

      Serial.println("Done");
      
    } else if (type == 'H') {
      
      Serial.println(type); // echo to P
      spd = Serial.parseInt();
      
      Serial.println(spd);
      
      move_hopper(spd); 
       
      Serial.println("Done"); 
       
    } else if (type == 'W') {
      
      Serial.println(type); // echo to Pi
      
      release_wall();
      
      Serial.println("Done");
    }
  }
}

void move_motor1(int spd) {
  if (spd>0) {
    analogWrite(en1, spd);
    digitalWrite(ph1, HIGH);
  } else {
    analogWrite(en1, -spd);
    digitalWrite(ph1, LOW);
  }
}

void move_motor2(int spd) {
  if (spd>0) {
    analogWrite(en2, spd);
    digitalWrite(ph2, HIGH);
  } else {
    analogWrite(en2, -spd);
    digitalWrite(ph2, LOW);
  }
}

void move_motor3(int spd) {
  if (spd>0) {
    analogWrite(en3, spd);
    digitalWrite(ph3, HIGH);
  } else {
    analogWrite(en3, -spd);
    digitalWrite(ph3, LOW);
  }
}

void move_motor4(int spd) {
  if (spd>0) {
    analogWrite(en4, spd);
    digitalWrite(ph4, HIGH);
  } else {
    analogWrite(en4, -spd);
    digitalWrite(ph4, LOW);
  }
}

void move_hopper(int spd) {
  if (spd>0) {
    analogWrite(en5, spd);
    digitalWrite(ph5, HIGH);
  } else {
    analogWrite(en5, -spd);
    digitalWrite(ph5, LOW);
  }
}

void release_wall() {
  if(wall_state == 1) { //wall is up, pull it down
    wall.write(180);
    wall_state = 0;
  } else {
    wall.write(0);
    wall_state = 1;
  }
}
