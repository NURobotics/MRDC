const float pi = 3.141596;


const int led = 13;
//Receiver
const int Channel1pin = 8;
const int Channel4pin = 10;

int Channel1, Channel4;

//Motor
const int en1 = 2;
const int dir1 = 3;
float sig;
int sig_int;

void setup() {
  Serial.begin(9600);
  pinMode(en1, OUTPUT);
  pinMode(dir1, OUTPUT);

  pinMode(Channel1pin, INPUT);
  pinMode(Channel4pin, INPUT);

}

void loop() {

  Channel1 = pulseIn(Channel1pin, HIGH);
  //  Channel4 = pulseIn(Channel4pin, HIGH);
  sig = 0.5045*Channel1 - 752.27;
  sig_int = (int) sig;
  Serial.println(sig_int);
  move_motor1(sig_int);

//move_motor1(-100);


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

