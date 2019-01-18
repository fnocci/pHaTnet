#!/usr/bin/python3

# ble2mqtt - script to read data coming into BLE device 
#            from a particular eddystone beacon
#            put it in a json string
#            and send it up to an mqtt broker

from json import JSONEncoder as json
from binascii import unhexlify
from datetime import datetime

# convert TX & RSSI to distance
# TX is measured from beacon

from math import pow

_TX_ = -59

def getDistance (RSSI, TX):
    return pow(10, (TX - RSSI) / (10 * 2));


# scan for & pick up BLE beacon signal using bluepy 
# to get bluepy: pip install bluepy

from bluepy.btle import Scanner, DefaultDelegate

_pHprobe1_addr = 'e5:b5:5a:fa:76:de'

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev: 
            pass #print ("Discovered device", dev.addr)
        elif isNewData:
            pass #print ("Received new data from", dev.addr)


# publish to remote MQTT broker on Pi3
# pip install paho-mqtt

import paho.mqtt.client as mqtt

broker_num =  '192.168.1.31' 
broker_name = 'pithree1'
broker_port = 1883

def on_publish(client, userdata, result):
    print(userdata, " published to mqtt broker with return code: ",result)
    #pass

client = mqtt.Client("ph_topic")

client.on_publish = on_publish

client.connect(broker_num, broker_port)

while True:
    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(10.0)

    for dev in devices:

        if dev.addr == _pHprobe1_addr:

            print ("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))

            for (adtype, desc, value) in dev.getScanData():

               print (adtype, desc, value)

               if adtype == 22: 

                    pH = (int(value[-8:-6]) - 30) + \
                         (int(value[-6:-4]) - 30) * 0.1 + \
                         (int(value[-4:-2]) - 30) * 0.01

                    dist = getDistance(dev.rssi, _TX_)

                    pH_url = 'http://' + str(unhexlify(value[-22:]))[2:-1]

                    print (datetime.now(), dev.addr, dev.rssi, pH_url, pH, dist)

                    pH_json = json().encode (\
                              {'measurement': 'pH', 
                               'time':        str(datetime.now()), 
                               'fields': {
                                 'device': dev.addr, 
                                 'ph_url': pH_url,
                                 'rssi':   dev.rssi,
                                 'dist':   dist,
                                 'pH'  :   pH } } )
                                    

                    # make a big json structure with all the things we want to put in the message

                    ret = client.publish ("pH_url", pH_url)
                    ret = client.publish ("pH_json", pH_json)
                    ret = client.publish ("pH", pH)



