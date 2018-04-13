

This Arduino sketch pHaTsensor is compiled with the Arduino IDE 'Tools->Board' with option "Adafruit Feather 324u"

There are complete instructions for installing and configuring Arduino IDE and their BLE library at:

https://learn.adafruit.com/adafruit-feather-32u4-bluefruit-le/using-with-arduino-ide

Make sure to DFU (Devide Firmware Update) your Feather Bluefruit board for running firmware release 0.8.0, which can be found in:

https://github.com/adafruit/Adafruit_BluefruitLE_Firmware/tree/master/0.8.0/blespifriend

The instructions for doing a DFU are at: 

https://learn.adafruit.com/adafruit-feather-32u4-bluefruit-le/dfu-bluefruit-updates

Since 0.8.0 is released, it will show up on your Bluefruit LE Connect app, and you can update it from there.  The reason this update is so important is that earlier versions of the firmware would run for awhile and then just stop, and not run again without a DFU update.  It was a bug in the firmware.  So please get 0.8.0 or later.  
