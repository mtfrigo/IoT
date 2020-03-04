#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import requests 
from signal import *

from http import Http

class ESP12e_Push(object):
    created_at = None

    # --- MQTT config
    broker_ip = None
    broker_port = None
    topic = None

    # --- HTTP handler
    httpClient = None

    # --- Placeholder
    esp_ip = "129.69.209.118"


    def __init__(self, esp_ip, broker_ip, broker_port, topic):
        self.created_at = self.getNowTime()

        self.updateConfig(esp_ip, broker_ip, broker_port, topic)

        self.httpClient = Http()

    def updateConfig(self, esp_ip, broker_ip, broker_port, topic):
        self.esp_ip = esp_ip
        self.broker_ip = broker_ip
        self.broker_port = broker_port
        self.topic = topic

    def sendConfig(self):
        data = '{"ip": "'+self.broker_ip+'", "topic": "'+self.topic+'"}"'
        # --- Model for messaging directly with MBP
        #data = '{"ip": "'+self.broker_ip+'", "topic": "'+self.topic+'","component": "'+component+'","componentId": "'+component_id+'","status": "'+status+'"}"'

        httpClient.sendRequest(esp_ip, 80, "config", data)

    def sendStatus(self, status):
        data = "{'status': '"+status+"'}"
        httpClient.sendRequest(esp_ip, 80, "status", data)

    def start(self):
        self.sendConfig()
        self.turnOn()

    def turnOff(self):
        self.sendStatus(0)

    def turnOn(self):
        self.sendStatus(1)

    def clean(*args):
        self.turnOff()
        data = "{'status': '"+status+"'}"
        #sendConfig(esp_ip, "localhost", "sensor/123412341234123412341234", "sensor", "123412341234123412341234", "0")
        sys.exit(0)

    

    