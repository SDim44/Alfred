#       Class Commandlist
#
#       Autor:              Stefan Dimnik
#       Date:               04.11.2020
#       Python:             3.7
#       Projekt Details:    https://github.com/SDim44/Alfred
#       ------------------------------------------------------------
#       
#       V0.1
#       Saves and Load Commands
#       ------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------
# Libraries



# Variable


# ------------------------------------------------------------------------------------------------------
# define class

class command(object):
    def __init__(self,name,description,driver,protocol):
        self.name = name
        self.description = description
        self.driver = driver
        self.protocol = protocol()

    # --------------------------------------------------------------------------------------------------------
    # Methodes

    def show(self):
        ret = print("\n\t" + f"{'{0}':^15}" + "|" + f"{'{1}' :^15}" + "|"  f"{'{2}' :^15}" .format(self.name, self.unit, self.description))
        return ret

    def protocol(self):
        import self.driver as d
        supported_protocol = d.supported_protocol
        return supported_protocol

# ------------------------------------------------------------------------------------------------------
# Functions

def load_commandlist():
    import interfaces.pickle_list as pk
    pk.load_list("programdata/devicelist.pkl")


def save_commandlist(commandlist):
    import interfaces.pickle_list as pk
    pk.save_list(commandlist,"programdata/commandlist.pkl")

def create_command():
    import mct
    while True:
        try:
            mct.title("Command-Manager")
            print("\n")
            print("\t\t" + f"{'Add Commands  ':.<50}" + "  1")
            print("\t\t" + f"{'Show Commands  ':.<50}" + "  2")
            print("\t{0:^{1}}".format(" ", mct.width_menue))
            print("\t\t" + f"{'Quit  ':.<50}" + "  0")
            print("\t{0:^{1}}".format(" ", mct.width_menue))

            # Eingabe
            eingabe = int(input("\n\t\t\t" + f"{'Choose an action': <42}" + ": "))
            if (eingabe < 0) or (eingabe > 2):
                print(
                    "\n\n\n\n\n\n\n\t\t!!! Please use a number from the menu !!!\n\n")
                continue
            return eingabe
            break

        except ValueError:
            print("\n\n\n\n\n\n\n\t!!! You entered an incorrect data type !!!")
            print("\t!!! Please use a number from the menu !!!")
            continue

    # ------------------------------------------------------------------
    # Name
    print("\n\tEnter the following information: ")
    while True:
        name = input("\n\t\t" + f"{'Name  ' :<25}" + ": ")
        break
    # ------------------------------------------------------------------
    # description
    while True:
        description = input("\n\t\t" + f"{'Description  ' :<25}" + ": ")
        break
    # ------------------------------------------------------------------
    # driver
    from os import listdir
    from pathlib import Path
    path = Path("modules/driver")
    filelist = listdir(path)
    driverlist = []
    while True:
        for dr in filelist:
            dr_name = dr.strip(".py")
            driverlist.append(dr_name)
        print(driverlist)
        driver = input("\n\t\t" + f"{'Choose a Driver  ' :<25}" + ": ")
        if driver in driverlist:
            break
        else:
            continue