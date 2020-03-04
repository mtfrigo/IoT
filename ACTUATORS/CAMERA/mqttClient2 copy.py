import paho.mqtt.client as mqtt
from datetime import datetime
import json

############################
# MQTT Client
############################

class FileHandler(object):
    

    def __init__(self):
        self.file = None

    



class mqttClient(object):
   hostname = 'localhost'
   port = 1883
   clientid = ''

   lastMessage = None

   file = None

   encoded_filename = "encoded_image.txt"
   decoded_image_file = 'some_image.jpg'

   

   def __init__(self, hostname, port, clientid):
      self.hostname = hostname
      self.port = port
      self.clientid = clientid

      self.file_handler = FileHandler()

      self.lastMessage = None

      # create MQTT client and set user name and password 
      self.client = mqtt.Client(client_id=self.clientid, clean_session=True, userdata=None, protocol=mqtt.MQTTv31)
      #client.username_pw_set(username="use-token-auth", password=mq_authtoken)

      # set mqtt client callbacks
      self.client.on_connect = self.on_connect
      self.client.on_message = self.on_message

   def open_file(self):
      self.file = open("encoded_image.txt","w+")

   def close_file(self):
      self.file.close()

   # The callback for when the client receives a CONNACK response from the server.
   def on_connect(self, client, userdata, flags, rc):
      print("[" + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + "]: " + "ClientID: " + self.clientid + "; Connected with result code " + str(rc))


   def convert_base64_jpg(self):
        imgdata = base64.b64decode(self.read_file())
        filename = decoded_image_file  # I assume you have a way of picking unique filenames
        with open(filename, 'wb') as f:
            f.write(imgdata)

   # --- Callback when a message has been received on the subscribed topic
   def on_message(self, client, userdata, message):
      parsed_json = json.loads(message.payload)
      
      self.receive_packet(parsed_json)

   def setLastMessage(self, message):
      self.lastMessage = message

   def getLastMessage(self):
      return self.lastMessage

   # publishes message to MQTT broker
   def sendMessage(self, topic, msg):
      self.client.publish(topic=topic, payload=msg, qos=0, retain=False)
      print(msg)

   def subscribe(self, topic):
      self.client.subscribe(topic)

   def connect(self):
      self.client.connect(self.hostname, self.port, 60)

   # connects to MQTT Broker
   def start(self):
      #runs a thread in the background to call loop() automatically.
      #This frees up the main thread for other work that may be blocking.
      #This call also handles reconnecting to the broker.
      #Call loop_stop() to stop the background thread.
      self.client.loop_start()

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
      filename = decoded_image_file  # I assume you have a way of picking unique filenames
      with open(filename, 'wb') as f:
         f.write(imgdata)

   def receive_packet(receive_packet):

      if(receive_packet['pos'] == 0):
         print("First packet")
         self.open_file()
      
      print (receive_packet['pos'])
      print (receive_packet['size'])
      self.file.write(receive_packet['data'])

      if(receive_packet['pos'] == receive_packet['size']):
         self.close_file()
         print("Converting base64 to jpg...")
         self.convert_base64_jpg()
         print("Updating Display...")
         #self.script_process = Popen(['python2', 'image.py', 'image.jpg'], stdout=PIPE, bufsize=0)
         subprocess.call(["sudo fbi -d /dev/fb1 -T 1 -noverbose -a some_image.jpg"], shell=True)
         print("Done!")
   