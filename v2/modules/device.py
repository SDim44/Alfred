#       Class Devicelist
#
#       Autor:              Stefan Dimnik
#       Date:               04.11.2020
#       Python:             3.7
#       Projekt Details:    https://github.com/SDim44/Alfred
#       ------------------------------------------------------------
#       
#       V0.1
#       Saves and Manage connected devices
#       ------------------------------------------------------------


# ------------------------------------------------------------------------------------------------------
# Libraries

import time
import pickle
import os

# Config file importieren ...
config = {}


# Variable
supported_protocol = ["mqtt","serial","i2c"]
supported_baudrate = ["9600","19200","115200"]

width_menue = 70


broker = "testipi"
port = 1883
topic = "homestead/"


# ------------------------------------------------------------------------------------------------------
# define class

class device(object):
    devicelist = []

    def __init__(self, name, description, mqtt:bool, mac_address, broker, i2c:bool, slave_address:str, serial:bool, serial_port, baudrate, driver):
        self.name = name
        self.description = description
        
        # if mqtt
        self.mqtt = mqtt                                #True = wired
        self.mac_address = mac_address
        self.broker = broker

        # if i2c
        self.i2c = i2c                                  #True = wired
        self.slave_address = str(slave_address)
        
        # if serial
        self.serial = serial                            #True = wired
        self.serial_port = serial_port
        self.baudrate = baudrate

        # driver
        self.driver = driver                            # [[driver1,protocol],[driver2,protocol]]

        # auto generate
        self.commandlist = self.update_commandlist()
        self.status = self.update_status()              #True = online
        

        print("\n\n\t\tDevice created!: {0} {1}".format(self.name, self.description))

    # --------------------------------------------------------------------------------------------------------
    # Methodes

    def show(self):
        #self.update()
        
        if self.status:
            status = "ONLINE"
        else:
            status = "OFFLINE"

        print("\n\t{0:{3}}  |  {1:{4}}  |  {2:{5}}".format(self.name,status,self.description,20,15,40))


    def show_commands(self):

        if self.status:
            status = "ONLINE"
        else:
            status = "OFFLINE"

        print("\n\tCommands for {0} -> Currently {1}".format(self.name,status))

        print("\n\t{0:{2}}  |    {1:{3}}".format("Alias","Execution",20,40))
        print("\t","_"*70)

        up = 0
        lo = 0
        splitted = ""
        sc_key = ""
        sc_value = ""

        for keys,values in self.commandlist.items():
            
            if "scale." in keys:
                sc_key = str(keys)
                sc_value = values
                splitted = keys.split(".")
                value = int(splitted[-1])

                if value < lo:
                    lo = value

                elif value > up:
                    up = value            
            
            else:
                print("\n\t{0:{2}}  |    {1:{3}}".format(keys,values,20,40))

        if sc_key:
            area = str(lo) + "-" + str(up)
            splitted = sc_key.split(".")
            current_int = splitted[-1]
            keys = keys.replace(current_int,"")
            keys = str(keys + area)
            
            print("\n\t{0:{2}}  |    {1:{3}}".format(keys,sc_value,20,40))
        
        print("\n")

    def update_protocol(self):

        if self.mac_address and self.broker:
            self.mqtt == True
        else:
            self.mqtt == False
        if self.slave_address:
            self.i2c == True
        else:
            self.i2c == False
        if self.serial_port and self.baudrate:
            self.serial == True
        else:
            self.serial == False

    def update_status(self):
        status = False
        if self.i2c:
            try:
                import modules.interfaces.i2c as i2c
                i2c.send(self.slave_address,0)
                status = True
                
            except:
                pass

        if self.mqtt:
            requests = mqtt_authenticator(5,self.broker)
            for entry in requests:
                if entry["mac_address"] == self.mac_address:
                    status == True
                        
        print(status)
        return status

    def update_commandlist(self):
        driverlist = self.driver
        commandlist = {}
        for driver in driverlist:
            import importlib
            MODULE_NAME = "modules.driver."+driver[0]
            d = importlib.import_module(MODULE_NAME)
            
            if self.i2c == True and driver[1] == "i2c":
                for sup in d.supported_commands:
                    if "scale." in sup:
                        area = sup.replace("scale.","")
                        area = area.split("-")
                        lo = int(area[0])
                        up = int(area[1])+1
                        for i in range(lo, up):
                            command = str("driver."+driver[0]+"."+'i2c("'+self.slave_address+'","'+str(i)+'")')
                            key = str(self.name+".scale."+str(i))
                            commandlist[key] = command
                    else:    
                        command = str("driver."+driver[0]+"."+'i2c("'+self.slave_address+'","'+sup+'")')
                        key = str(self.name+"."+sup)
                        commandlist[key] = command
            
            
            elif self.serial == True and driver[1] == "serial":
                for sup in d.supported_commands:
                    command = str("driver."+driver[0]+"."+'serial("'+self.slave_address+'","'+sup+'")')
                    key = str(self.name+"."+sup)
                    commandlist[key] = command

            elif self.mqtt == True and driver[1] == "mqtt":
                pass

                        
        return commandlist

    #def listen_mqtt(self):
    #    import paho.mqtt.client as mqtt
    #    broker = "testipi"
    #    port = 1883

    #    if self.mqtt:
    #        path = "homestead/sensor/" + self.mac_address


    @staticmethod
    def update_staticdevicelist():
        device.devicelist = manager.load_devicelist()
        for dev in device.devicelist:
            print(dev.name)
        
        


