#       Homestead MQTT Listener
#
#       Autor:              Stefan Dimnik
#       Date:               28.09.2020
#       Python:             3.7
#       Projekt Details:    https://github.com/SDim44/Homestead
#       ------------------------------------------------------------
#       
#       V0.1
#       Recieved MQTT messages and Authenticate devices
#       Save new devices in .pkl file
#       ------------------------------------------------------------


# ------------------------------------------------------------------------------------------------------
# Libraries

import paho.mqtt.client as mqtt
from uuid import getnode as get_mac
import time
import os
import pickle


# ------------------------------------------------------------------------------------------------------
# Variables
broker = "localhost"
port = 1883
my_mac = hex(get_mac())
my_hostname = os.uname()[1]

root_topic = "homestead/"
topic = "homestead/Authentication"
default_location = "/home/pi/Homestead/devicelist.pkl"
devicelist = []

# ------------------------------------------------------------------------------------------------------
# MQTT Connect

def on_connect(client, userdata, flags, rc):
    try:
        os.system("sudo systemctl enable mosquitto")
        client.subscribe(topic)
        print("connected")
    except:
        print("Broker is down!!!")

# ------------------------------------------------------------------------------------------------------
# MQTT Disconnect

def on_disconnect(client, userdata, flags, rc):
    try:
        os.system("sudo systemctl enable mosquitto")
    except:
        print("Broker is down!!!")
    print("Trying to reconnect ...")
    client.subscribe(root_topic + "#")


# ------------------------------------------------------------------------------------------------------
# MQTT message recieved

def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    print(msg)

    if msg.startswith("NEW_DEVICE"):
        print("\nDevice is trying to connect")
        arr = msg.split(";")
        mac = arr[4]
        print("{0} - Mac_Address: {1}\n".format(arr[1],mac))

        devicelist = []
        devicelist = load_devicelist(default_location)

        known_macs=[]
        for device in devicelist:
            known_macs.append(device.mac_address)

        if mac in known_macs:
            #print("\n{0} - is online\n".format(device.name))
            client.publish(root_topic + mac,"TRUE")

        else:
            print("\nAdd {0} to devicelist".format(arr[1]))
            #print("Parameter: {1} {2} {3} {4} {5} {6} {7} {8}\n\n".format(arr[2],arr[3],arr[4],arr[5],arr[6],arr[7],arr[8],arr[9]))

            add_device(default_location,arr[1],arr[2],arr[3],arr[4],arr[5],arr[6],arr[7],arr[8],arr[9])
    else:
        pass

# ------------------------------------------------------------------------------------------------------
# MQTT message sent

def on_publish(client,userdata,result):
    #print("data published\n")
    pass


# ------------------------------------------------------------------------------------------------------
# Main loop


try:
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect

    client.connect(broker)
    print("MQTT Broker is online")

    try:
        devicelist = load_devicelist(default_location)
        print("Devicelist loaded!")
    except:
        print("Devicelist not loaded!")

    client.loop_forever()
    
except:
    print("FAILD!!")