#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

class RELAY(object):

	relayPin = 14 # relay connected to D27

	def __init__(self, relayPin=14): 

		self.relayPin = relayPin

		self.init()

	def init(self):
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.relayPin, GPIO.OUT)

	def turnOn(self):
		GPIO.output(self.relayPin, GPIO.HIGH)

	def turnOff(self):
		GPIO.output(self.relayPin, GPIO.LOW)

	def play(self, sec):
		self.turnOn()
		time.sleep(sec)
		self.turnOff()
		time.sleep(sec)
