import RPi.GPIO as GPIO
import time
from subprocess import Popen, PIPE
from LIB.mqtt import Client as mqttClient
 
button1 = 15
button2 = 16
 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# --- Config
broker_relay = "129.69.209.78"
hostname = "129.69.209.78"
port = 1883
id = "button_relay"

# --- Create and initialize MQTT client
mqttClient = mqttClient(broker_relay, port, id)
mqttClient.connect()
mqttClient.start()
 
while True:
    if GPIO.input(button1) == GPIO.HIGH:
        Popen(['python2', '../CAMERA/image.py', 'image.jpg'], stdout=PIPE, bufsize=0)
        time.sleep(10)
    if GPIO.input(button2) == GPIO.HIGH:
        mqttClient.sendMessage("relay", 1)
        time.sleep(10)