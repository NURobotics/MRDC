const int Channel1pin = 9;
const int Channel4pin = 10;

int Channel1, Channel4;

void setup() {
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
  
}
