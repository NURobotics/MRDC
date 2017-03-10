
//motor1 = en1
//motor2 = en2
//motor3 = en3
//motor4 = en4


//move left and right

//mapping the signal from the joystick to actual speeds
int map_analog(float val) {
  int ret_val;  
//  deadzone between 0 and 3200
  if (val > 100 && val < 4000) {
    ret_val = 0;
  } else {
    ret_val = map(val, -32768, 32767, -100, 100);
  }
  return ret_val;
}

void move_all_motors() {

  //left joystick
  float drive;
  float strafe;
  float rot;
  int drive_spd;
  int strafe_spd;
  int rot_spd;

  //analog signal for the left joystick, this is to move forward and back
  drive = Xbox.getAnalogHat(LeftHatY);
  strafe = Xbox.getAnalogHat(LeftHatX);
  rot = Xbox.getAnalogHat(RightHatX);

  
  drive_spd = map_analog(drive);
  strafe_spd =  map_analog(strafe);
  rot_spd =  map_analog(rot);


  move_motor1(-drive_spd + strafe_spd - rot_spd);
  move_motor2(-drive_spd - strafe_spd + rot_spd);
  move_motor3(-drive_spd - strafe_spd - rot_spd);
  move_motor4(-drive_spd + strafe_spd + rot_spd);

}

void move_left_right(int spd23, int spd14) {
  move_motor1(spd14);
  move_motor2(spd23);
  move_motor3(spd23);
  move_motor4(spd14);
}


//move forward and backward
void move_motors12(int spd) {
  move_motor1(spd);
  move_motor2(spd);
}

void move_motors34(int spd) {
  move_motor3(spd);
  move_motor4(spd);
}


//backward full speed is -255, forward full speed is 255
void move_motor1(int spd) {
  if (spd >= 0) {
    analogWrite(en1, spd);
    digitalWrite(dir1, HIGH);
  } else if (spd < 0) {
    analogWrite(en1, -spd);
    digitalWrite(dir1, LOW);
  }
}

void move_motor2(int spd) {
  if (spd >= 0) {
    analogWrite(en2, spd);
    digitalWrite(dir2, HIGH);
  } else if (spd < 0) {
    analogWrite(en2, -spd);
    digitalWrite(dir2, LOW);
  }
}

void move_motor3(int spd) {
  if (spd >= 0) {
    analogWrite(en3, spd);
    digitalWrite(dir3, HIGH);
  } else if (spd < 0) {
    analogWrite(en3, -spd);
    digitalWrite(dir3, LOW);
  }
}

void move_motor4(int spd) {
  if (spd >= 0) {
    analogWrite(en4, spd);
    digitalWrite(dir4, HIGH);
  } else if (spd < 0) {
    analogWrite(en4, -spd);
    digitalWrite(dir4, LOW);
  }
}

void move_hopper(int spd) {
  if (spd >= 0) {
    analogWrite(en5, spd);
    digitalWrite(dir5, HIGH);
  } else if (spd < 0) {
    analogWrite(en5, -spd);
    digitalWrite(dir5, LOW);
  }
}

void move_arm(int spd) {
  if (spd >= 0) {
    analogWrite(en6, spd);
    digitalWrite(dir6, HIGH);
  } else if (spd < 0) {
    analogWrite(en6, -spd);
    digitalWrite(dir6, LOW);
  }
}

void arm_motion() {
  if (Xbox.getButtonClick(L1)) {
    Serial.println("l1");
    if (arm_motor_state == 0) {
      move_arm(50);
      arm_motor_state = 1;
    } else {
      move_arm(0);
      arm_motor_state = 0;
    }
  }

  if (Xbox.getButtonClick(R1)) {
    Serial.println("R1");
    if (arm_motor_state == 0) {
      move_arm(-50);
      arm_motor_state = 1;
    } else {
      move_arm(0);
      arm_motor_state = 0;
    }
  }
}


