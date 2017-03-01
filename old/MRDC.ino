const int Channel1pin = 9;
const int Channel4pin = 10;

const int en1 = 2;
const int dir1 = 3;


int Channel1, Channel4;

void setup() {

  pinMode(en1, OUTPUT);
  pinMode(dir1, OUTPUT);

  
  pinMode(Channel1pin,INPUT);
  pinMode(Channel4pin,INPUT);
  Serial.begin(9600);

}

void loop() {
  Channel1 = pulseIn(Channel1pin, HIGH);
  Channel4 = pulseIn(Channel4pin, HIGH);

  Serial.print(Channel1);
  Serial.print("   ");
  Serial.println(Channel4);

  move_motor1(512);
  
}

void move_motor1(int spd) {
  if (spd >= 0) {
    analogWrite(en1, spd);
    digitalWrite(dir1, HIGH);
  } else if (spd < 0) {
    analogWrite(en1, -spd);
    digitalWrite(dir1, LOW);
  }

}

