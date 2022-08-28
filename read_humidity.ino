/* Analog Input Example, Teensyduino Tutorial #4
   http://www.pjrc.com/teensy/tutorial4.html

   After uploading this to your board, use Serial Monitor
   to view the message.  When Serial is selected from the
   Tools > USB Type menu, the correct serial port must be
   selected from the Tools > Serial Port AFTER Teensy is
   running this code.  Teensy only becomes a serial device
   while this code is running!  For non-Serial types,
   the Serial port is emulated, so no port needs to be
   selected.

   This example code is in the public domain.
*/
const int ledPin = 11;
const int soilPin = 21;

void setup()
{                
  Serial.begin(9800);
  pinMode(ledPin, OUTPUT);
}


void loop()                     
{
  int val = analogRead(soilPin);
  Serial.print("soilPin  is: ");
  Serial.println(val);
  
  digitalWrite(ledPin, HIGH);   // set the LED on
  delay(1000);                  // wait for a second
  digitalWrite(ledPin, LOW);    // set the LED off
  delay(100); 
}
