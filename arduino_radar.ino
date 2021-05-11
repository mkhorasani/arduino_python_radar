#include <Servo.h>
Servo myservo; 
int val = 0;              // variable to store the sensor value
int analogPin = A0;       // sensor pin
String pval = "*";        // string variable to send sensor value over COM port

void setup() {
  Serial.begin(9600);     // setup serial communication
  myservo.attach(3);      // attach motor to PWM pin 3
  myservo.write(90);      // rotating motor to initial position
}

void loop() {
  for(int i=0;i<=180;i=i+2){
    myservo.write(i);                                 // rotating motor CW
    val = 100095*(pow(analogRead(analogPin),-0.966)); // sensor calibration equation
    if ((val>1500) || (val<0)){                       // disregarding erroneous readings
      val = NULL;
    }
    Serial.println(i + pval + val);                   // sending motor position and sensor reading over COM port
    delay(50);
  }
  for(int i=180;i>=0;i=i-2){
    myservo.write(i);                                 // rotating motor CCW
    val = 100095*(pow(analogRead(analogPin),-0.966)); // sensor calibration equation
    if ((val>1500) || (val<0)){                       // disregarding erroneous readings
      val = NULL;
    }
    Serial.println(i + pval + val);                   // sending motor position and sensor reading over COM port
    delay(50);
  }
}
