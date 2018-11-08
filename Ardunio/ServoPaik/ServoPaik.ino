/*
Control of Servo Motor attached to flexible lense with distance sensor. 

Control via keyboars:
Control modes:
'0' - default (0 change)

'a' - automatic controll
  
'c' Callibrate
  'u' - increment servo 
  'd' - decrement servo 

*/

#include <Servo.h>

// input/output
int inputSerial;

// Control Mode
char controlMode ='a';

// Distance Sensor
const byte triggerPin = 13;
const byte echoPin = 12;

long lecture_echo;
long distance_mm;
long measure;

//const long timeout = 25000UL; // connait pas a quoi ca sert ??? a chercher
//float soundSpeed = 340/1000;

// Partie pour le servomoteur
// Declare the Servo pin
const int servoPin = 10;

// Create a servo object
Servo Servo1;

int servoPos;

// Distance and Corresponding Position 
const int refDist [] = {0, 1000, 2000, 3000}; // [mm]
const int refAng [] = {0, 90, 120, 180}; // [deg]
int nMeas;

const int defaultPos = 90;


void setup() {
  // We need to attach the servo to the used pin number
  Servo1.attach(servoPin);

  Serial.begin(9600); // Arduino print to cmd

  // Partie pour le capteur de distance
  pinMode(triggerPin,OUTPUT);
  digitalWrite(triggerPin,LOW); //declanchement initial en LOW
  pinMode(echoPin,INPUT);

  nMeas = sizeof(refDist);

  // Initial servo pos
  servoPos = defaultPos;
  Servo1.write(servoPos);
  delay(100);
  Servo1.write(servoPos+10);
  delay(100);
  Servo1.write(servoPos-10);
  delay(100);
  Servo1.write(servoPos);
}


void loop() {
  
  inputSerial = Serial.read(); 
  
  // Change control mode via keyboard
  if(char(inputSerial) == '0'){
    controlMode = '0';
    Serial.print("---------- New mode 'default' \r\n");
    delay(500);
  }
  else if(char(inputSerial) == 'a'){
    controlMode = 'a';
    Serial.print("---------- New mode 'automatic' \r\n");
    delay(500);
  }
  else if(char(inputSerial) == 'c'){
    controlMode = 'c';
    Serial.print("---------- New mode 'callibration' \r\n");
    delay(500);
  }
  
  
  // Capture Distance
  digitalWrite(triggerPin,HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin,LOW);
  
  // mesure le temps d'envoi
  lecture_echo = pulseIn(echoPin,HIGH);
  distance_mm =lecture_echo/6;
  
  
  // Different control modes
  if(controlMode=='0'){ //calibration
      servoPos = defaultPos;
  }
  
  if(controlMode =='a'){ //calibration
    // calcul la distance en fonction du temps de trajet mesuré
    int i;
    for(i=1; i<nMeas; i++){
      if(lecture_echo >  refDist[i]|| i == nMeas-1){
      servoPos = (1.*lecture_echo-refDist[i-1])/(refDist[i]-refDist[i-1]) * (refAng[i]-refAng[i-1]) + refAng[i-1];
      }
    }
    
    Serial.print(F("Distance [mm]:"));
    Serial.print(distance_mm);
    Serial.print("\r\n");
    Serial.print("Pos: ");
    Serial.print(servoPos);
    Serial.print("\r\n");
  }
  else if(controlMode =='c'){ //calibration
  
    if(inputSerial ==100){ // 'd' 100
      if(servoPos >=0){
        servoPos = servoPos - 5; 
      }
      Serial.print("---------- New pos: ");
      Serial.print(servoPos);
      Serial.print("\r\n");
    }
    else if(char(inputSerial)=='u'){// 'u'  117
        if(servoPos <= 180) {
          servoPos = servoPos + 5; 
        }
        Serial.print("---------- New pos: ");
        Serial.print(servoPos);
        Serial.print("\r\n");
    }
    Serial.print(F("Distance [mm]:"));
    Serial.print(distance_mm);
    Serial.print("\r\n");
  }

  Servo1.write(servoPos);

  delay(20);
}
