#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import paho.mqtt.client as mqtt
from datetime import datetime
import time
import json
import os

from LIB.mqtt import Client as mqttClient
from LIB.relay import RELAY
import LIB.utils as utils

def main(argv):
    # --- Broker configuration
    broker_ip = "129.69.209.78"
    broker_port = 1883
    topic = "relay"
    id = utils.createNewId()

    # --- Relay component configuration
    RELAY_PIN = 14
    relay = RELAY(RELAY_PIN)

    # --- Subscriber initialization
    mqtt = mqttClient(broker_ip, broker_port, id)
    mqtt.connect()
    mqtt.subscribe(topic)
    mqtt.start()

    while True:
        if(mqtt.getLastMessage()):
            relay.turnOn()
            print("turn on!")
            time.sleep(9)
            relay.turnOff()
            mqtt.lastMessage = 0
            print("turn off!")
        time.sleep(1)

if __name__ == "__main__":
   main(sys.argv[1:])