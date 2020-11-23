#       Homestead MQTT Client
#
#       Autor:              Stefan Dimnik
#       Date:               28.09.2020
#       Python:             3.7
#       Projekt Details:    https://github.com/SDim44/Homestead
#       ------------------------------------------------------------
#       
#       V0.1
#       Connect to Homestead and authenticate over mqtt
#       ------------------------------------------------------------
#       V0.2 - 03.10.2020
#       Autoconnect and Identify 
#       Send Sensor Data if the Command is recieved
#       ------------------------------------------------------------


# ------------------------------------------------------------------------------------------------------
# Libraries

import paho.mqtt.client as mqtt
from uuid import getnode as get_mac
import time
import os

# ------------------------------------------------------------------------------------------------------
# Variables

global signed_in
global sensor
global actuator
global authen
global authen_topic
global sensor_topic

########################################################################################################
#                                       Client abilities
#                      Modify this Settings to idetify your device on Homestead 

name = "Alfred"
connection_type = "wlan"
sensor = ["temperature","pressure","sealevelpressure","humidity"]
actuator = [["btn","Auf"],["btn","Zu"],["scale","Grad",["0","40"]]]
description = "Robot control"

#Optional Settings
broker = "testipi"
port = 1883

#
#
########################################################################################################

my_hostname = os.uname()[1]
my_mac = hex(get_mac())

topic = "homestead/" + hex(get_mac())
authen_topic = "homestead/Authentication"
sensor_topic = "homestead/sensor/" + hex(get_mac())

authen = ("NEW_DEVICE;" + str(name) + ";" + "mqtt;" + str(connection_type) + ";" + str(my_mac) + ";" + str(broker) + ";" + str(my_hostname) + ";" + str(sensor) + ";" + str(actuator) + ";" + str(description))

signed_in = "FALSE"

# ------------------------------------------------------------------------------------------------------
# read Sensor data

def get_sensor(chosen=all):
    global sensor
    if chosen == sensor[0]:
        value =  "24.6°C"
    elif chosen == sensor[1]:
        value = "230 bar"
    elif chosen == sensor[2]:
        value = "400 hpa"
    elif chosen == sensor[3]:
        value = "30%"
    elif chosen == "all":
        value = ["24.6°C","230 bar","400 hpa","30%"]
    return value

# ------------------------------------------------------------------------------------------------------
# set actuator

def set_actuator(chosen,value=0):
    if chosen == "Zuf":
        do = "AUF"
    elif chosen == "Zu":
        do = "ZU"
    elif chosen == "Grad":
        do = value
    else:
        do = "FALSE"
    return do

# ------------------------------------------------------------------------------------------------------
# MQTT Connect

def on_connect(client, userdata, flags, rc):
    global authen
    global topic
    print("Trying to connect homestead ...")
    client.subscribe(topic)
    temp=authen.split(";")
    greetings = str("Hallo Homestead! I am " + temp[1] + " - " + temp[4])
    client.publish(topic,greetings)
    print("\nConnected!\n")

# ------------------------------------------------------------------------------------------------------
# MQTT Disconnect

def on_disconnect(client, userdata, flags, rc):
    global signed_in
    global authen
    signed_in = "FALSE"
    print("Trying to reconnect homestead ...")
    client.subscribe(topic)
    temp=authen.split(";")
    greetings = str("Hallo Homestead! I am " + temp[1] + " - " + temp[4])
    client.publish(topic,greetings)


# ------------------------------------------------------------------------------------------------------
# MQTT on subscribe

#def on_subscribe(client, userdata, message):
#    client.publish(autopub_topic,topic + "  -->  " + str(get_value(all)))
#    time.sleep(10)


# ------------------------------------------------------------------------------------------------------
# MQTT message recieved

def on_message(client, userdata, message):
    global signed_in
    global authen
    global topic
    global authen_topic
    global sensor_topic
    sensor_values = []
    chosen=[]
    msg = str(message.payload.decode("utf-8"))

    # ------------------------------------------------------------------------------------------------------
    # Sign-in
    if signed_in == "FALSE":
        client.publish(authen_topic,authen)
        time.sleep(5)
        if msg == "TRUE":
            signed_in = "TRUE"
            print("Authentication Succsessful!!!")
        else:
            print("Authentication ...")
            client.publish(authen_topic,authen)
            time.sleep(5)
            if msg != "TRUE":
                temp=authen.split(";")
                greetings = str("Hallo Homestead! I am " + temp[1] + " - " + temp[4])
                client.publish(topic,greetings)
    else:
        # ------------------------------------------------------------------------------------------------------
        # get Sensor data
        if msg.startswith('get'):
                     
            for data in sensor:
                if data in msg:
                    chosen.append(data)
                    value = get_sensor(data)
                    print(value)
                    sensor_values.append(value)
            try:
                if sensor_values[0]:
                    pass
                else:
                    sensor_values = get_sensor("all")
            except:
                sensor_values = get_sensor("all")
                

            client.publish(sensor_topic,str(sensor_values))

        # ------------------------------------------------------------------------------------------------------
#!!!!!!!!!!!!!!Funktioniert NICHT!!!!!!!!!!!!!!        
        # set actuator 
        elif msg.startswith('do'):
            for action in actuator:
                if action in msg:
                    if action[0] == "btn":
                        ret = set_actuator(action[1],"0")
                    elif action[0] == "scale":
                        ret = set_actuator(action[1],action[2])
            print(ret)
            client.publish(topic,str(ret))


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
    #client.on_subscribe = on_subscribe


    client.connect(broker)

    print("Connected to MQTT Broker: " + broker + "->" + topic)

    client.loop_forever()

except:
    print("FAILD!!")
