import RPi.GPIO as GPIO
import spidev
from time import sleep
from neopixel import *
import sys, getopt

from LIB.ledrgb import LED

def main(argv):
    
    # Initialisiere Joystick auf Analogen PINS 0 & 1
    joyX = 0
    joyY = 1
    
    spi = spidev.SpiDev()
    spi.open(0,0)
    #GPIO.setwarnings(False)
    #GPIO.setmode(GPIO.BCM)

    ledrgb = LED(19)
    ledrgb.setBlue()
    
    def readadc(adcnum):
    # SPI-Daten auslesen
        r = spi.xfer2([1,8+adcnum <<4,0])
        adcout = ((r[1] &3) <<8)+r[2]
        return adcout
    
    minX = 218
    minY = 247
    maxX = 828
    maxY = 781

    colors = [
        Color(0,0,128),
        Color(0,0,255),
        Color(0,128,0),
        Color(0,128,128),
        Color(0,255,0),
        Color(0,255,128),
        Color(0,255,255),
        Color(128,0,0),
        Color(128,0,128),
        Color(128,0,255),
        Color(128,128,0),
        Color(128,128,128),
        Color(128,128,255),
        Color(128,255,0),
        Color(128,255,128),
        Color(128,255,255),
        Color(255,0,0),
        Color(255,0,128),
        Color(255,0,255),
        Color(255,128,0),
        Color(255,128,128),
        Color(255,128,255),
        Color(255,255,0),
        Color(255,255,128),
        Color(255,255,255)
    ]

    sleep(2)

    lastValue = 999

    

    while True:
        x = readadc(joyX)
        y = readadc(joyY)

        if(x > 1000):
            print("Joystick gedrueckt")
        else:
            if x > maxX:
                maxX = x
            if x < minX:
                minX = x
            if y > maxY:
                maxY = y
            if y < minY:
                minY = y

        normalizedX = (x - minX) / (maxX - minX)
        normalizedY = (y - minY) / (maxY - minY)

        rgb = normalizedX*normalizedY

        #print("Print: " + str(int(rgb*Color(255, 255, 255))))
        #color = int(rgb*Color(255, 255, 255))
        #r = int(color / 65536)
        #g = int((color % 65536) / 256)  
        #b = int((color % 65536) % 256)
        

        color_index = int(round(rgb*len(colors)))

        #ledrgb.setColor(Color(r,g,b))
        #print(Color(r,g,b))

        print("X: " + str(x) + "; Y: " + str(y) + "; Color: " + str(color_index))
        color = colors[color_index]
        '''
        if lastValue != color:
            lastValue = color
            if rgb == 0:
                ledrgb.setColor(Color(0,0,0))
            elif rgb == 1:
                ledrgb.setColor(Color(0,0,255))
            elif rgb == 2:
                ledrgb.setColor(Color(0,255,0))
            elif rgb == 3:
                ledrgb.setColor(Color(255,0,0))
            elif rgb == 4:
                ledrgb.setColor(Color(0,255,255))
            elif rgb == 5:
                ledrgb.setColor(Color(255,0,255))
            elif rgb == 6:
                ledrgb.setColor(Color(255,255,0))
            elif rgb == 7:
                ledrgb.setColor(Color(255,255,255))
        
        '''
        ledrgb.setColor(color)
        
        sleep(0.5)

if __name__ == "__main__":
   main(sys.argv[1:])