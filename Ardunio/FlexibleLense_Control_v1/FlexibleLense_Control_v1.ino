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

// wating time after 
int update_freq = 200;


// input/output
int inputSerial;

// Control Mode
char controlMode ='a';
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
/* const int refDist [] = { 270, 246, 222, 197, 170, 149, 122, 92, 68,  40}; // [mm] */
/* const int refAng [] =  {  60,  60,  65,  65,  65,  70,  75, 85, 90, 125}; // [deg] */

const int refDist [] = { 270, 246, 222, 197, 170, 149, 122, 92, 68,  40}; // [mm] > arduino

const int DIST_SAMPLES = 10;
int refAng[10];
const int refAng_fw [] =  {  60,  60,  65,  65,  65,  70,  75, 85, 90, 125}; // [deg] -- fw: servoPos + dServo
const int refAng_bw [] =  {  60,  60,  65,  65,  65,  70,  75, 85, 90, 125}; // [deg] -- bw: servoPos - dServo


/* const int refDist [] = {500, 0}; */
/* const int refAng [] =  {90, 90}; */

/* const int deltaPos_dir = 10; // [deg] */
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

  for(int i=0; i<DIST_SAMPLES; i++){
      refAng[i] = 0.5*(refAng_fw[i] + refAng_bw[i]);
  }
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
  int it_dist = 0;
  if(controlMode =='a'){ //automatic
    // calcul la distance en fonction du temps de trajet mesuré
    for(int i=1; i<nMeas; i++){
      if(distance_mm > refDist[i] || i == nMeas-1){
      servoPos_new = (1.*distance_mm-refDist[i-1])/(refDist[i]-refDist[i-1]) * (refAng[i]-refAng[i-1]) + refAng[i-1];
      it_dist = i;
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
      Serial.print(it_dist);
      Serial.print("\r\n");

      Serial.print(F("Distance [mm]:"));
      Serial.print(distance_mm);
      Serial.print("\r\n");
      Serial.print(F("refDist1:"));
      Serial.print(refDist[it_dist-1]);
      Serial.print("\r\n");

      Serial.print(F("refDist2:"));
      Serial.print(refDist[it_dist]);
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

  // Decide direction of movement forward / backard
  deltaServo = servoPos_new - servoPos;
  if(deltaServo > 0){
    movingDirection = 'f';
    /* servoPos_new = refAng_fw; */
      }
  else if(deltaServo < 0){
    movingDirection = 'b';

    /* servoPos_new = servoPos_new - deltaPos_dir; */
  }

  if(controlMode =='a'){ //calibration
      if(movingDirection=='f'){
          servoPos_new = (1.*distance_mm-refDist[it_dist-1])/(refDist[it_dist]-refDist[it_dist-1])
              * (refAng_fw[it_dist]-refAng_fw[it_dist-1]) + refAng_fw[it_dist-1];
      }else if(movingDirection = 'b'){
          servoPos_new = (1.*distance_mm-refDist[it_dist-1])/(refDist[it_dist]-refDist[it_dist-1])
              * (refAng_bw[it_dist]-refAng_bw[it_dist-1]) + refAng_bw[it_dist-1];          
      }
  }   
 
  // Initial seringe movement to get the motor moving. // accounf for hysterisis
  
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
  
  delay(update_freq);
}
