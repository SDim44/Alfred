#
#       Alfred Modul - Motorsteuerung
#
#       Stefan Dimnik, 28.07.2020
#
#       Dieses Programm ist für die Sprachausgabe zustaendig.

#Libarys einbinden
from subprocess import call
import time
import logging

#Logging starten
Version = "V1.0"
logging.basicConfig(filename='/home/pi/Alfred/Logs/Alf_Speech.log',level=logging.DEBUG ,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.debug("----------- Starte Alfred Modul - Sprachausgabe {0} ---------------".format(Version))


#Text als Sprache ausgeben
def say(speech):
  
    call(["espeak",speech])
    logging.debug("Alfred: {0}".format(speech))
