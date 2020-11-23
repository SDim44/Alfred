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
#   
#     ------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------
# Libraries

import paho.mqtt.client as mqtt
from uuid import getnode as get_mac
import time
import os


def run(broker="localhost",port=1883,topic="homestead/sensor/#"):

    # ------------------------------------------------------------------------------------------------------
    # MQTT Connect

    def on_connect(client, userdata, flags, rc):
        global g_topic

        try:
            client.subscribe(topic)
            print("\tConnected")
        except:
            print("\n\n\tBroker is down!!!")

    # ------------------------------------------------------------------------------------------------------
    # MQTT Disconnect

    def on_disconnect(client, userdata, flags, rc):
        
        print("\tTrying to reconnect ...")
        client.subscribe(g_topic)


    # ------------------------------------------------------------------------------------------------------
    # MQTT message recieved

    def on_message(client, userdata, message):
        msg = str(message.payload.decode("utf-8"))

        print("\n")
        print("\tMessage: {0}".format(msg))

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

        client.connect(broker,port)
        client.loop_forever()

    except KeyboardInterrupt:
        client.loop_stop()