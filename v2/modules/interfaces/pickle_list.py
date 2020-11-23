#       Pickle Load and Save
#
#       Autor:              Stefan Dimnik
#       Date:               04.11.2020
#       Python:             3.7
#       Projekt Details:    https://github.com/SDim44/Alfred
#       ------------------------------------------------------------
#       
#       V01.0
#       Load and Save Pickle Objects
#       ------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------
# Libraries

import pickle
from pathlib import Path

# ------------------------------------------------------------------------------------------------------
# load command list

def load_list(path):

    location = Path(path)
    try:
        datenobjekt = open(location, "rb")
        objekt = pickle.load(datenobjekt)
        datenobjekt.close()
        return objekt

    except:
        print("\n\n\n\n\n\n\t!!!ATTENTION - The file was not found or is damaged!  - Use forward slashes -> /  ")


# ------------------------------------------------------------------------------------------------------
# save command list

def save_list(objectlist,path):

    try:
        if ".pkl" not in path:
            path = (str(path) + ".pkl")

        location = Path(path)

        datenobjekt = open(location, "wb")
        pickle.dump(devicelist, datenobjekt)
        datenobjekt.close()

    except:
        print("\n\n\n\n\n\n\t!!!ATTENTION - Location not found! - Use forward slashes -> /  ")