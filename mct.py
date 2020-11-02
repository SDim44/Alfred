#       Module Creation Tool
#
#       Autor:              Stefan Dimnik
#       Date:               02.11.2020
#       Python:             3.7
#       Projekt Details:    https://github.com/SDim44/Alfred
#       ------------------------------------------------------------
#       
#       V0.1
#       Menue to add Modules to Alfred
#       ------------------------------------------------------------
#       V0.2 -> working on it
#       Get Sensor Data or set Actuator directly from mct
#       ------------------------------------------------------------


# import libraries
import pickle
import time
import Alf_Modules as cla
import paho.mqtt.client as mqtt


# Variable
width_menue = 70  # Window width

yes = 'j', 'J', 'y', 'Y', 'ja', 'Ja', 'yes', 'Yes'
forbidden = "!$%&/()=?-+*"
numbers = "0123456789"

default_save = "devicelist.pkl"  # Default-path

devicelist = []


broker = "testipi"
topic = "homestead/#"
client = mqtt.Client()

# ------------------------------------------------------------------------------------------------------
# Menue

def menue(loaded_list):

    while True:
        try:
            title("Device Manager")

            if devicelist:
                print("\tLoaded device list: {0}".format(loaded_list))

            else:
                print("\t(No device list loaded!)")

            print("\n")
            print("\t\t" + f"{'Create device list  ':.<50}" + "  1")
            print("\t\t" + f"{'Modify device list  ':.<50}" + "  2")
            print("\t\t" + f"{'Show devices  ':.<50}" + "  3")
            print("\t\t" + f"{'Show device abilities  ':.<50}" + "  4")
            print("\t{0:^{1}}".format(" ", width_menue))
            print("\t\t" + f"{'Get Sensor Data  (...in developement)':.<50}" + "  5")
            print("\t\t" + f"{'Set an Actuator  (...in developement)':.<50}" + "  6")
            print("\t{0:^{1}}".format(" ", width_menue))
            print("\t\t" + f"{'Load pkl  ':.<50}" + "  8")
            print("\t\t" + f"{'Save pkl  ':.<50}" + "  9")
            print("\t{0:^{1}}".format(" ", width_menue))
            print("\t\t" + f"{'Quit  ':.<50}" + "  0")
            print("\t{0:^{1}}".format(" ", width_menue))

            # Eingabe
            eingabe = int(input("\n\t\t\t" + f"{'Choose an action': <42}" + ": "))
            if (eingabe < 0) or (eingabe > 9):
                print(
                    "\n\n\n\n\n\n\n\t\t!!! Please use a number from the menu !!!\n\n")
                continue
            return eingabe
            break

        except ValueError:
            print("\n\n\n\n\n\n\n\t!!! You entered an incorrect data type !!!")
            print("\t!!! Please use a number from the menu !!!")
            continue


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


# -------------------------------------------------------------------
# create sensor
    
def create_sensors():

    yes = 'j', 'J', 'y', 'Y', 'ja', 'Ja', 'yes', 'Yes'
    forbidden = "!$%&/()=?-+*"
    numbers = "0123456789"

    sensorlist =[]
    n=0
    while True:
        n+=1
        values = []
        print("\n\n\tCreat Sensor entrys")
        
        try:
            s_name = input("\n\t\t{0}. Sensor".format(n) + f"{'Name  ' :<25}" + ": ")
        except:
            print("\n\n\t!!!ATTENTION - Something went wrong!")

        try:
            s_unit = input("\n\t\t{0}. Sensor".format(n) + f"{'Unit  ' :<25}" + ": ")
        except:
            print("\n\n\t!!!ATTENTION - Something went wrong!")

        try:
            s_description = input("\n\t\t{0}. Sensor".format(n) + f"{'Description  ' :<25}" + ": ")
        except:
            print("\n\n\t!!!ATTENTION - Something went wrong!")


        svalue = cla.sensor(s_name,s_unit,s_description)
        sensorlist.append(svalue)

        rp = input("\n\twould you like to add another device? (y/n): ")
        i = 0
        for j in yes:
            if j == rp:
                i += 1
        if i == 0:
            print('\n\n\n\n\n')
            break
        
    return sensorlist

