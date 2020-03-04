import RPi.GPIO as GPIO
import time

SENSOR_PIN = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

def movement(channel):
    print("There was movement!")


try: 
    GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, callback = movement)

    while True:
        print("sleeping for 5 sec")
        time.sleep(5)

except KeyboardInterrupt:
    print('Program was terminated.')

GPIO.cleanup()
