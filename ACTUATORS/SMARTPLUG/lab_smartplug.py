import os
import time
from random import randint

from meross_iot.cloud.devices.door_openers import GenericGarageDoorOpener
from meross_iot.cloud.devices.hubs import GenericHub
from meross_iot.cloud.devices.light_bulbs import GenericBulb
from meross_iot.cloud.devices.power_plugs import GenericPlug
from meross_iot.cloud.devices.subdevices.thermostats import ValveSubDevice, ThermostatV3Mode
from meross_iot.manager import MerossManager
from meross_iot.meross_event import MerossEventType

EMAIL = "matheus.tfrigo@gmail.com"
PASSWORD = "*********"

#sudo pip3 install meross_iot

def event_handler(eventobj):
    if eventobj.event_type == MerossEventType.DEVICE_ONLINE_STATUS:
        print("Device online status changed: %s went %s" % (eventobj.device.name, eventobj.status))
        pass

    elif eventobj.event_type == MerossEventType.DEVICE_SWITCH_STATUS:
        print("Switch state changed: Device %s (channel %d) went %s" % (eventobj.device.name, eventobj.channel_id,
                                                                        eventobj.switch_state))
    elif eventobj.event_type == MerossEventType.CLIENT_CONNECTION:
        print("MQTT connection state changed: client went %s" % eventobj.status)

        # TODO: Give example of reconnection?

    elif eventobj.event_type == MerossEventType.GARAGE_DOOR_STATUS:
        print("Garage door is now %s" % eventobj.door_state)

    elif eventobj.event_type == MerossEventType.THERMOSTAT_MODE_CHANGE:
        print("Thermostat %s has changed mode to %s" % (eventobj.device.name, eventobj.mode))

    elif eventobj.event_type == MerossEventType.THERMOSTAT_TEMPERATURE_CHANGE:
        print("Thermostat %s has revealed a temperature change: %s" % (eventobj.device.name, eventobj.temperature))

    else:
        print("Unknown event!")

print(EMAIL, PASSWORD)

if __name__ == '__main__':
    # Initiates the Meross Cloud Manager. This is in charge of handling the communication with the remote endpoint
    manager = MerossManager(meross_email="matheus.tfrigo@gmail.com", meross_password="********")

    # Register event handlers for the manager...
    manager.register_event_handler(event_handler)

    # Starts the manager
    manager.start()

    # You can retrieve the device you are looking for in various ways:
    # By kind
    plugs = manager.get_devices_by_kind(GenericPlug)
    all_devices = manager.get_supported_devices()

    tpl_plug = manager.get_device_by_name("TPL 01")

    # ---------------------------
    # Let's play with smart plugs
    # ---------------------------

    if tpl_plug.online:

        print("Let's play with smart plug %s" % tpl_plug.name)

        channels = len(tpl_plug.get_channels())
        print("The plug %s supports %d channels." % (tpl_plug.name, channels))
        for i in range(0, channels):
            print("Turning on channel %d of %s" % (i, tpl_plug.name))
            tpl_plug.turn_on_channel(i)

            time.sleep(1)

            print("Turning off channel %d of %s" % (i, tpl_plug.name))
            tpl_plug.turn_off_channel(i)

        usb_channel = tpl_plug.get_usb_channel_index()
        if usb_channel is not None:
            print("Awesome! This device also supports USB power.")
            tpl_plug.enable_usb()
            time.sleep(1)
            tpl_plug.disable_usb()

        if tpl_plug.supports_electricity_reading():
            print("Awesome! This device also supports power consumption reading.")
            print("Current consumption is: %s" % str(tpl_plug.get_electricity()))
    else: 
        print("The plug %s seems to be offline. Cannot play with that..." % tpl_plug)


    # At this point, we are all done playing with the library, so we gracefully disconnect and clean resources.
    print("We are done playing. Cleaning resources...")
    manager.stop()

    print("Bye bye!")