This scripts implements the relay module plugged to a Raspi. The running exemple on the lab has a COOLER FAN connected to it.

* **relay-mqtt.py** is the script that subscribes to a topic and when receive a message it turns on or turns off the relay.

* **relay.py** is the implementation of the relay as a Class to be used by others applications.