# ------------------------------------------------------------------
# create actuator
def create_actuators():

    yes = 'j', 'J', 'y', 'Y', 'ja', 'Ja', 'yes', 'Yes'
    forbidden = "!$%&/()=?-+*"
    numbers = "0123456789"
    
    actuatorlist =[]
    n=0
    while True:
        n+=1
        values = []
        print("\n\n\tCreat Actuator entrys")
        
        try:
            a_name = input("\n\t\t{0}. Actuator".format(n) + f"{'Name  ' :<25}" + ": ")
        except:
            print("\n\n\t!!!ATTENTION - Something went wrong!")

        try:
            a_function = input("\n\t\t{0}. Actuator".format(n) + f"{'Function  ' :<25}" + ": ")
        except:
            print("\n\n\t!!!ATTENTION - Something went wrong!")

        try:
            a_values = input("\n\t\t{0}. Actuator".format(n) + f"{'Function Values  ' :<25}" + ": ")
        except:
            print("\n\n\t!!!ATTENTION - Something went wrong!")

        try:
            a_description = input("\n\t\t{0}. Actuator".format(n) + f"{'Description  ' :<25}" + ": ")
        except:
            print("\n\n\t!!!ATTENTION - Something went wrong!")

        avalue = cla.actuator(a_name,a_function,a_values,a_description)
        actuatorlist.append(avalue)

        rp = input("\n\twould you like to add another device? (y/n): ")
        i = 0
        for j in yes:
            if j == rp:
                i += 1
        if i == 0:
            print('\n\n\n\n\n')
            break
    
    return actuatorlist

# ------------------------------------------------------------------------------------------------------
# create device

def create_device():

    yes = 'j', 'J', 'y', 'Y', 'ja', 'Ja', 'yes', 'Yes'
    forbidden = "!$%&/()=?-+*"
    numbers = "0123456789"


    # ------------------------------------------------------------------
    # Name
    print("\n\tEnter the following information: ")
    while True:
        name = input("\n\t\t" + f"{'Name  ' :<25}" + ": ")
        break

    # ------------------------------------------------------------------
    # protocol

    while True:
        print("\n\t\tSupported Protocols:  {0}".format(cla.supported_protocol))
        protocol = input("\n\t\t" + f"{'Protocol  ' :<25}" + ": ")
        if protocol not in cla.supported_protocol:
            print("\n\n\t!!!ATTENTION - Wrong entry! Choose from Supported!")
            continue
        break

    # ------------------------------------------------------------------
    # connection type
    if protocol == "i2c":
        connection_type = "bus"
    else:
        while True:
            connection_type = input("\n\t\t" + f"{'Connection type  ' :<25}" + ": ")
            i = 0
            for s in connection_type:
                if s in forbidden:
                    i += 1
                elif s in numbers:
                    i += 1
            if i > 0:
                print(
                    "\n\n\t!!!ATTENTION - Wrong entry! No special characters or numbers are allowed!")
                continue
            break

    # ------------------------------------------------------------------
    # mac address / Slave Adress / Device Identification
    while True:
        if protocol == "i2c":
            mac_address = input("\n\t\t" + f"{'Slave Address (0x03) ' :<25}" + ": ")
            
            if "0x" not in mac_address:
                continue

        else:
            mac_address = input("\n\t\t" + f"{'MAC Adress  ' :<25}" + ": ")
            # Check if mac-address is correct
        
        break

    # ------------------------------------------------------------------
    # server_address
    if protocol == "i2c":
        server_address = "-"
        client_address = "-"

    else:
        while True:
            server_address = input("\n\t\t" + f"{'Server address (hostname or ip-address)  ' :<25}" + ": ")
            i = 0
            for s in server_address:
                if s in forbidden:
                    i += 1
            if i > 0:
                print(
                    "\n\n\t!!!ATTENTION - Wrong entry! No special characters or numbers are allowed!")
                continue
            break

        # ------------------------------------------------------------------
        # client_address
        while True:
            client_address = input("\n\t\t" + f"{'Client address (hostname or ip-address)  ' :<25}" + ": ")
            i = 0
            for s in client_address:
                if s in forbidden:
                    i += 1
            if i > 0:
                print(
                    "\n\n\t!!!ATTENTION - Wrong entry! No special characters or numbers are allowed!")
                continue
            break

    # ------------------------------------------------------------------
    # description
    while True:
        description = input("\n\t\t" + f"{'Description  ' :<25}" + ": ")
        # ------------
        break

    sensorlist = create_sensors()
    actuatorlist = create_actuators()

    status = "offline"
    objekt = cla.device(name, protocol, connection_type,mac_address,server_address,client_address,sensorlist,actuatorlist,description,status)
    

    return objekt

