
// Counter code which uses panasonic ex-23-c5 sensor
// to interact with this code please look for CounterThread under pywiliot->wiliot->wiliot_testers->tester_utils

const int input = 2; // This is where the input is fed.
int pulse = 0; // Variable for saving pulses count.
int var = 0;

void setup(){
  pinMode(input, INPUT);
 
  Serial.begin(9600);
  Serial.println(F("No pulses yet...")); // Message to send initially (no pulses detected yet).
}

void loop(){ 
  if(digitalRead(input) > var)
  {
    var = 1;
    pulse++;
   
    Serial.print(pulse);
    Serial.print(F(" pulse"));

    // Put an "s" if the amount of pulses is greater than 1.
    if(pulse > 1) {Serial.print(F("s"));}
   
    Serial.println(F(" detected."));
  }
 
  if(digitalRead(input) == 0) {var = 0;}
 
  delay(1); // Delay for stability.
}