# ------------------------------------------------------------------------------------------------------
# Functions


def load_device(filename):
    import pickle
    from pathlib import Path

    if ".pkl" not in filename:
        filename = filename + ".pkl"

    destination = "modules/programdata/" + str(filename)
    path = Path(destination)
    
    try:
        datenobjekt = open(path, "rb")
        objekt = pickle.load(datenobjekt)
        datenobjekt.close()

    except:
        print("\n\n\n\n\n\n\t!!!ATTENTION - Location not found! {0}".format(path))

    return objekt


def save_device(device):
    import pickle
    from pathlib import Path

    destination = "modules/programdata/" + device.name + ".pkl"
    path = Path(destination)

    try:
        datenobjekt = open(path, "wb")
        pickle.dump(device, datenobjekt)
        datenobjekt.close()

    except:
        print("\n\n\n\n\n\n\t!!!ATTENTION - Location not found! {0}".format(path))


def update_devicelist(devicelist):
    for dev in devicelist:      
        new_device = device(dev.name, dev.description, dev.mqtt, dev.mac_address, dev.broker, dev.i2c, dev.slave_address, dev.serial, dev.serial_port, dev.baudrate, dev.driver)
        save_device(new_device)

# ------------------------------------------------------------------------------------------------------
# get commands from command Library  

def get_commandlist(devicelist):
    commandlist = {}
    print("\n\t" + f"{'{0}' :25}".format("Alias") + "|    " + f"{'{0}' :<50}".format("Execution"))
    for dev in devicelist:
        if dev.status == "ONLINE":
            for keys,values in dev.commandlist.items():
                print("\n\t" + f"{'{0}' :25}".format(keys) + "|    " + f"{'{0}' :<50}".format(values))
                commandlist[keys] = values
    return commandlist


# ------------------------------------------------------------------------------------------------------
# send command from command Library  

def exe(command_value):
    import importlib
    command=""

    try:
        lib=command_value.split(".")
        MODULE_NAME = lib[0]+"."+lib[1]
        imp = "modules." + MODULE_NAME
        d = importlib.import_module(imp)
        command = command_value.replace(MODULE_NAME,"d")
    except:
        print("Module Import Failed!!!")

    exec(command)


