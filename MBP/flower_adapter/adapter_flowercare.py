#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, fnmatch
import sys, getopt
import json
from os.path import expanduser
from datetime import datetime
import time
import re

# --- Custom LIB imports
from plant import  PLANT
import utils as utils

############################
# MQTT Client
############################
class mqttClient(object):
   hostname = 'localhost'
   port = 1883
   clientid = ''

   def __init__(self, hostname, port, clientid):
      self.hostname = hostname
      self.port = port
      self.clientid = clientid

      # create MQTT client and set user name and password 
      self.client = mqtt.Client(client_id=self.clientid, clean_session=True, userdata=None, protocol=mqtt.MQTTv31)
      #client.username_pw_set(username="use-token-auth", password=mq_authtoken)

      # set mqtt client callbacks
      self.client.on_connect = self.on_connect

   # The callback for when the client receives a CONNACK response from the server.
   def on_connect(self, client, userdata, flags, rc):
      print("[" + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + "]: " + "ClientID: " + self.clientid + "; Connected with result code " + str(rc))

   # publishes message to MQTT broker
   def sendMessage(self, topic, msg):
      self.client.publish(topic=topic, payload=msg, qos=0, retain=False)
      print(msg)

   # connects to MQTT Broker
   def start(self):
      self.client.connect(self.hostname, self.port, 60)

      #runs a thread in the background to call loop() automatically.
      #This frees up the main thread for other work that may be blocking.
      #This call also handles reconnecting to the broker.
      #Call loop_stop() to stop the background thread.
      self.client.loop_start()

############################
# MAIN
############################
def main(argv):

   sensor = None
   mac = None

   paramArray = json.loads(argv[0])
   for param in paramArray:
      if not ('name' in param and 'value' in param):
         continue
      elif param["name"] == "mac":
         mac = param["value"]
      elif param["name"] == "sensor":
         sensor = param["value"]
   

   configFileName = "connections.txt"
   topics = []
   brokerIps = []
   configExists = False

   configFile = os.path.join(os.getcwd(), configFileName)

   while (not configExists):
       configExists = os.path.exists(configFile)
       time.sleep(1)

   # BEGIN parsing file
   fileObject = open (configFile)
   fileLines = fileObject.readlines()
   fileObject.close()

   for line in fileLines:
       pars = line.split('=')
       topic = pars[0].strip('\n').strip()
       ip = pars[1].strip('\n').strip()
       topics.append(topic)
       brokerIps.append(ip)

   # END parsing file
       
   hostname = brokerIps [0]
   topic_pub = topics [0]
   topic_splitted = topic_pub.split('/')
   component = topic_splitted [0]
   component_id = topic_splitted [1]
   
   print("Connecting to: " + hostname + " pub on topic: " + topic_pub)
   
   # --- Begin start mqtt client
   id = "id_%s" % (datetime.utcnow().strftime('%H_%M_%S'))
   publisher = mqttClient(hostname, 1883, id)
   publisher.start()

   plant_entity = PLANT(mac)
   plant_entity.updateValues()
   
   try:  
      while True:
         # messages in json format
         # send message, topic: temperature
         t = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

         msg_pub = {"component": component.upper(), "id": component_id, "value": "%f" % (float(plant_entity.getAttb(sensor))) }
         publisher.sendMessage (topic_pub, json.dumps(msg_pub))

         time.sleep(15)

   except:
      e = sys.exc_info()
      print ("end due to: ", str(e))
      
if __name__ == "__main__":
   #main()
   main(sys.argv[1:])
