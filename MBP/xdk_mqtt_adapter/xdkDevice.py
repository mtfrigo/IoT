import paho.mqtt.client as mqtt
from datetime import datetime
import time
import json
from mqttClient import mqttClient   

############################
# XDK OBject
############################
class xdkDevice(object):

   # --- Device configuration
   id = None
   sensor = None

   # --- Last value read from sensor
   lastValue = None

   # --- Addresses of broker 
   hostname_sub = None
   topic_sub = None

   # --- Instance of mqtt client to connect to broker where the sensor values are firstly sent
   subscriber = None

   def __init__(self, id, sensor, hostname="localhost", topic=None):

      self.id = id
      self.sensor = sensor
      self.lastValue = None

      self.hostname_sub = hostname
      self.topic_sub = 'XDK/' + id

      self.subscriber = self.configMqttClient()
      self.startSubscriber()

   def configMqttClient(self):
      # --- Generating a id with the current timestamp
      id_sub = "id_%s" % (datetime.utcnow().strftime('%H_%M_%S'))
      return mqttClient(self.hostname_sub, self.port_sub, id_sub)
      
   def startSubscriber(self):
      # --- Start subscriber
      self.subscriber.connect()
      self.subscriber.subscribe(topic_sub)
      self.subscriber.start()

   def getLastValue(self):
      # --- Get for last value variable
      return self.lastValue

   def updateLastValue(self):
      # --- Update the lastValue variable wih the lastValue from subscriber client
      while(self.subscriber.getLastMessage() == None):
         time.sleep(1)

      lastMessage = self.subscriber.getLastMessage()
      value = self.filterMessage(lastMessage)
      self.setLastValue(value)

   def setLastValue(self, value):
      # --- Set method for lastValue variable
      self.lastValue = value

   def filterMessage(self, message):
      # --- Get the wanted sensor value from the JSON message
      return message[self.sensor]