# ------------------------------------------------------------------------------------------------------
# Add new devices    
def add():            
            
    while True:
        
        name = input("\n\t\t" + f"{'Name  ' :<25}" + ": ")
        description = input("\n\t\t" + f"{'Description  ' :<25}" + ": ")

        # ------------------------------------------------------------------
        # mqtt
        while True:
            inp_mqtt = input("\n\t\t" + f"{'Is MQTT wired?  ' :<25}" + "(j/n) : ")
            
            if inp_mqtt == "j":
                mqtt = True
                mac_address = input("\n\t\t" + f"{'MAC-Address  ' :<25}" + ": ")
                broker = input("\n\t\t" + f"{'Broker IP or Hostname ' :<25}" + ": ")
            elif inp_mqtt == "n":
                mqtt = False
                mac_address = ""
                broker = ""
            else:
                print("\n\n\n\n\n\n\t!!!ATTENTION - Write j or n)")
                continue
            break

        # ------------------------------------------------------------------
        # i2c
        while True:
            inp_i2c = input("\n\t\t" + f"{'Is I²C wired?  ' :<25}" + "(j/n) : ")
            
            if inp_i2c == "j":
                i2c = True
                slave_address = input("\n\t\t" + f"{'Slave-Address  ' :<25}" + ": ")
            elif inp_i2c == "n":
                i2c = False
                slave_address = ""
            else:
                print("\n\n\n\n\n\n\t!!!ATTENTION - Write j or n)")
                continue
            break

        # ------------------------------------------------------------------
        # serial
        while True:
            inp_serial = input("\n\t\t" + f"{'Is Serial wired?  ' :<25}" + "(j/n) : ")
            
            if inp_serial == "j":
                serial = True
                serial_port = input("\n\t\t" + f"{'Serial Port  ' :<25}" + ": ")
                baudrate = input("\n\t\t" + f"{'Baud-Rate ' :<25}" + ": ")
            elif inp_serial == "n":
                serial = False
                serial_port = ""
                baudrate = ""
            else:
                print("\n\n\n\n\n\n\t!!!ATTENTION - Write j or n)")
                continue
            break


        # ------------------------------------------------------------------
        # driver
        from os import listdir
        from pathlib import Path
        path = Path("modules/driver/")
        filelist = listdir(path)
        driverlist = []
        driver = []
        while True:
            for dr in filelist:
                dr_name = dr.strip(".py")
                if dr == "__pycache__":
                    pass
                else:
                    driverlist.append(dr_name)
            print(driverlist)
            inp_driver = input("\n\t\t" + f"{'Choose a Driver from List  ' :<25}" + ": ")
            
            if inp_driver in driverlist:
                while True:
                    import importlib
                    MODULE_NAME = "modules.driver."+inp_driver
                    d = importlib.import_module(MODULE_NAME)
                    print("\n\tSupported Protocols from Driver: {0}".format(d.supported_protocol))
                    inp_protocol = input("\n\t\t" + f"{'Choose a Protocol from Driver {0}  ' :<25}".format(inp_driver) + ": ")
                    i=0
                    for prot in d.supported_protocol:
                        if prot == inp_protocol:
                            i+=1
                    if i == 0:
                        continue
                    break
            else:
                continue
            driver.append([inp_driver,inp_protocol])
            wh = input("\n\n\n\t\tAdd another driver? (j/n))")
            if wh == "n":
                break

        new_device = device(name, description, mqtt, mac_address, broker, i2c, slave_address, serial, serial_port, baudrate, driver)
        
        save_device(new_device)
        
        return new_device

# ------------------------------------------------------------------------------------------------------
# Load Devices to devicelist

def load_devicelist():
    from os import listdir
    from pathlib import Path
    
    devicelist = []
    
    path = Path("modules/programdata/")
    filelist = listdir(path)

    for dev_file in filelist:
        dev_object = load_device(dev_file)
        devicelist.append(dev_object)
        
    return devicelist

# ------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------
# MQTT Auhtenticator

