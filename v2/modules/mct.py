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
from datetime import datetime
import time
import device as cla


# Variable
width_menue = 70  # Window width

yes = 'j', 'J', 'y', 'Y', 'ja', 'Ja', 'yes', 'Yes'
forbidden = "!$%&/()=?-+*"
numbers = "0123456789"

loaded_list = "new devicelist (not saved)"


# Viriables for connection
broker = "testipi"
topic = "homestead/#"
#client = mqtt.Client()

# ------------------------------------------------------------------------------------------------------
# Menue

def menue(loaded_list):

    while True:
        try:
            title("Device Manager")

            if devicelist:
                print("\tDevicelist Loaded -> {0}".format(loaded_list))

            else:
                print("\t(No device list loaded!)")

            print("\n")
            print("\t\t" + f"{'Create new device  ':.<50}" + "  1")
            print("\t\t" + f"{'Show devices  ':.<50}" + "  2")
            print("\t\t" + f"{'Show available commands  ':.<50}" + "  3")
            print("\t\t" + f"{'Update Devicelist':.<50}" + "  4")
            print("\t{0:^{1}}".format(" ", width_menue))
            print("\t\t" + f"{'Execute command  (...in developement)':.<50}" + "  5")
            print("\t{0:^{1}}".format(" ", width_menue))
            print("\t\t" + f"{'Quit  ':.<50}" + "  0")
            print("\t{0:^{1}}".format(" ", width_menue))

            # Eingabe
            eingabe = int(input("\n\t\t\t" + f"{'Choose an action': <42}" + ": "))
            if (eingabe < 0) or (eingabe > 5):
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


##########################################################################
#def on_connect(client, userdata, flags, rc):
#    try:
#        client.subscribe(topic)
#        print("connected")
#    except:
#        print("Broker is down!!!")
#
#def on_message(client, userdata, message):
#    clt = str(client.payload.decode("utf-8"))
#    udata = str(userdata.payload.decode("utf-8"))
#    msg = str(message.payload.decode("utf-8"))
#    print("--> {0}, {1}, {2}".format(clt,udata,msg))


def load_devicelist():
    import device
    from os import listdir
    from pathlib import Path
    
    devicelist = []
    
    path = Path("modules/programdata/")
    filelist = listdir(path)

    for dev_file in filelist:
        if ".pkl" in dev_file:
            dev_object = cla.load_devic(dev_file)

            devicelist.append(dev_object)

    return devicelist
        

# ------------------------------------------------------------------------------------------------------
# Main

import device

# Welcometext
print("\n\n\n\n\tWelcome to Device Manager!")


# Variablen
devicelist = []

try:
    devicelist = load_devicelist()
    loaded_list = str(datetime.now().strftime("%H:%M:%S"))
except:
        loaded_list = "Loading Failed!!"


try:

    while True:

        # ------------------------------------------------------------------------------------------------------
        # Menue

        selection = menue(loaded_list)

        # ------------------------------------------------------------------------------------------------------
        # Create new device

        if selection == 1:

            title("Creat devices")
            cla.add()
            
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
    
                for element in devicelist:
                    element.show()
            
            else:
                print("\n\n\n\n\n\n\t!!!ATTENTION - No device list loaded!")

            input("\n\n\t\t\t--Press any key to continue--")

        # ------------------------------------------------------------------------------------------------------
        # show commands

        elif selection == 3:
            
            if devicelist:
                title("Device Abilities")
                
                for d in devicelist:
                    print("\n\n\n\t{0}".format(d.name))
                    for cmd in d.commandlist:
                        print("\t\t{0}".format(cmd))

            else:
                print("\n\n\n\n\n\n\t!!!ATTENTION - No device list loaded!")

            input("\n\n\t\t\t--Press any key to continue--")

        # ------------------------------------------------------------------------------------------------------
        # Update Devicelist

        elif selection == 4:
            try:
                devicelist = load_devicelist()
                loaded_list = str(datetime.now().strftime("%H:%M:%S"))
            except:
                loaded_list = "Loading Failed!!"


        # ------------------------------------------------------------------------------------------------------    
        # execute command

        elif selection == 5:
            pass

        # ------------------------------------------------------------------------------------------------------
        # Programm Beenden

        elif selection == 0:
            print('\n\n\n\n\n\tSee ya!!!\n\n\n')
            break

except KeyboardInterrupt:
    selection = 0