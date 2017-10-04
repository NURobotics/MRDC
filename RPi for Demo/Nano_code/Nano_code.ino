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

const byte numChars = 32;
char receivedChars[numChars];
char tempChars[numChars];        // temporary array for use when parsing

// variables for parsed data
char command_type_str[numChars] = {0};
char command_type = 0;
signed int newSpeeds[4];

boolean newData = false;

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

  wall.attach(wall_pwm);
  wall.write(70); // set servo to initial position
  wall_state = 1; // set state to 1

  Serial.begin(9600);
//  Serial.println("Format: <A,0,0,0,0>");
}

//===========

void loop() {
    recvWithStartEndMarkers();
    if (newData == true) {
        strcpy(tempChars, receivedChars);
            // this temporary copy is necessary to protect the original data
            //   because strtok() used in parseData() replaces the commas with \0
        parseData();
        
        // change motor speeds based on command_type
        if (command_type == 'D'){
          
//          Serial.println(newSpeeds[0]);
//          Serial.println(newSpeeds[1]);
//          Serial.println(newSpeeds[2]);
//          Serial.println(newSpeeds[3]);

          move_motor1(newSpeeds[0]);
          move_motor2(newSpeeds[1]);
          move_motor3(newSpeeds[2]);
          move_motor4(newSpeeds[3]);
                    
        } else if (command_type == 'H') {
          
//          Serial.println(newSpeeds[0]);

          move_hopper(newSpeeds[0]);
          
        } else if (command_type == 'W') {
          
//          Serial.println("wall");

          release_wall();
          
        }

        newData = false;
        
    }
}

//============

void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;

    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

//============

void parseData() {      // split the data into its parts

    char * strtokIndx; // this is used by strtok() as an index

    strtokIndx = strtok(tempChars,",");      // get the first part - the string
    strcpy(command_type_str, strtokIndx); // copy to string
    command_type = command_type_str[0];  
 
    strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
    newSpeeds[0] = atoi(strtokIndx);     // convert this part to an integer

    strtokIndx = strtok(NULL, ","); 
    newSpeeds[1] = atoi(strtokIndx);    

    strtokIndx = strtok(NULL, ","); 
    newSpeeds[2] = atoi(strtokIndx);    

    strtokIndx = strtok(NULL, ","); 
    newSpeeds[3] = atoi(strtokIndx);     
}

//============

void showParsedData() {
    Serial.println(command_type);
    Serial.println(newSpeeds[0]);
    Serial.println(newSpeeds[1]);
    Serial.println(newSpeeds[2]);
    Serial.println(newSpeeds[3]);
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
    wall.write(90);
    wall_state = 0;
  } else {
    wall.write(70);
    wall_state = 1;
  }
}
