#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, getopt
import paho.mqtt.client as mqtt
from datetime import datetime
import time
import json
import os, fnmatch
from os.path import expanduser
import random

import re

from mqttClient import mqttClient


from threading import Thread

def getParamValues(paramLabels, parameters):

   paramObj = {}

   paramArray = json.loads(parameters)
   for param in paramArray:
      if not ('name' in param and 'value' in param):
          continue
      elif param["name"] in paramLabels:
         paramObj[param["name"]] = param["value"]
      else:
         paramObj[param["name"]] = None

   return paramObj

def parseConnections(configFileName):

   topics = []
   brokerIps = []
   configExists = False

   configFile = os.path.join(os.getcwd(), configFileName)

   while (not configExists):
       configExists = os.path.exists(configFile)
       time.sleep(1)

   # --- Begin parsing file
   fileObject = open (configFile)
   fileLines = fileObject.readlines()
   fileObject.close()

   for line in fileLines:
       pars = line.split('=')
       topic = pars[0].strip('\n').strip()
       ip = pars[1].strip('\n').strip()
       topics.append(topic)
       brokerIps.append(ip)

   return brokerIps[0], topics

############################
# MAIN
############################
def main():

   # --- Constants
   pub_interval = 5 # Seconds between 2 values publish to MBP broker
   paramLabels = ['sensor', 'axis', 'id']
   topic_sub = 'XDK'

   # --- Placeholders
   hostname = 'localhost'
   topic_pub = 'test'

   # --- Get parameters
   paramObj = getParamValues(paramLabels, argv[0])
   sensor = paramObj.sensor
   if 'axis' in paramObj:
      axis = paramObj.axis

   # --- Begin start mqtt client
   id = "id_%s" % (datetime.utcnow().strftime('%H_%M_%S'))
   subscriber = mqttClient("localhost", 1883, id)
   subscriber.setSubTopic(topic_sub)
   subscriber.setSensor(sensor) 

   # ---  Get config from connections file
   hostname, topics = parseConnections("connections.txt")
   topic_pub = topics[0]
   topic_splitted = topic_pub.split('/')
   component = topic_splitted [0]
   component_id = topic_splitted [1]

   # --- Start subscriber
   subscriber.connect()
   subscriber.subscribe()
   subscriber.start()

   time.sleep(5.0)

   # --- Start publisher
   id = "id_%s" % (datetime.utcnow().strftime('%H_%M_%S'))
   publisher = mqttClient(hostname, 1883, id)
   publisher.connect()

   try:  
      while True:
         # messages in json format

         t = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

         value = subscriber.getLastValue()

         msg_pub = {"component": component.upper(), "id": component_id, "value": "%f" % (float(value)) }
         publisher.sendMessage(topic_pub, json.dumps(msg_pub))

         time.sleep(pub_interval)

   except:
      e = sys.exc_info()
      print ("end due to: ", str(e))
      
if __name__ == "__main__":
   main()
