#
#       Alfred Main
#
#       Stefan Dimnik, 28.07.2020
#
#       Dieses Programm steuert die Soundausgabe des Roboters.


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
from subprocess import call

#Variablen
logfile = 'logs/Alf_Speech.log'
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
   
#Text als Sprache ausgeben
def say(speech):
  
    call(["espeak",speech])
    logging.debug("Alfred: {0}".format(speech))

def r2d2(file):
    path = "DATA/sounds/" + file
    call(["aplay",path])
    logging.debug("Alfred: r2d2 - {0}".format(file))

#------------------------------------------------------------------------------------------------- 


#Main

try:
    print("------START------")
    while True:
              
        Mode = mode()
 
        if Mode == "1":
            if mod_changed(Mode):
                r2d2("verfolgung.wav")

            
        elif Mode == "2": 
            if mod_changed(Mode):
                r2d2("ladestation.wav")
            
        elif Mode == "3": #Tool Mode
            if mod_changed(Mode):    
                say("Tool Mode")                      

        elif Mode == "5": #Face detection + follow
            if mod_changed(Mode):
                say("Trying to find Humans")



except KeyboardInterrupt:
    GPIO.cleanup()

