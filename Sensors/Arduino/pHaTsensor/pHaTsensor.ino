#include <Arduino.h>
#include <SPI.h>
#include <Adafruit_ATParser.h>
#include <Adafruit_BLE.h>
#include <Adafruit_BLEBattery.h>
#include <Adafruit_BLEEddystone.h>
#include <Adafruit_BLEGatt.h>
#include <Adafruit_BLEMIDI.h>
#include <Adafruit_BluefruitLE_SPI.h>
#include <Adafruit_BluefruitLE_UART.h>
#include <SoftwareSerial.h>

// from eddystone ex start


#define DEBUG 0
#include "BluefruitConfig.h"

#define FACTORYRESET_ENABLE         1
#define MINIMUM_FIRMWARE_VERSION    "0.7.0"
#define URL                         "http://mdc?pH="

Adafruit_BluefruitLE_SPI ble(BLUEFRUIT_SPI_CS, BLUEFRUIT_SPI_IRQ, BLUEFRUIT_SPI_RST);
Adafruit_BLEEddystone eddyBeacon(ble);

#define rx 11                                        //define what pin rx is going to be 11 IS CORRECT                                                    
#define tx 12                                        //define what pin tx is going to be

SoftwareSerial myserial(rx, tx);                     //define how the soft serial port is going to work 

String inputstring = "";                             //a string to hold incoming data from the PC
String sensorstring = "";                            //a string to hold the data from the Atlas Scientific product
String urlstring = URL;
char urlcharArray[17];


boolean input_string_complete = false;                //have we received all the data from the PC
boolean sensor_string_complete = false;               //have we received all the data from the Atlas Scientific product
float pH;                                             //used to hold a floating point number that is the pH
float prev_pH;

void setup() {
  
  ble.begin(VERBOSE_MODE);

  ble.factoryReset();
  
  myserial.begin(9600);  //set baud rate for the software serial port to 9600
  
  eddyBeacon.begin(true);

  inputstring.reserve(10);                            //set aside some bytes for receiving data from the PC
  sensorstring.reserve(30);                           //set aside some bytes for receiving data from Atlas Scientific product
}


void loop() {                                         //here we go...

  if (myserial.available() > 0) {                     //if we see that the Atlas Scientific product has sent a character  
    char inchar = (char)myserial.read();              //get the char we just received
    if (inchar != '.') {                              // exclude the decimal point because we know it's to 3 decimal places
                                                      // and we'll need to make a valid URI from this string
        sensorstring += inchar;                       //add the char to the var called sensorstring
    }
    if (inchar == '\r') {                             //if the incoming character is a <CR>
      sensor_string_complete = true;                  //set the flag
    }
  }


   if (sensor_string_complete == true) {               //if a string from the Atlas Scientific product has been received in its entirety
                                                        //uncomment this section to see how to convert the pH reading from a string to a float
      if (isdigit(sensorstring[0])) {                   //if the first character in the string is a digit
      prev_pH = pH;
      pH = sensorstring.toFloat();                    //convert the string to a floating point number so it can be evaluated by the Arduino
      
      if (abs (pH - prev_pH) > 0.1) {

             urlstring += sensorstring;
             urlstring.toCharArray(urlcharArray,20);

             eddyBeacon.stopBroadcast(); 
             eddyBeacon.setURL(urlcharArray);                             
             eddyBeacon.startBroadcast(); 
                              
             urlstring = URL;      
          }
      }  

   sensorstring = "";                                //clear the string
   sensor_string_complete = false;                   //reset the flag used to tell if we have received a completed string from the Atlas Scientific product
  }
}


