"""
write state for relay

"""
import RPi.GPIO as GPIO
import time

relayPin = 14 # relay connected to D27

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relayPin, GPIO.OUT)

def play():
	GPIO.output(relayPin, GPIO.HIGH)
	time.sleep(10)
	GPIO.output(relayPin, GPIO.LOW)
	time.sleep(10)
