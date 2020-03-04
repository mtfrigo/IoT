import sys
import time  
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler  
import datetime
import RPi.GPIO as GPIO
import tm1637
import os
import subprocess
import json
 
Display = tm1637.TM1637(4,5,tm1637.BRIGHT_TYPICAL)
 
Display.Clear()
Display.SetBrightnes(1)

known_devices = {}
unknown_devices = []
connected_devices = []

json_devices_file = '/var/www/html/devices/devices.json'
devices_dir = "/var/www/html/devices"

class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.json"]

    def process(self, event):
        """
        event.event_type 
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed there
        #print event.src_path, event.event_type  # print now only for degug
        readJSON()

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

def readJSON():
   #prompt the user for a file to import
   with open(json_devices_file) as json_file:

      data = json.load(json_file)

      for d in data['known']:
         if(not(d in known_devices)):
            data['known'][d]['isNew'] = True
            known_devices[d] = data['known'][d]

      for d in known_devices.keys():
         if(not(d in data['known'])):
            known_devices.pop(d)

      for d in data['unknown']:
         if(not(d in unknown_devices)):
            unknown_devices.append(d)

      for index, d in enumerate(unknown_devices):
         if(not(d in data['unknown'])):
            unknown_devices.remove(d)

      for d in data['connected']:
         if(not(d in connected_devices)):
            connected_devices.append(d)

      for index, d in enumerate(connected_devices):
         if(not(d in data['connected'])):
            connected_devices.remove(d)

      json_file.close()

def writeJSON(mac):

   with open(json_devices_file) as json_file:

      data = json.load(json_file)

      aux = data['unknown']
      aux.append(mac)
      unknown_devices = aux
      data['unknown'] = aux
      json_file.close()

   with open(json_devices_file, 'w') as outfile:
      json.dump(data, outfile)

def updateConnectedDevicesJSON(macs):
   with open(json_devices_file) as json_file:

      data = json.load(json_file)
      data['connected'] = macs
      json_file.close()

   with open(json_devices_file, 'w') as outfile:
      json.dump(data, outfile)

def checkIfConnectedDevicesChanged(aux):
   changed = False
   for mac in aux:
      if(not(mac in connected_devices)):
         changed = True

   for mac in connected_devices:
      if(not(mac in aux)):
         changed = True

   if(changed):
      #print("mudou!!!")
      updateConnectedDevicesJSON(aux)

def main():
   counter = 0

   readJSON()

   observer = Observer()
   observer.schedule(MyHandler(), path=devices_dir)
   observer.start()

   try:
      while(True):
         data = [ 0, 0, int(counter/10), counter%10 ]
      
         Display.Show(data)
         Display.ShowDoublepoint(0)

         #os.system("sudo iw wlan0 station dump")
         raw_dump = subprocess.check_output(["iw", "wlan0", "station", "dump"])

         dump_split = (raw_dump.split())
         counter = 0

         aux_connected_devices = []

         for index, string in enumerate(dump_split) :
            if(string == "Station"):
               counter = counter + 1

               aux_connected_devices.append(dump_split[index+1])

               if(dump_split[index+1] in known_devices):
                  if(known_devices[dump_split[index+1]]['isNew']):
                     print(known_devices[dump_split[index+1]]['owner'])
                     known_devices[dump_split[index+1]]['isNew'] = False
                     #subprocess.call(["espeak -s100 -vf5 'Welcome, "+known_devices[dump_split[index+1]]['owner']+"'"], shell=True)
               
               elif(not(dump_split[index+1] in unknown_devices)):
                  writeJSON(dump_split[index+1])

         checkIfConnectedDevicesChanged(aux_connected_devices)

         for device in known_devices:
            if(not(device in aux_connected_devices)):
               known_devices[device]["isNew"] = True

         time.sleep(5)
   except KeyboardInterrupt:
      observer.stop()

   observer.join()
   

if __name__ == "__main__":
   main()
 
