/*
Controlc of Servo Motor attached to flexible lense with distance sensor.

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
char controlMode ='0';
char movingDirection = 'f';

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
int servoSpeedMax = 2.5;
float deltaServo;
float filterRatio = 0.01; // the smaller, the longer it takes to accept new values.

// Iteration counter  to display output
int itNum;

// Distance and Corresponding Position
//const int refDist [] = {0, 1000, 2000, 3000}; // [mm]
//const int refAng [] = {0, 90, 120, 180}; // [deg]

const int refDist [] = { 270, 246, 222, 197, 170, 149, 122, 92, 68,  40}; // [mm]
const int refAng [] =  {  60,  60,  65,  65,  65,  70,  75, 85, 90, 125}; // [deg]
const int deltaPos_dir = 10; // [deg]
// direction up at 80
// direction up at 70

// delta 10, it doesen't move.

int nMeas;
const int servoMin = 40;
const int servoMax = 135;

const int defaultPos = 40;

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

  // Initial servo pos
  servoPos = defaultPos;
  Servo1.write(servoPos);
  delay(100);
  Servo1.write(servoPos+1);
  delay(100);
  Servo1.write(servoPos-1);
  delay(100);
  Servo1.write(servoPos);
}


void loop() {
  servoPos_new = servoPos;

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
      if(distance_mm > refDist[i] || i == nMeas-1){
      servoPos_new = (1.*distance_mm-refDist[i-1])/(refDist[i]-refDist[i-1]) * (refAng[i]-refAng[i-1]) + refAng[i-1];
      break;
      }
    }
    // Add filtering ???
    //servoPos = servoPos*(1-filterRatio) + servoPos_new*filterRatio;
    //servoPos = servoPos_new;

    if(itNum>10){
      itNum = 0;
      Serial.print(F("Iteration : "));
      //Serial.print(i);
      Serial.print(i);
      Serial.print("\r\n");

      Serial.print(F("Distance [mm]:"));
      Serial.print(distance_mm);
      Serial.print("\r\n");
      Serial.print(F("refDist1:"));
      Serial.print(refDist[i-1]);
      Serial.print("\r\n");

      Serial.print(F("refDist2:"));
      Serial.print(refDist[i]);
      Serial.print("\r\n");

      Serial.print("Pos: ");
      Serial.print(servoPos_new);
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
        servoPos_new = servoPos - 5;
      }
      Serial.print("---------- New pos: ");
      Serial.print(servoPos);
      Serial.print("\r\n");
    }
    else if(char(inputSerial)=='u'){// 'u'  117
        if(servoPos <= 180) {
          servoPos_new = servoPos + 5;
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

  // Decide directino of movement
  deltaServo = servoPos_new - servoPos;
  if(deltaServo > 0){
    movingDirection = 'f';
  }
  else if(deltaServo < 0){
    servoPos_new = servoPos_new - deltaPos_dir;
    movingDirection = 'b';
  }

  // Initial seringe movement to get the motor moving.
  if(char(movingDirection) == 'b'){
      servoPos_new = servoPos_new - deltaPos_dir;
  }
//
//  // Output servo positoin
//  Serial.print("New Pos");
//  Serial.print(servoPos_new);
//  Serial.print("\r\n");
//
//  // Output servo positoin
//  Serial.print("Old Pos: ");
//  Serial.print(servoPos);
//  Serial.print("\r\n");
//
  // Check if maximal position change
  deltaServo = servoPos_new - servoPos; // calculate again with new moving direction

//  // Output servo positoin
//  Serial.print("DeltaServo: ");
//  Serial.print(deltaServo);
//  Serial.print("\r\n");

  if(deltaServo > 0){
    if(deltaServo > servoSpeedMax){
      servoPos = servoPos + servoSpeedMax;
    }
    else{
      servoPos = servoPos + deltaServo;
    }
  }
  else if(deltaServo < 0){ // negative values
    if((-1)*deltaServo > servoSpeedMax){
      servoPos = servoPos - servoSpeedMax;
    }
    else{
      servoPos = servoPos + deltaServo; // is already a negative value
    }
  }


  // Output servo positoin
//  Serial.print("Pos final: ");
//  Serial.print(servoPos);
//  Serial.print("\r\n");


  // Check limits - reset
  if(servoPos > servoMax){
    servoPos = servoMax;
  }
  else if(servoPos < servoMin){
    servoPos = servoMin;
  }




  Servo1.write(servoPos);



  delay(200);
}
