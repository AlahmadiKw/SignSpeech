// Delcare Flex Sensor Pins
int thumbFlexPin = A4;
int indexFlexPin = A3;
int middleFlexPin = A2;
int ringFlexPin = A1;
int pinkyFlexPin = A0;
int button = A8; 

// Declare Touch Sensor Pins
int thumbTouchPin = 0;
int indexTouchPin = 5;
int middleTouchPin = 4;
int ringTouchPin = 3;
int pinkyTouchPin = 2;

//Declare Flex Sensor Values
int thumbReading = 0;
int indexReading = 0;
int middleReading = 0;
int ringReading = 0;
int pinkyReading = 0;

int thumbConverted = 0;
int indexConverted = 0;
int middleConverted = 0;
int ringConverted = 0;
int pinkyConverted = 0;

// Declare Touch Sensor Values
int indexTouchVal = 0;
int middleTouchVal = 0;
int ringTouchVal = 0;
int pinkyTouchVal = 0;

// Set Min and Max for calibration
int thumbMin = 1023;
int indexMin = 1023;
int middleMin = 1023;
int ringMin = 1023;
int pinkyMin = 1023;

int thumbMax = 0;
int indexMax = 0;
int middleMax = 0;
int ringMax = 0;
int pinkyMax = 0;


int addr = 0;

void setup(){
  Serial.begin(9600);
  pinMode(thumbTouchPin, OUTPUT);
  pinMode(indexTouchPin, INPUT);
  pinMode(middleTouchPin, INPUT);
  pinMode(ringTouchPin, INPUT);
  pinMode(pinkyTouchPin, INPUT);
  digitalWrite(thumbTouchPin, HIGH);
  
  //calibrate
  while(Serial.read() == -1){
    thumbMin = min(analogRead(thumbFlexPin), thumbMin); 
    indexMin = min(analogRead(indexFlexPin), indexMin);
    middleMin = min(analogRead(middleFlexPin), middleMin);
    ringMin = min(analogRead(ringFlexPin), ringMin);
    pinkyMin = min(analogRead(pinkyFlexPin), pinkyMin);
    
    thumbMax = max(analogRead(thumbFlexPin), thumbMax); 
    indexMax = max(analogRead(indexFlexPin), indexMax);
    middleMax = max(analogRead(middleFlexPin), middleMax);
    ringMax = max(analogRead(ringFlexPin), ringMax);
    pinkyMax = max(analogRead(pinkyFlexPin), pinkyMax);
    delay(50);
  }  
  
 
}

void loop(){
  
  // read in flex sensor values
  thumbReading = analogRead(thumbFlexPin); 
  indexReading = analogRead(indexFlexPin);
  middleReading = analogRead(middleFlexPin);
  ringReading = analogRead(ringFlexPin);
  pinkyReading = analogRead(pinkyFlexPin);

  // scale and constraing
  thumbConverted = constrain(map(thumbReading, thumbMax, thumbMin, 0, 100), 0, 100); 
  indexConverted = constrain(map(indexReading, indexMin, indexMax, 0, 100), 0, 100); 
  middleConverted = constrain(map(middleReading, middleMin, middleMax, 0, 100), 0, 100); 
  ringConverted = constrain(map(ringReading, ringMin, ringMax, 0, 100), 0, 100); 
  pinkyConverted = constrain(map(pinkyReading, pinkyMin, pinkyMax, 0, 100), 0, 100); 
  
  // read in touch sensor values
  indexTouchVal = digitalRead(indexTouchPin);
  middleTouchVal = digitalRead(middleTouchPin);
  ringTouchVal = digitalRead(ringTouchPin);
  pinkyTouchVal = digitalRead(pinkyTouchPin);
    
  // print to serial  
  Serial.println('/' + String(thumbConverted) + 
                 '/' + String(indexConverted) + 
                 '/' + String(middleConverted) + 
                 '/' + String(ringConverted) + 
                 '/' + String(pinkyConverted) + 
                 '/' + String(indexTouchVal) + 
                 '/' + String(middleTouchVal) + 
                 '/' + String(ringTouchVal) + 
                 '/' + String(pinkyTouchVal) + "/%");
                 
  Serial.println('/' + String(thumbReading) + 
                 '/' + String(indexReading) + 
                 '/' + String(middleReading) + 
                 '/' + String(ringReading) + 
                 '/' + String(pinkyReading) + "/%");   
                 
//  Serial.println(' ' + String(thumbMax) + 
//                 ' ' + String(indexMax) + 
//                 ' ' + String(middleMax) + 
//                 ' ' + String(ringMax) + 
//                 ' ' + String(pinkyMax) + 
//                 ' ' + String(thumbMin) + 
//                 ' ' + String(indexMin) + 
//                 ' ' + String(middleMin) + 
//                 ' ' + String(ringMin) + 
//                 ' ' + String(pinkyMin) + " %");
//                 
  delay(50); //just here to slow down the output for easier reading
}

