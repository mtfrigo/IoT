from LIB.mqtt import Client as mqttClient

import RPi.GPIO as GPIO
import time

import sys, getopt
from datetime import datetime
import time

def main(argv):

    # --- Broker 
    broker_ip = "129.69.209.78"
    broker_port = 1883
    topic = "movement"

    id = "id_%s" % (datetime.utcnow().strftime('%H_%M_%S'))

    mqtt = mqttClient(broker_ip, broker_port, id)
    mqtt.connect()

    SENSOR_PIN = 4
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SENSOR_PIN, GPIO.IN)

    
    mqtt.sendMessage("movement", "1")

    def movement(channel):
        mqtt.sendMessage("movement", "1")
        print("Movement detection sent")


    try: 
        GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, callback = movement)

        while True:
            time.sleep(5)

    except KeyboardInterrupt:
        print('Program was terminated.')

    GPIO.cleanup()


if __name__ == "__main__":
   main(sys.argv[1:])
