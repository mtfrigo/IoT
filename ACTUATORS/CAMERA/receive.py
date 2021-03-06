import math
import random, string
import json
import paho.mqtt.client as mqtt
import time
from datetime import datetime
import base64
import subprocess
from mqttClient2 import mqttClient

class FileHandler(object):
    file = None
    encoded_filename = "encoded_image.txt"
    decoded_image_file = 'some_image.jpg'

    def __init__(self, filepath):
        self.file = None
        self.encoded_filename = filepath
    
    def open_file(self):
        self.file = open("encoded_image.txt","w+")

    def write_file(self):
            self.file = open(self.encoded_filename,"w+")

    def read_file(self):
        content = ""

        self.file = open(self.encoded_filename,"r")
        if self.file.mode == "r":
            content = self.file.read()
            
        self.file.close()

        return content

    def close_file(self):
        self.file.close()

    def convert_base64_jpg(self):
        imgdata = base64.b64decode(self.read_file())
        filename = self.decoded_image_file  # I assume you have a way of picking unique filenames
        with open(filename, 'wb') as f:
            f.write(imgdata)

    def receive_packet(self, parsed_message):

        #print(parsed_message)
        if(parsed_message['pos'] == 0):
            print("First packet")
            self.open_file()
        
        print (parsed_message['pos'])
        print (parsed_message['size'])
        self.file.write(parsed_message['data'])
        
        if(parsed_message['pos'] == (parsed_message['size'] - 1)):
            self.close_file()
            print("Converting base64 to jpg...")
            self.convert_base64_jpg()
            print("Updating Display...")
            #self.script_process = Popen(['python2', 'image.py', 'image.jpg'], stdout=PIPE, bufsize=0)
            subprocess.call(["sudo fbi -d /dev/fb1 -T 1 -noverbose -a some_image.jpg"], shell=True)
            print("Done!")

def main():
    
    file_handler = FileHandler("encoded_image.txt")
    id = "id_%s" % (datetime.utcnow().strftime('%H_%M_%S'))
    
    client = mqttClient("129.69.209.92", 1883, id, file_handler)
    client.connect()
    client.subscribe("image")
    client.start()

    try:
      while(True):
        time.sleep(5)
    except KeyboardInterrupt:
        client.stop()
        client.file_handler.close_file()

if __name__ == "__main__":
   main()
