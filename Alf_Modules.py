#       Module Check
#
#       Autor:              Stefan Dimnik
#       Date:               02.11.2020
#       Python:             3.7
#       Projekt Details:    https://github.com/SDim44/Alfred
#       ------------------------------------------------------------
#       
#       V0.1
#       Saves and Manage connected Modules
#       ------------------------------------------------------------


import pickle
import time
import c_device as cla
import paho.mqtt.client as mqtt


# Variable
supported_protocol = ["mqtt","serial","I2C"]
supported_connection_type = ["lan","wlan","usb","bus"]
supported_sensor_data = ["temperature","pressure","sealevelpressure","humidity"]
supported_actuator_actions = ["btn","scale"]


# ------------------------------------------------------------------------------------------------------
# define class

class device(object):
    def __init__(self, name, protocol, connection_type, mac_address, server_address, client_address, sensorlist, actuatorlist, description, status):
        self.name = name
        self.protocol = protocol
        self.connection_type = connection_type
        self.mac_address = mac_address
        self.server_address = server_address
        self.client_address = client_address
        self.sensorlist = sensorlist
        self.actuatorlist = actuatorlist
        self.description = description
        self.status = status

        print("\n\n\t\tDevice created!: {0} {1}".format(self.name, self.description))

        # --------------------------------------------------------------------------------------------------------
    # methodes

    def show(self):
        ret = print("\n\t" + f"{'{0}' :^15}".format(self.name) + "|" + f"{'{0}' :^10}".format(self.status) + "|"  f"{'{0}' :^15}".format(self.mac_address) + "|" +  f"{'{0}' :^15}" .format(self.description))
        return ret

    def abilities(self):
        slist = []
        alist = []
        for s in self.sensorlist:
            slist.append(s.name)
        
        for a in self.actuatorlist:
            alist.append(a.name)
        
        ret = print("\n\n\t{0} \n\tSensors: {1} \n\tActuators: {2} ".format(self.name,slist,alist))
        return ret

    def get(selfe,cmd="all"):
        device_topic = "homestead/" + self.mac_address
        command = "get " + cmd
        client.publish(device_topic,command)

    def do(selfe,cmd):
        device_topic = "homestead/" + self.mac_address
        command = "do " + cmd
        client.publish(device_topic,command)
    
    
# --------------------------------------------------------------------------------------------------------
class sensor(object):
    def __init__(self,name,unit,description):
        self.name = name
        self.unit = unit
        self.description = description

    def show(self):
        ret = print("\n\t" + f"{'{0}':^15}" + "|" + f"{'{1}' :^15}" + "|"  f"{'{2}' :^15}" .format(self.name, self.unit, self.description))
        return ret

    def get(selfe,cmd="all"):
        if device.protocol == "mqtt":
            device_topic = "homestead/" + self.mac_address
            cmd = "get " + self.name
            client.publish(device_topic,cmd)

        elif device.protocol == "serial":
            print("Not Supported")

        elif device.protocol == "http":
            print("Not Supported")

        

        else:
            print("Not Supported")

# --------------------------------------------------------------------------------------------------------
class actuator(object):
    def __init__(self,name,function,values,description):
        self.name = name
        self.function = function
        self.values = values
        self.description = description

    def show(self):
        ret = print("\n\t" + f"{'{0}':^15}" + "|" + f"{'{1}' :^15}" + "|"  f"{'{2}' :^15}" .format(self.name, self.command, self.description))
        return ret  
    
    def do(selfe,cmd):
        device_topic = "homestead/" + self.mac_address
        command = "do " + cmd
        client.publish(device_topic,command)