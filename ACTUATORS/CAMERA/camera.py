import picamera
from time import sleep

width = 160
height = 128

camera = picamera.PiCamera()

def takePic(name):
    try: 
        camera.start_preview()
        sleep(1)
        camera.capture(name, resize=(width, height))
        camera.stop_preview()
        pass
    finally:
        camera.close()
        print("picture taken")