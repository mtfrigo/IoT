https://tutorials-raspberrypi.de/raspberry-pi-miflora-xiaomi-pflanzensensor-openhab/

https://gadget-freakz.com/product/xiaomi-mi-flora-plant-sensor/

https://www.home-assistant.io/integrations/miflora/

* **mi_flora.py** implements the connection with the device. It validates the mac, connect through BLE and polls the values from the sensors (MI_CONDUCTIVITY, MI_MOISTURE, MI_LIGHT, MI_TEMPERATURE, MI_BATTERY).
* **plant.py** is an interface that implements a Plant Class that used the script mentioned above to get the values from the sensors.

