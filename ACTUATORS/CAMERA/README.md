# Camera

This folder has scripts to take a picture with the camera module plugged on a Raspberry Pi, encode the image, send to an endpoint, receive and decode the image file.

https://www.amazon.de/SainSmart-Fish-Eye-Camera-Raspberry-Arduino/dp/B00N1YJKFS

## Producer 
* **image.py** is the main script. It calls the other scripts. 

To use this script you need to call it sending the filename you want the image to have. E.g.: 'python2 image.py image.jpg'. And you need to specify the address where you want to send the image (line number 5). 

First the picture is taken and saved with the specified name.
Then the file is encoded.
Finally the encoded file is sent to the desired host.

* **camera.py** is the module responsible for the camera manipulation.

* **decode.py** is the module responsible for encoding the image file.

* **send.py** is the module responsible for split the encoded image file into several packets and send all of them to the desired endpoit.

* **mqttClient.py** is the default mqtt script from the lib. It implements the mqtt connection the send.py script needs to connect to the broker.

## Consumer

* **receive.py** is the main script on the Consumer side. It subscribes to a broker where the packets (several parts of the encoded image) are sent, put it together, convert to a jpg, and show on the LCD display.

* **mqttClient2.py** is the default mqtt script from the lib with some modifications. It implements the mqtt connection the receive.py script needs to subscribe to the broker.

## Adapter

* **camera_adapter.py** is the camera script that works with the MBP platform. It is explained here [MBP Camera Adapter](../../MBP/camera_adapter)