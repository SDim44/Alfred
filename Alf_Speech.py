#
#       Alfred Main
#
#       Stefan Dimnik, 28.07.2020
#
#       Dieses Programm steuert die Soundausgabe von Alfred.


#Libarys
import time
import logging
from subprocess import call

#------------------------------------------------------------------------------------------------- 
#Variablen
global prev_mode
prev_mode = "0"

#------------------------------------------------------------------------------------------------- 
#GPIO Warnungen deaktivieren
GPIO.setwarnings(False)

#------------------------------------------------------------------------------------------------- 
#Start Logging
Version = "V1.0"
logfile = 'logs/Alf_Speech.log'
logging.basicConfig(filename=logfile,level=logging.DEBUG ,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.FileHandler(logfile, mode="w", encoding=None, delay=False)
logging.info("----------- Starte Alfred Speech {0} ---------------".format(Version))


#------------------------------------------------------------------------------------------------- 
#Funktion - Modus auslesen
def mode():
    config = open("mode.conf")
    set = config.read()
    config.close()
    #set = int(set)
    return set
    logging.info("mode.conf wird ausgelesen: {0}".format(set))

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
    logging.info("Alfred: {0}".format(speech))

def r2d2(file):
    cmd = 'DATA/sounds/' + file
    call(["aplay",cmd])
    logging.info("Alfred: r2d2 - {0}".format(file))


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
                r2d2("toolmode.wav")                      

        elif Mode == "5": #Face detection + follow
            if mod_changed(Mode):
                say("Trying to find Humans")



except KeyboardInterrupt:
    GPIO.cleanup()

