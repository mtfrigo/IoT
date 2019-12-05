#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, getopt
import paho.mqtt.client as mqtt
from datetime import datetime
import time
import json
import os, fnmatch
from os.path import expanduser

import re

from mqttClient import mqttClient
from xdkDevice import xdkDevice

def getParamValues(paramLabels, parameters):

   paramObj = {}

   #parameters = "[{\"name\":\"sensor\",\"value\":\"light\"}, {\"name\":\"id\",\"value\":\"XDK1\"}]"

   # --- Parses the JSON received as parameter to an array
   paramArray = json.loads(parameters)
   
   # --- Iterates on the array to get all the parameters
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

   # --- Get path of config file
   configFile = os.path.join(os.getcwd(), configFileName)

   # --- Checks if config file have been already created
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
def main(argv):

   # --- Constants
   pub_interval = 5 # Seconds between 2 values publish to MBP broker
   paramLabels = ['sensor', 'id']

   # --- Subcribe broker
   hostname_sub = "localhost"

   # --- Placeholders
   hostname_pub = 'localhost'
   topic_pub = 'test'

   # --- Get parameters
   paramObj = getParamValues(paramLabels, argv[0])
   sensor = paramObj['sensor']
   id = paramObj['id']

   # --- Create XDK instance
   xdk = xdkDevice(id, sensor, hostname_sub)

   # ---  Get config from connections file
   hostname_pub, topics = parseConnections("connections.txt")
   topic_pub = topics[0]
   topic_splitted = topic_pub.split('/')
   component = topic_splitted [0]
   component_id = topic_splitted [1]

   # --- Sleeps with time equals to pub_interval to make sure there is going to have some value to print
   time.sleep(pub_interval)

   # --- Start publisher
   id_pub = "id_%s" % (datetime.utcnow().strftime('%H_%M_%S'))
   publisher = mqttClient(hostname_pub, 1883, id_pub)
   publisher.connect()


   try:  
      while True:

         # --- Get timestamp
         t = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

         # --- Get last value received from XDK Device
         xdk.updateLastValue()
         value = xdk.getLastValue()

         # --- Message in JSON format
         msg_pub = {"component": component.upper(), "id": component_id, "value": "%f" % (float(value)) }

         # --- Publish the message
         publisher.sendMessage(topic_pub, json.dumps(msg_pub))

         # --- Sleeps for determined interval
         time.sleep(pub_interval)

   except:
      e = sys.exc_info()
      print ("end due to: ", str(e))
      
if __name__ == "__main__":
   main(sys.argv[1:])