# ------------------------------------------------------------------------------------------------------
# Load device list

def load_list():

    title("Load device list")

    while True:
        try:
            input_path = input("\n\n\tEnter the file path to your device list (default... {0}): ".format(default_save))

            if input_path:
                location = input_path
            else:
                location = default_save

            datenobjekt = open(location, "rb")
            objekt = pickle.load(datenobjekt)
            datenobjekt.close()

            devicelist = objekt

            print("\n\n\tDevece list loaded '{0}'".format(location))

            element = [devicelist, location]
            return element
            break

        except:
            print("\n\n\n\n\n\n\t!!!ATTENTION - The file was not found or is damaged! z.B.:(C:/devicelist.pkl)")

# ------------------------------------------------------------------------------------------------------
# save device list

def save_list(loaded_list):

    # check location
    if loaded_list == "new device list (not saved)":
        loaded_list = False

    # modify default-path
    if loaded_list:
        sug_pkl = loaded_list
        print("\n\n\tThe default location has been changed to the location of the loaded list!")
    else:
        sug_pkl = default_save

    title("Save device list")

    # get path and save
    while True:
        try:
            input_path = input("\n\n\tEnter the file path to your device list (default... {0}): ".format(sug_pkl))

            if input_path:
                location = input_path
            else:
                location = sug_pkl

            if ".pkl" in location:
                pass
            else:
                #location = location + ".pkl"
                print("\n\n\n\n\n\n\t!!!ATTENTION - Please enter the file extension .pkl! e.g.:(devicelist.pkl)")
                continue
            
            datenobjekt = open(location, "wb")
            pickle.dump(devicelist, datenobjekt)
            datenobjekt.close()
            
            print("\n\n\tDevicelist saved -> '{0}'".format(location))

            return location
            break

        except:
            print(
                "\n\n\n\n\n\n\t!!!ATTENTION - Location not found! z.B.:(C:/devicelist.pkl)")


def on_connect(client, userdata, flags, rc):
    try:
        client.subscribe(topic)
        print("connected")
    except:
        print("Broker is down!!!")

def on_message(client, userdata, message):
    clt = str(client.payload.decode("utf-8"))
    udata = str(userdata.payload.decode("utf-8"))
    msg = str(message.payload.decode("utf-8"))
    print("--> {0}, {1}, {2}".format(clt,udata,msg))

# ------------------------------------------------------------------------------------------------------
# Main

# Welcometext
print("\n\n\n\n\tWelcome to Device Manager!")


# Variablen
loaded_list = "new devicelist (not saved)"

