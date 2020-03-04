#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
this script demos the graphic character LCD with 4 Buttons.
it requires the RPLCD module. install with:
sudo pip install RPLCD
sudo apt-get install espeak

"""

import sys, os

from RPLCD import CharLCD
import RPi.GPIO as GPIO
import time

TEXT_1 = "Press button two for weather forecast or button three for my CPU temperature"
TEXT_2 = "Button 2 was pressed"
TEXT_3 = "Button 3 was pressed"
TEXT_4 = "Button 4 was pressed"

def initButtons():
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(9, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def checkSwitch():
  v0 = not GPIO.input(4)
  v1 = not GPIO.input(23)
  v2 = not GPIO.input(10)
  v3 = not GPIO.input(9)
  return v3, v0, v1, v2

initButtons()
lcd = CharLCD(pin_rs=7, pin_e=8, pins_data=[17, 18, 27, 22], numbering_mode=GPIO.BCM, cols=16, rows=2, dotsize=8)
lcd.clear()
lcd.write_string('* TPL IoT Lab * > Press a button')

while (True):
  v = checkSwitch()
  #print ("Button 1: ", v[0], " Button 2: ", v[1], " Button 3: ", v[2], " Button 4: ", v[3])

  if (v[0] == True):
    os.system("espeak -ven+f5 -s130 \'" + TEXT_1 + "\' --stdout | aplay")
  elif (v[1] == True):
    TEXT_2 = os.popen("curl http://wttr.in/Stuttgart?format=\'Weather+condition+in+%l:+%C+%t\'").readline()
    os.system("espeak -ven+f5 -s130 \'" + str(TEXT_2) + "\' --stdout | aplay")
  elif (v[2] == True):
    res = os.popen('vcgencmd measure_temp').readline()
    TEXT_3 = (res.replace("temp=","My CPU temperature is ").replace("'C\n"," Celsius degrees"))
    os.system("espeak -ven+f5 -s130 \'" + TEXT_3 + "\' --stdout | aplay")
  elif (v[3] == True):
    os.system("espeak -ven+f5 -s130 \'" + TEXT_4 + "\' --stdout | aplay")

  time.sleep(0.5)

