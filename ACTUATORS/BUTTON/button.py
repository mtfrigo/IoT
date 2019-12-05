import RPi.GPIO as GPIO
import time
from subprocess import Popen, PIPE
 
#Initialisiere LED auf Digital-PIN 4 und Button auf Digital-PIN 15 & 16
button1 = 15 # right
button2 = 16 # left
 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

camera_script_pid = None
camera_script_path = '../CAMERA/image.py'

led_script_pid = None
led_script_path = 'strandtest.py'

def camera_shot():
    if(camera_script_pid == None or camera_script_pid.poll() != None):
        camera_script_pid = Popen(['python2', camera_script_path, 'image.jpg'], stdout=PIPE, bufsize=0)

def led_blink():
    if(led_script_pid == None or led_script_pid.poll() != None):
        led_script_pid = Popen(['python', led_script_path], stdout=PIPE, bufsize=0)
 
while True:
    if GPIO.input(button1) == GPIO.HIGH:
        camera_shot()
        time.sleep(1)
    if GPIO.input(button2) == GPIO.HIGH:
        led_blink()
        time.sleep(1)