#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import RPi.GPIO as GPIO
import time

class BUTTON2(object):
 
    button1 = 15 # right
    button2 = 16 # left
 
    def __init__(self, button1=15, button2=16):
		# Intialize the library (must be called once before other functions).
        self.button1 = button1
        self.button2 = button2
        
        self.setup()

    def setup(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.button2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def checkButton(self, btn):
        if GPIO.input(btn) == GPIO.HIGH:
            return True
        return False

    

