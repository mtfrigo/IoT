#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, getopt
import time

lucky_bamboo = None
spider_plant = None
value = 1

ledbar1 = None
ledbar2 = None


# --- Custom LIB imports
from LIB.ledbar import LEDBAR
from LIB.plant import  PLANT
from LIB.button2 import BUTTON2

from threading import Thread


def getAttb(value):
    if value == 1:
        attb = "moisture"
    elif value == 2:
        attb = "temperature"
    elif value == 3:
        attb = "conductivity"
    elif value == 4:
        attb = "light"
        
    return attb

def updateLedBar():
    global value
    global lucky_bamboo
    global spider_plant
    global ledbar1
    global ledbar2

    print(value)

    attb = getAttb(value)

    rel_value = lucky_bamboo.getRelativeValue(attb, lucky_bamboo.getAttb(attb))
    rounded_value = int(round(rel_value/10, 0))

    print(attb, rel_value, rounded_value)

    ledbar1.sendInteger(rounded_value)

    rel_value = spider_plant.getRelativeValue(attb, spider_plant.getAttb(attb))
    rounded_value = int(round(rel_value/10, 0))

    ledbar2.sendInteger(rounded_value)



def checkButtons(btn, btn1, btn2):
    global value
    while True:
        if btn.checkButton(btn1):
            if(value < 4):
                value = value + 1
            updateLedBar()
            time.sleep(1)
        elif btn.checkButton(btn2):
            if(value > 1):
                value = value - 1
            updateLedBar()
            time.sleep(1)
            

def main(argv):

    global value

    global lucky_bamboo
    global spider_plant

    global ledbar1
    global ledbar2

    attb = "moisture"
    # 1 => moisture
    # 2 => temperature
    # 3 => conductivity
    # 4 => light

    ledbar1 = LEDBAR(12,13)
    ledbar2 = LEDBAR(26,27)

    ledbar1.setup()
    ledbar2.setup()

    btn1 = 15
    btn2 = 16

    buttons = BUTTON2(btn1, btn2)

    lucky_bamboo = PLANT("C4:7C:8D:66:B0:15")
    spider_plant = PLANT("C4:7C:8D:66:AE:35")

    lucky_bamboo.setMinMax(15, 60, 'moisture')
    lucky_bamboo.setMinMax(350, 2000, 'conductivity')
    lucky_bamboo.setMinMax(800, 25000, 'light')
    lucky_bamboo.setMinMax(10, 32, 'temperature')

    spider_plant.setMinMax(15, 60, 'moisture')
    spider_plant.setMinMax(200, 1300, 'conductivity')
    spider_plant.setMinMax(500, 30000, 'light')
    spider_plant.setMinMax(10, 32, 'temperature')

    buttons_thread = Thread(target=checkButtons, args=(buttons, btn1, btn2))
    buttons_thread.name = "ButtonsThread"
    buttons_thread.daemon = True

    buttons_thread.start()
    time.sleep(2)

    while True:

        print("Updating Lucky Bamboo...")
        lucky_bamboo.updateValues()
        print("Lucky Bamboo updated!")

        print("Updating Spider Plant...")
        spider_plant.updateValues()
        print("Spider Plant updated!")

        updateLedBar()
        
        time.sleep(5)

if __name__ == "__main__":
   main(sys.argv[1:])