def mqtt_authenticator(try_time=5,broker="localhost",port=1883,topic="homestead/Authentication/#"):
    
    import paho.mqtt.client as mqtt
    from uuid import getnode as get_mac

    global mqtt_requests

    # --------------
    # MQTT Connect

    def on_connect(client, userdata, flags, rc):

        try:
            client.subscribe(topic)
        except:
            print("\n\n\tBroker is down!!!")

    # ----------------
    # MQTT Disconnect

    def on_disconnect(client, userdata, flags, rc):
        
        print("\tTrying to reconnect ...")
        client.subscribe(g_topic)


    # ----------------------
    # MQTT message recieved

    def on_message(client, userdata, message):
        global mqtt_requests

        msg = str(message.payload.decode("utf-8"))

        splitted = msg.split(";")
        data = {}

        #print("\n\n\tDevice found: ")

        for dataset in splitted:
            info = dataset.split(",")
            #print("\n\t\t{0} :  {1}".format(info[0],info[1]))
                
            data[info[0]] = info[1]

        mqtt_requests.append(data)
        
    # --------------------
    # MQTT message sent

    def on_publish(client,userdata,result):
        #print("data published\n")
        pass

    # --------------------
    # Main loop

    mqtt_requests = []

    try:
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_publish = on_publish
        client.on_disconnect = on_disconnect


        client.connect(broker,port)
        client.loop_start()

        time.sleep(try_time)

        client.loop_stop()

        return mqtt_requests
    
    except KeyboardInterrupt:
        client.loop_stop()



# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------
# Device Manager
# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def manager():   

    from datetime import datetime

    devicelist = []

    # Variable
    width_menue = 70  # Window width

    yes = 'j', 'J', 'y', 'Y', 'ja', 'Ja', 'yes', 'Yes'
    forbidden = "!$%&/()=?-+*"
    numbers = "0123456789"


    # ------------------------------------------------------------------------------------------------------
    # title
    def title(txt):
        print("\n\n\n\n\n\n")
        print("\t*{0:^{1}}*".format("*" * width_menue, width_menue))
        print("\t*{0:^{1}}*".format(" ", width_menue))
        print("\t*{0:^{1}}*".format(txt, width_menue))
        print("\t*{0:^{1}}*".format(" ", width_menue))
        print("\t*{0:^{1}}*".format("*" * width_menue, width_menue))
        print("\n")

    # ------------------------------------------------------------------------------------------------------
    # Menue

    def menue(loaded_list):
        while True:
            try:
                title("Device Manager")

                print("\tDevicelist -> {0}".format(loaded_list))

                print("\n")
                print("\t\t" + f"{'Create new device  ':.<50}" + "  1")
                print("\t\t" + f"{'Show device status  ':.<50}" + "  2")
                print("\t\t" + f"{'Show available commands  ':.<50}" + "  3")
                print("\t\t" + f"{'Update Devicelist':.<50}" + "  4")
                print("\t{0:^{1}}".format(" ", width_menue))
                print("\t\t" + f"{'Execute command':.<50}" + "  5")
                print("\t\t" + f"{'Listen MQTT Sensors':.<50}" + "  6")
                print("\t\t" + f"{'Search for new MQTT Devices':.<50}" + "  7")
                print("\t{0:^{1}}".format(" ", width_menue))
                print("\t\t" + f"{'Quit  ':.<50}" + "  0")
                print("\t{0:^{1}}".format(" ", width_menue))

                # Eingabe
                eingabe = int(input("\n\t\t\t" + f"{'Choose an action': <42}" + ": "))
                if (eingabe < 0) or (eingabe > 7):
                    print("\n\n\n\n\n\n\n\t\t!!! Please use a number from the menu !!!\n\n")
                    continue
                return eingabe
                break

            except ValueError:
                print("\n\n\n\n\n\n\n\t!!! You entered an incorrect data type !!!")
                print("\t!!! Please use a number from the menu !!!")
                continue
            

    # ------------------------------------------------------------------------------------------------------
    # Manager Main

    # Welcometext
    print("\n\n\n\n\tWelcome to Device Manager!")

    try:
        devicelist = load_devicelist()
        loaded_list = str(datetime.now().strftime("%H:%M:%S"))
    except:
            loaded_list = "Loading Failed!!"

    try:
        while True:
            
            selection = menue(loaded_list)

            # ------------------------------------------------------------------------------------------------------
            # Crate device
            if selection == 1:

                title("Creat device")
                add()
                
                try:
                    devicelist = load_devicelist()
                    loaded_list = str(datetime.now().strftime("%H:%M:%S"))
                except:
                    loaded_list = "Loading Failed!!"

            # ------------------------------------------------------------------------------------------------------
            # show devices

            elif selection == 2:
                
                if devicelist:
                    title("Device overview")

                    print("\n\t{0:{3}}  |  {1:{4}}  |  {2:{5}}".format("Name","Status","Description",20,15,40))
                    print("\t","_"*85)
                    for deve in devicelist:
                        deve.show()
                
                    jn = input("\n\n\tMore Information? (j/n) : ")
                    if jn in yes:
                        for dev in devicelist:
                            print("\t{0:{2}}:  {1:{3}}".format("Name",dev.name,20,25))
                            print("\t{0:{2}}:  {1:{3}}".format("Description",dev.description,20,50))
                            print("\t{0:{2}}:  {1:{3}}".format("MQTT - wired?",dev.mqtt,20,1))
                            print("\t{0:{2}}:  {1:{3}}".format("Mac_Address",dev.mac_address,20,25))
                            print("\t{0:{2}}:  {1:{3}}".format("Broker",dev.broker,20,25))
                            print("\t{0:{2}}:  {1:{3}}".format("I²C - wired?",dev.i2c,20,1))
                            print("\t{0:{2}}:  {1:{3}}".format("Slave_Address",dev.slave_address,20,25))
                            print("\t{0:{2}}:  {1:{3}}".format("Serial - wired?",dev.serial,20,1))
                            print("\t{0:{2}}:  {1:{3}}".format("Serial_Port",dev.serial_port,20,50))
                            print("\t{0:{2}}:  {1:{3}}".format("Baudrate",dev.baudrate,20,25))
                            print("\t{0:{1}}:\n".format("Driver",20))
                            for dr in dev.driver:
                                print("\t\t{0:{2}}->  {1:{3}}".format(dr[0],dr[1],15,10))

                            print("\n\n\t-------------------------------------------------------------\n\n")

                        input("\n\n\t\t\t--Press any key to continue--")
                    
                else:
                    print("\n\n\n\n\n\n\t!!!ATTENTION - No device list loaded!")


            # ------------------------------------------------------------------------------------------------------
            # show commands

            elif selection == 3:
                
                if devicelist:
                    title("Available Commands")
                    
                    for dev in devicelist:
                        temp = dev.show_commands()

                else:
                    print("\n\n\n\n\n\n\t!!!ATTENTION - No device list loaded!")

                input("\n\n\t\t\t--Press any key to continue--")

            # ------------------------------------------------------------------------------------------------------
            # Update Devicelist

            elif selection == 4:
                
                update_devicelist(devicelist)
                devicelist = load_devicelist()
                loaded_list = str(datetime.now().strftime("%H:%M:%S"))

            # ------------------------------------------------------------------------------------------------------    
            # execute command

            elif selection == 5:
                
                if devicelist:
                    title("Available Commands")
                    
                    commandlist = {}

                    for dev in devicelist:
                        if dev.status:
                            commandlist.update(dev.commandlist)

                    for dev in devicelist:
                        temp = dev.show_commands()

                    while True:
                        inp_cmd = input("\n\n\tChoos Alias: ")

                        if inp_cmd:
                            if inp_cmd in commandlist.keys():
                                exec_cmd = commandlist[inp_cmd]
                                exe(exec_cmd)

                                #if feedback == "1":
                                #    print("True")
                                #elif feedback == "0":
                                #    print("False")
                                #else:
                                #    print("Unknown")
                            else:
                                continue
                        else:
                            break
                
                else:
                    print("\n\n\n\n\n\n\t!!!ATTENTION - No device list loaded!")

            
            # ------------------------------------------------------------------------------------------------------
            # Listen MQTT

            elif selection == 6:
                
                print("\n\n\tPress Crtl + c to exit")
                import modules.interfaces.mqtt_listener as mqtt_listener
                mqtt_listener.run("testipi")


            # ------------------------------------------------------------------------------------------------------
            # Listen for MQTT-Requests
                
            elif selection == 7:
                
                broker = "testipi"
                title("Searching for new Devices ...")
                requests = mqtt_authenticator(5,broker)
                found_devices = []
                
                for entry in requests:
                    count = 0
                    for dev in devicelist:
                        if entry["mac_address"] in dev.mac_address:
                            count +=1
                    if count == 0:
                        found_devices.append(entry)

                for dev in found_devices:
                    print("\n\n\tDevice: ")
                    for keys,values in dev.items():
                        print("\n\t\t{0:{2}}  |    {1:{3}}".format(keys,values,20,40))


                    jn = input("\n\n\n\t\tWould you reate a new Device from recieved data? (j/n) : ")

                    if jn in yes:
                        try:
                            if dev["name"]:
                                name = dev["name"]
                        except:
                            name = input("\n\t\t" + f"{'Name  ' :<25}" + ": ")
                        ###
                        try:
                            if dev["description"]:
                                description = dev["description"]
                        except:
                            description = input("\n\t\t" + f"{'Description  ' :<25}" + ": ")
                        ###
                        try:
                            if dev["baudrate"]:
                                baudrate = dev["baudrate"]
                        except: 
                            baudrate = ""
                        ###
                        try:
                            driver = []
                            if dev["driver"]:
                                dr = dev["driver"]
                                driver.append(dr.split("@"))  
                        except: 
                            driver = input("\n\t\t" + f"{'Description  ' :<25}" + ": ")
                        ###
                        try:
                            if dev["slave_address"]:
                                slave_address = dev["slave_address"]
                        except:
                            slave_address = input("\n\t\t" + f"{'Slave_Address  ' :<25}" + ": ")
                        ###
                        try:
                            if dev["serial_port"]:
                                serial_port = dev["serial_port"]
                        except:
                            serial_port = input("\n\t\t" + f"{'Serial_Port  ' :<25}" + ": ")

                        mqtt = True
                        mac_address = dev["mac_address"]
                        i2c = False
                        serial = False
                        print("\n")
                        print(dev["driver"])
                        print("\n")
                        print(driver)

                        input("\n\tEnter....")
                        
                        new_device = device(name, description, mqtt, mac_address, broker, i2c, slave_address, serial, serial_port, baudrate, driver)
                        save_device(new_device)
                    

            # ------------------------------------------------------------------------------------------------------
            # Programm Beenden

            elif selection == 0:
                print('\n\n\n\n\n\tSee ya!!!\n\n\n')
                break
            
    except KeyboardInterrupt:
        selection = 0




















###########################################################################################
#    def get(selfe,cmd="all"):
#        device_topic = "homestead/" + self.mac_address
#        command = "get " + cmd
#        client.publish(device_topic,command)
#
#    def do(selfe,cmd):
#        device_topic = "homestead/" + self.mac_address
#        command = "do " + cmd
#        client.publish(device_topic,command)
#    def get(selfe,cmd="all"):
#        if device.protocol == "mqtt":
#            device_topic = "homestead/" + self.mac_address
#            cmd = "get " + self.name
#            client.publish(device_topic,cmd)
#
#        elif device.protocol == "serial":
#            print("Not Supported")
#
#        elif device.protocol == "http":
#            print("Not Supported")
#
#        else:
#            print("Not Supported")
#
#   
#   def do(self,protocol,dev_id,cmd):
#        if protocol == "mqtt":
#            device_topic = "homestead/" + dev_id
#            command = "do " + cmd
#            client.publish(device_topic,command)
#
#        elif protocol == "i2c":
#            import Alf_I2CTool as i2c
#            print("{0} <- in modules call i2c.send".format(cmd))
#            i2c.send(dev_id,cmd)