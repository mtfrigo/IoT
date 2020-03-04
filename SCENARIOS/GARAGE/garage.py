#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, getopt

from neopixel import *

from datetime import datetime
import time

# --- Custom LIB imports
from LIB.ledrgb import LED
from LIB.mqtt import Client as mqttClient
from LIB.esp12e import ESP12e_Push
from LIB.ultrasonic import Ultrasonic

def main(argv):

    # --- Config
    hostname = "129.69.209.78"
    port = 1883

    # --- IP of esp
    esp_ip = "129.69.209.118"

    # --- Broker 
    broker_ip = "129.69.209.78"
    broker_port = 1883
    topic = "esp1"

    # --- Create LED instance
    # TODO should instantiate a Raspi????
    ledrgb = LED(12)

    # --- Create ESP12e instance
    esp = ESP12e_Push(esp_ip, broker_ip, broker_port, topic)
    esp.start()

    # --- Create Ultrasonic sensor instance
    ultrasonic = Ultrasonic(broker_ip, broker_port, topic)

    while ultrasonic.getLastValue() == None:
        ultrasonic.updateLastValue()
        time.sleep(1)


    while True:
        ultrasonic.updateLastValue()
        distance = ultrasonic.getLastValue()
        print("Distance: " + str(distance))

        if int(distance) > 5:
            # --- Set LED color to GREEN
            ledrgb.setGreen()
        else:
            ledrgb.setRed()
        
        time.sleep(1)

if __name__ == "__main__":
   main(sys.argv[1:])
