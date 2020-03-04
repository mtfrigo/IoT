#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, getopt
import time

# --- Custom LIB imports
from LIB.plant import  PLANT
from LIB.lcd import LCD
import LIB.utils as utils

from threading import Thread

first_value_flag = False

lucky_bamboo = None
spider_plant = None
value = 1

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

def lcd_thread(lcd):

    while True:

        global value

        v = lcd.checkSwitch()

        if (v[0] == True):
            value = 1
        elif (v[1] == True):
            value = 2
        elif (v[2] == True):
            value = 3
        elif (v[3] == True):
            value = 4
            
        time.sleep(0.3)

def plants():
    global lucky_bamboo
    global spider_plant
    global first_value_flag

    while True:

        print("Updating Lucky Bamboo...")
        lucky_bamboo.updateValues()
        print("Lucky Bamboo updated!")

        print("Updating Spider Plant...")
        spider_plant.updateValues()
        print("Spider Plant updated!")

        first_value_flag = True

        
        time.sleep(5)


def main(argv):

    global lucky_bamboo
    global spider_plant
    global value
    global first_value_flag

    attb = "moisture"
    # 1 => moisture
    # 2 => temperature
    # 3 => conductivity
    # 4 => light

    lcd = LCD()

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

    buttons_thread = Thread(target=lcd_thread, args=(lcd,))
    buttons_thread.name = "LCDThread"
    buttons_thread.daemon = True

    buttons_thread.start()

    plants_thread = Thread(target=plants)
    plants_thread.name = "LCDThread"
    plants_thread.daemon = True

    plants_thread.start()
    time.sleep(5)

    while first_value_flag == False:
        time.sleep(1)

    while True:
        attb = getAttb(value)
        sigla = "M"

        values = str(spider_plant.getAttb(attb)) + "/" + str(spider_plant.MinMax[attb]['max'])

        sentence1 = attb[0:(16 - 2 - len(values))]
        sentence1 += ": "

        while 16 - (len(sentence1) + len(values)) > 0:
            sentence1 = sentence1 + " "

        sentence1 = sentence1 + values
        sentence2 = utils.getNowTime() + "  "

        print("Sentence 1: "+sentence1+"; Len: "+str(len(sentence1)))
        print("Sentence 2: "+sentence2+"; Len: "+str(len(sentence2)))

        lcd.write(sentence1 + sentence2)

        time.sleep(2)

if __name__ == "__main__":
   main(sys.argv[1:])