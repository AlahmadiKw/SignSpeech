//"services.h/spi.h/boards.h" is needed in every new  project
#include <SPI.h>
#include <boards.h>
#include <ble_shield.h>
#include <services.h> 

///////////////////////
// gloves variables  //
///////////////////////

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

///////////////////////////////////
// Bluetooth & button variables  //
///////////////////////////////////
String message;
bool is_pressed;
const int buffer_size = 128;
const int buttonPin = 7;    // the number of the pushbutton pin
const int ledPin = 13;      // the number of the LED pin
// Variables will change:
int ledState = HIGH;         // the current state of the output pin
int buttonState;             // the current reading from the input pin
int lastButtonState = HIGH;   // the previous reading from the input pin
// the following variables are long's because the time, measured in miliseconds,
// will quickly become a bigger number than can be stored in an int.
long lastDebounceTime = 0;  // the last time the output pin was toggled
long debounceDelay = 50;    // the debounce time; increase if the output flickers


void setup()
{  
	// Init. and start BLE library.
	ble_begin();

	// init sensors
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

	// init button, led (for debuging), initialize message to be sent to iphone
	message  = "";
	is_pressed = false; 
	pinMode(buttonPin, INPUT_PULLUP);
	pinMode(ledPin, OUTPUT);
  	digitalWrite(ledPin, ledState); // set initial LED state DEBUGING 
	// ------------------
}

char buf[buffer_size] = {0};
unsigned char len = 0;

void loop(){
	// push button debounce, do not touch
	int reading = digitalRead(buttonPin);
	if (reading != lastButtonState) {
		lastDebounceTime = millis();
	}
	if ((millis() - lastDebounceTime) > debounceDelay) {
		if (reading != buttonState) {
			buttonState = reading;
			if (buttonState == LOW) {
				is_pressed = true; 
				ledState = !ledState;
			}
		}
	}
	if (is_pressed){
		digitalWrite(ledPin, ledState);
	}

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
  
	// conver message to char array and terminate with 0x0A 
	message = String(thumbConverted) + 
                 ' ' + String(indexConverted) + 
                 ' ' + String(middleConverted) + 
                 ' ' + String(ringConverted) + 
                 ' ' + String(pinkyConverted) + 
                 ' ' + String(indexTouchVal) + 
                 ' ' + String(middleTouchVal) + 
                 ' ' + String(ringTouchVal) + 
                 ' ' + String(pinkyTouchVal);
	len = message.length();
	message.toCharArray(buf, buffer_size); 
	buf[len] = 0x0A;
	len++;
    
	// if button is pressed, send via Bluetouth
	if (is_pressed){
		for (int i = 0; i < len; i++)
			ble_write(buf[i]);
		len = 0;
	}

        // proccess ble, reset button state (has to be at the end)
  	ble_do_events();
	is_pressed = false; 
	lastButtonState = reading;
}