try:

    while True:

        # ------------------------------------------------------------------------------------------------------
        # Menue

        selection = menue(loaded_list)

        # ------------------------------------------------------------------------------------------------------
        # Create devicelist

        if selection == 1:

            while True:

                if devicelist:
                    new = input(
                        "\n\n\n\tChanges to the loaded device list are not saved automatically! Would you like to continue anyway? (y/n): ")
                    i = 0
                    for j in yes:
                        if j == new:
                            i += 1
                    if i == 0:
                        print("\n\n\n\tThe process was canceled!")
                        print('\n\n\n\n\n')
                        break

                devicelist = []
                loaded_list = "new device list (not saved)"
                title("Creat devices")
                while True:
                    objekt = create_device()
                    devicelist.append(objekt)

                    rp = input("\n\twould you like to add another device? (y/n): ")
                    i = 0
                    for j in yes:
                        if j == rp:
                            i += 1
                    if i == 0:
                        print('\n\n\n\n\n')
                        break
                break

        # ------------------------------------------------------------------------------------------------------
        # add device to list

        elif selection == 2:

            while True:
                if devicelist:
                    while True:
                        objekt = create_device()
                        devicelist.append(objekt)

                        rp = input("\n\tWould you like to add another device? (y/n): ")
                        i = 0
                        for j in yes:
                            if j == rp:
                                i += 1
                        if i == 0:
                            print('\n\n\n\n\n')
                            break

                else:
                    new = input("\n\n\n\tNo device list loaded! Would you like to create a new one? (y/n): ")
                    i = 0
                    for j in yes:
                        if j == new:
                            i += 1
                    if i == 0:
                        print('\n\n\n\n\n')
                        break
                    else:
                        while True:
                            objekt = create_device()
                            devicelist.append(objekt)

                            rp = input("\n\tWould you like to add another device? (y/n): ")
                            i = 0
                            for j in yes:
                                if j == rp:
                                    i += 1
                            if i == 0:
                                print('\n\n\n\n\n')
                                break
                break

        # ------------------------------------------------------------------------------------------------------
        # device overview

        elif selection == 3:
            
            if devicelist:
                title("Device overview")
    
                for element in devicelist:
                    element.show()
            
            else:
                print("\n\n\n\n\n\n\t!!!ATTENTION - No device list loaded!")

            input("\n\n\t\t\t--Press any key to continue--")

        # ------------------------------------------------------------------------------------------------------
        # show device abilities

        elif selection == 4:
            
            if devicelist:
                title("Device Abilities")
                
                for element in devicelist:
                    element.abilities()

            else:
                print("\n\n\n\n\n\n\t!!!ATTENTION - No device list loaded!")

            input("\n\n\t\t\t--Press any key to continue--")

        # ------------------------------------------------------------------------------------------------------
        # show Sensor Data

        elif selection == 5:
            
            
            title("Get Sensor Data")
                
            try:
                client.connect(broker)
                print("Connected to MQTT Broker: " + broker + "->" + topic)
                print("\n\tPress crtl + c to abort")
                client.on_connect = on_connect
                client.on_message = on_message
                client.loop_forever

            except KeyboardInterrupt:
                client.disconnect()
                client.loop_stop()
            except:
                print("Can't reach MQTT Broker: " + broker)
                


#        devices = []
#                    if devicelist:
#                        for device in devicelist:
#                            if device.status == "online":
#                                devices.append(device)
#                        print("Devices online: " + f"{'{0}':<25}".format(devices.name))
#                        inp = input("Choos a Device to get Sensor Data: "+ f"{' ':<25}")
#                        for dev in devicelist:
#                            if inp in dev.name:
#                                dev.get()
#                                break
#                            else:
#                                print("\n\n\n\n\n\n\t!!!ATTENTION - Device not in List!")
#                                continue
#                    else:
#                        print("\n\n\n\n\n\n\t!!!ATTENTION - No device list loaded!")

        # ------------------------------------------------------------------------------------------------------
        # set actuator

        elif selection == 6:

            
            try:
                title("Send a command")
                while True:
                    devices = []
                    if devicelist:
                        for device in devicelist:
                            if device.status == "online":
                                devices.append(device)
                        print("Devices online: " + f"{'{0}':<25}".format(devices.name))
                        inp = input("Choos a Device to send a command: "+ f"{' ':<25}")
                        for dev in devicelist:
                            if inp in dev.name:
                                cmd = input("Command: "+ f"{' ':<25}")
                                dev.do(cmd)
                                break
                            else:
                                print("\n\n\n\n\n\n\t!!!ATTENTION - Device not in List!")
                                continue
                    else:
                        print("\n\n\n\n\n\n\t!!!ATTENTION - No device list loaded!")

            except KeyboardInterrupt:
                continue


    
        # ------------------------------------------------------------------------------------------------------
        # Laden

        elif selection == 8:

            while True:
            
                try:
                    if devicelist:
                        new = input("\n\n\n\tChanges to the loaded device list are not saved automatically! Would you like to continue anyway? (y/n): ")
                        i = 0
                        for j in yes:
                            if j == new:
                                i += 1
                        if i == 0:
                            print("\n\n\n\tThe process was canceled!")
                            print('\n\n\n\n\n')
                            break

                    data = load_list()
                    devicelist = data[0]
                    loaded_list = data[1]
                    break
                except KeyboardInterrupt:
                    break
            
            

        # ------------------------------------------------------------------------------------------------------
        # Speichern

        elif selection == 9:

            if devicelist:
                loaded_list = save_list(loaded_list)

            else:
                print("\n\n\n\n\n\n\t!!!ATTENTION - No device list loaded!")


        # ------------------------------------------------------------------------------------------------------
        # Programm Beenden

        elif selection == 0:
            print('\n\n\n\n\n\tSee ya!!!\n\n\n')
            break

except KeyboardInterrupt:
    selection = 0