#
#       Alfred Main
#
#       Stefan Dimnik, 09.03.2020
#
#       Dieses Programm uebernimmt die Steuerung der Roboter-Platform.


#Libarys
import time
import logging
import subprocess
import RPi.GPIO as GPIO
import Alf_Motor as engin
import Alf_Verfolgung as alf
import Alf_Ultraschall as distance
import Alf_Pixy2 as pixy
import Alf_ToolConnect as tool
import Alf_LED as led
import Alf_Speech as ask

#Variablen
logfile = '/home/pi/Alfred/Logs/Alf_SpeechInterface.log'
global prev_mode
prev_mode = "0"

#GPIO Warnungen deaktivieren
GPIO.setwarnings(False)

#Start Logging
Version = "V1.0"
logging.basicConfig(filename=logfile,level=logging.DEBUG ,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.debug("----------- Starte Alfred {0} ---------------".format(Version))
 
#------------------------------------------------------------------------------------------------- 

#Funktion - Modus auslesen
def mode():
    config = open("/var/www/html/mode.conf")
    set = config.read()
    config.close()
    #set = int(set)
    return set
    logging.debug("mode.conf wird ausgelesen: {0}".format(set))

def mod_changed(m):
    global prev_mode

    if prev_mode == m:
        return False

    else:
        prev_mode = m
        return True
   
#Main

try:
    print("------START------")
    while True:
              
        Mode = mode()
 
        if Mode == "1":
            if mod_changed(Mode):
                ask.r2d2("verfolgung.wav")

            
        elif Mode == "2": 
            if mod_changed(Mode):
                ask.r2d2("ladestation.wav")
            
        elif Mode == "3": #Tool Mode
            if mod_changed(Mode):    
                ask.say("Tool Mode")                      

        elif Mode == "5": #Face detection + follow
            if mod_changed(Mode):
                ask.say("Trying to find Humans")



except KeyboardInterrupt:
    GPIO.cleanup()
