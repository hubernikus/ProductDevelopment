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

float lecture_echo;
float distance_mm;
long measure;

//const long timeout = 25000UL; // connait pas a quoi ca sert ??? a chercher
//float soundSpeed = 340/1000;

// Partie pour le servomoteur
// Declare the Servo pin
const int servoPin = 10;

// Create a servo object
Servo Servo1;

int servoPos;
float servoPos_new;
int servoSpeedMax = 2;
int deltaServo;
float filterRatio = 0.01; // the smaller, the longer it takes to accept new values.
 
// Iteration counter  to display output
int itNum;

// Distance and Corresponding Position 
const int refDist [] = {0, 1000, 2000, 3000}; // [mm]
const int refAng [] = {0, 90, 120, 180}; // [deg]
int nMeas;
int servoMax, servoMin;

const int defaultPos = 90;

// Iteration counter for printing values to screen
int itCount = 0;

void setup() {
  // We need to attach the servo to the used pin number
  Servo1.attach(servoPin);

  Serial.begin(9600); // Arduino print to cmd

  // Partie pour le capteur de distance
  pinMode(triggerPin,OUTPUT);
  digitalWrite(triggerPin,LOW); //declanchement initial en LOW
  pinMode(echoPin,INPUT);

  // Get number of reference values (Measurements)
  nMeas = sizeof(refDist)/sizeof(refDist[0]);
  Serial.print("Number of reference measurments: ");
  Serial.print(nMeas);
  Serial.print("\r\n");
  
  // Set default servo values
  servoMin = refAng[0];
  servoMax = refAng[nMeas-1];

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
      servoPos_new = defaultPos;
  }
  
  if(controlMode =='a'){ //automatic
    // calcul la distance en fonction du temps de trajet mesuré
    int i;
    
    for(i=1; i<nMeas; i++){
      if(distance_mm < refDist[i] || i == nMeas-1){
      servoPos_new = (1.*distance_mm-refDist[i-1])/(refDist[i]-refDist[i-1]) * (refAng[i]-refAng[i-1]) + refAng[i-1];
      break;
      }
    }
    //
    //servoPos = servoPos*(1-filterRatio) + servoPos_new*filterRatio;
    //servoPos = servoPos_new;
    
    // Check limits
    if(servoPos > servoMax){
      servoPos = servoMax;
    }
    else if(servoPos < servoMin){
      servoPos = servoMin;
    }
    
    if(itNum>-1){
      itNum = 0;
      Serial.print(F("Iteration num:"));
      Serial.print(i                                                                                                                                                                                                                                                                                                                                                                                                                                                  );
      Serial.print("\r\n");   
      
      Serial.print(F("Distance [mm]:"));
      Serial.print(distance_mm);
      Serial.print("\r\n");
      Serial.print("Pos: ");
      Serial.print(servoPos);
      Serial.print("\r\n");
    }
    else
    {
      itNum++;
    }
  }
  else if(controlMode =='c'){ //calibration
  
    if(inputSerial ==100){ // 'd' 100
      if(servoPos >=0){
        servoPos = servoPos - servoSpeedMax; 
      }
      Serial.print("---------- New pos: ");
      Serial.print(servoPos);
      Serial.print("\r\n");
    }
    else if(char(inputSerial)=='u'){// 'u'  117
        if(servoPos <= 180) {
          servoPos = servoPos + servoSpeedMax; 
        }
        Serial.print("---------- New pos: ");
        Serial.print(servoPos);
        Serial.print("\r\n");
    }
    if(itNum>-1){
      itNum =0;
      Serial.print(F("Distance [mm]:"));
      Serial.print(distance_mm);
      Serial.print("\r\n");
    }
    else
    {
      itNum++;
    }
  }
  
  // Check if maximal position change
  deltaServo = servoPos_new - servoPos;
  if(deltaServo > 0){
    if(deltaServo > servoSpeedMax)
      servoPos = servoPos + servoSpeedMax;
    else 
      servoPos = servoPos + deltaServo;
  }
  else if(deltaServo < servoSpeedMax){ // negative values
    if((-1)*deltaServo > servoSpeedMax)
      servoPos = servoPos - servoSpeedMax;
    else 
      servoPos = servoPos - deltaServo;
  }

  Servo1.write(servoPos);

  delay(200);
}
