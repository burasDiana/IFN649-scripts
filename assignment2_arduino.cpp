#include "DHT.h"

const int delaytime = 1000;
const int ledRED = 1;
const int ledYELLOW = 2;
const int ledGREEN = 0;
const int LDRPIN = 20;

const String status_ok = 0;
const String status_bad = "1";
const String status_ok_warnings = "2";
const String status_Start = "Start";

#define DHTPIN 21     
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

// Teensy 5V <--> HC-05 Vcc
// Teensy Ground <--> HC-05 GND
#define rxPin 7 // Teensy pin 7 <--> HC-05 Tx
#define txPin 8 // Teensy pin 8 <--> HC-05 Rx
//SoftwareSerial BTSerial =  SoftwareSerial(rxPin, txPin);

void setup() {
Serial.begin(9600);
pinMode(ledRED, OUTPUT);
pinMode(ledYELLOW, OUTPUT);
pinMode(ledGREEN, OUTPUT);
pinMode(LDRPIN, INPUT);

// Setup DHT Sensor
  pinMode(DHTPIN, INPUT);
  dht.begin();

// Setup Serial1 for BlueTooth
  Serial1.begin(9600);
}

void loop() {
if(Serial1.available() > 0)
  {
    String str = Serial1.readString();
    //String str = Serial.readStringUntil('\n');
    //Serial.print(F(" Status is: "));  
    //Serial.print(str);
    //Serial.print(str.substring(1));
    if (str.trim() == status_Start){
      Serial.print("Reading data: start");
      }
    else if (str.trim() == status_ok) //str.substring(1).trim() <= sometimes this works idk why
      {
      Serial.print("green on");
      greenLightOn();
      }
    else if (str.trim() == status_ok_warnings)
      {
      Serial.print("yellow on");
      yellowLightOn();
      }
    else if (str.trim() == status_bad)
      {
      Serial.print("red on");
      redLightOn();
      }
      
readHumTemp();
//readLDR();
  }
}

void readHumTemp(){
    float h = dht.readHumidity();
    float t = dht.readTemperature();
    float hic = dht.computeHeatIndex(t, h, false);  

    Serial.print(F(" Humidity: "));
    Serial.print(h); 
    Serial.print(F("%  Temperature: "));
    Serial.print(t);
    Serial.print(F("C "));
    Serial.print(F(" Heat index: "));
    Serial.print(hic);
    Serial.println(F("C"));

    Serial1.print(F(" Humidity: "));
    Serial1.print(h);
    Serial1.print(F("%  Temperature: "));
    Serial1.print(t);
    Serial1.print(F("C "));
    Serial1.print(F(" Heat index: "));
    Serial1.print(hic);
    Serial1.print(F("C"));

    // LDR Reading
    int ldr = analogRead(LDRPIN);
    Serial.print(" LDR: ");
    Serial.println(ldr);
    Serial1.print(F(" LDR: "));
    Serial1.print(ldr);
    Serial1.println(F(" "));
    
    delay(delaytime);
}

void readLDR(){
int ldr = analogRead(LDRPIN);
Serial1.print(F(" LDR: "));
Serial1.print(ldr);

Serial.print(" LDR: ");
Serial.println(ldr);

delay(delaytime); // wait for a second
  }

void redLightOn(){
digitalWrite(ledYELLOW, LOW); 
digitalWrite(ledGREEN, LOW); 
digitalWrite(ledRED, HIGH); 
delay(delaytime); 
digitalWrite(ledRED, LOW); 

}

void greenLightOn(){
digitalWrite(ledRED, LOW); 
digitalWrite(ledYELLOW, LOW); 
digitalWrite(ledGREEN, HIGH);
delay(delaytime); 
digitalWrite(ledGREEN, LOW); 

}

void yellowLightOn(){
digitalWrite(ledRED, LOW); 
digitalWrite(ledGREEN, LOW); 
digitalWrite(ledYELLOW, HIGH);
delay(delaytime);
digitalWrite(ledYELLOW, LOW);  
}