
#BLE2MQTT

##Manifest:

This directory contains:

- ble2mqtt.py: a python script to run on a BLE-enabled device that picks up BLE Eddystone beacon packets off the device, parses out the pH field, forms an MQTT packet with the current timestamp and the RSSI (& distance estimate from the RSSI) and sends it up to the broker either on the same machine or a network-connected server.  

- ble2mqttd.py: a configurable systemd daemon that does basically the same thing as ble2mqtt.py but starts on system boot, allows status check, enable, reconfigure & restart from systemd  

- ble2mqttd.conf: 

- ble2mqttd.service:

##Dependencies:

- Bluez device stack


- bluepy library: https://github.com/IanHarvey/bluepy:

pip install bluepy

- paho-mqtt 

