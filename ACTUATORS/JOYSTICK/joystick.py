import RPi.GPIO as GPIO
import spidev
from time import sleep
from neopixel import *
  
# Initialisiere Joystick auf Analogen PINS 0 & 1
joyX = 0
joyY = 1
  
spi = spidev.SpiDev()
spi.open(0,0)
#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)
  
def readadc(adcnum):
# SPI-Daten auslesen
    r = spi.xfer2([1,8+adcnum <<4,0])
    adcout = ((r[1] &3) <<8)+r[2]
    return adcout
  
minX = 218
minY = 247
maxX = 828
maxY = 781

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

    print("Print: " + str(int(rgb*Color(255, 255, 255))))

    
    sleep(0.1)