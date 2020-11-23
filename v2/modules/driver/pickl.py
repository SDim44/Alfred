#       Pickle Files
#
#       Autor:              Stefan Dimnik
#       Date:               04.11.2020
#       Python:             3.7
#       Projekt Details:    https://github.com/SDim44/Alfred
#       ------------------------------------------------------------
#       
#       V0.1
#       Load and Save Pickle Files

# ------------------------------------------------------------------------------------------------------
# load device list

def load_list(path="devicelist.pkl"):
    try:
        datenobjekt = open(path, "rb")
        objekt = pickle.load(datenobjekt)
        datenobjekt.close()
        return objekt

    except:
        print("\n\n\n\n\n\n\t!!!ATTENTION - The file was not found or is damaged!")


# ------------------------------------------------------------------------------------------------------
# save device list

def save_list(devicelist,path="devicelist.pkl"):

    try:
        if ".pkl" not in path:
            path = (str(path) + ".pkl")

        datenobjekt = open(path, "wb")
        pickle.dump(devicelist, datenobjekt)
        datenobjekt.close()

    except:
        print("\n\n\n\n\n\n\t!!!ATTENTION - Location not found! {0}".format(path))
