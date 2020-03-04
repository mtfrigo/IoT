import os
import time
from random import randint

from meross_iot.cloud.devices.door_openers import GenericGarageDoorOpener
from meross_iot.cloud.devices.hubs import GenericHub
from meross_iot.cloud.devices.light_bulbs import GenericBulb
from meross_iot.cloud.devices.power_plugs import GenericPlug
from meross_iot.cloud.devices.subdevices.thermostats import ValveSubDevice, ThermostatV3Mode
from meross_iot.manager import MerossManager
from meross_iot.meross_event import MerossEventType

EMAIL = "matheus.tfrigo@gmail.com"
PASSWORD = "p9x3rvsj4"

import paho.mqtt.client as mqtt
from datetime import datetime
import json

############################
# MQTT Client
############################
class Client(object):
   # --- Placeholders
   hostname = 'localhost'
   port = 1883
   clientid = ''

   # --- Last message received from subscribed channel
   #     Useful just when using a Subscriber
   lastMessage = None

   def __init__(self, hostname, port, clientid, plug):
      self.hostname = hostname
      self.port = port
      self.clientid = clientid

      self.lastMessage = None

      self.plug = plug

      self.state = 0

      # create MQTT client and set user name and password 
      self.client = mqtt.Client(client_id=self.clientid, clean_session=True, userdata=None, protocol=mqtt.MQTTv31)
      #client.username_pw_set(username="use-token-auth", password=mq_authtoken)

      # set mqtt client callbacks
      self.client.on_connect = self.on_connect
      self.client.on_message = self.on_message

   # The callback for when the client receives a CONNACK response from the server.
   def on_connect(self, client, userdata, flags, rc):
      print("[" + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + "]: " + "ClientID: " + self.clientid + "; Connected with result code " + str(rc))

   # --- Callback when a message has been received on the subscribed topic
   def on_message(self, client, userdata, message):
      # --- Parse message to JSON

      print("oioioi")
      if self.state == 0:
          self.state = 1
          self.state = play(self.plug)

      # --- Set last messave received
      self.setLastMessage(parsed_json)

   def setLastMessage(self, message):
      self.lastMessage = message

   def getLastMessage(self):
      return self.lastMessage

   # publishes message to MQTT broker
   def sendMessage(self, topic, msg):
      self.client.publish(topic=topic, payload=msg, qos=0, retain=False)
      print(msg)

   def subscribe(self, topic):
      self.client.subscribe(topic)

   def connect(self):
      self.client.connect(self.hostname, self.port, 60)

   # connects to MQTT Broker
   def start(self):
      #runs a thread in the background to call loop() automatically.
      #This frees up the main thread for other work that may be blocking.
      #This call also handles reconnecting to the broker.
      #Call loop_stop() to stop the background thread.
      self.client.loop_start()

   

def event_handler(eventobj):
    if eventobj.event_type == MerossEventType.DEVICE_ONLINE_STATUS:
        print("Device online status changed: %s went %s" % (eventobj.device.name, eventobj.status))
        pass

    elif eventobj.event_type == MerossEventType.DEVICE_SWITCH_STATUS:
        print("Switch state changed: Device %s (channel %d) went %s" % (eventobj.device.name, eventobj.channel_id,
                                                                        eventobj.switch_state))
    elif eventobj.event_type == MerossEventType.CLIENT_CONNECTION:
        print("MQTT connection state changed: client went %s" % eventobj.status)

        # TODO: Give example of reconnection?

    elif eventobj.event_type == MerossEventType.GARAGE_DOOR_STATUS:
        print("Garage door is now %s" % eventobj.door_state)

    elif eventobj.event_type == MerossEventType.THERMOSTAT_MODE_CHANGE:
        print("Thermostat %s has changed mode to %s" % (eventobj.device.name, eventobj.mode))

    elif eventobj.event_type == MerossEventType.THERMOSTAT_TEMPERATURE_CHANGE:
        print("Thermostat %s has revealed a temperature change: %s" % (eventobj.device.name, eventobj.temperature))

    else:
        print("Unknown event!")

print(EMAIL, PASSWORD)

def play(tpl_plug):
    # ---------------------------
    # Let's play with smart plugs
    # ---------------------------

    if tpl_plug.online :

        print("Let's play with smart plug %s" % tpl_plug.name)

        channels = len(tpl_plug.get_channels())
        print("The plug %s supports %d channels." % (tpl_plug.name, channels))
        for i in range(0, channels):
            print("Turning on channel %d of %s" % (i, tpl_plug.name))
            tpl_plug.turn_on_channel(i)

            time.sleep(3)

            print("Turning off channel %d of %s" % (i, tpl_plug.name))
            tpl_plug.turn_off_channel(i)

        usb_channel = tpl_plug.get_usb_channel_index()
        if usb_channel is not None:
            print("Awesome! This device also supports USB power.")
            tpl_plug.enable_usb()
            time.sleep(1)
            tpl_plug.disable_usb()

        if tpl_plug.supports_electricity_reading():
            print("Awesome! This device also supports power consumption reading.")
            print("Current consumption is: %s" % str(tpl_plug.get_electricity()))
    else: 
        print("The plug %s seems to be offline. Cannot play with that..." % tpl_plug)

    return 0

if __name__ == '__main__':
    # Initiates the Meross Cloud Manager. This is in charge of handling the communication with the remote endpoint
    manager = MerossManager(meross_email="matheus.tfrigo@gmail.com", meross_password="p9x3rvsj4")

    # Register event handlers for the manager...
    manager.register_event_handler(event_handler)

    # Starts the manager
    manager.start()

    # You can retrieve the device you are looking for in various ways:
    # By kind
    plugs = manager.get_devices_by_kind(GenericPlug)
    all_devices = manager.get_supported_devices()

    tpl_plug = manager.get_device_by_name("TPL 01")

    # --- Broker 
    broker_ip = "129.69.209.78"
    broker_port = 1883

    id = "id_%s" % (datetime.utcnow().strftime('%H_%M_%S'))

    mqtt = Client(broker_ip, broker_port, id, tpl_plug)
    mqtt.connect()
    mqtt.subscribe("movement")
    mqtt.start()


    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        print("We are done playing. Cleaning resources...")
        manager.stop()


    # At this point, we are all done playing with the library, so we gracefully disconnect and clean resources.
    

    print("Bye bye!")