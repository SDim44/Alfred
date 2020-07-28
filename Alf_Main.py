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
logfile = '/home/pi/Alfred/Logs/Alf_Main.log'
global prev_mode
prev_mode = "0"

#GPIO Warnungen deaktivieren
GPIO.setwarnings(False)

#Start Logging
Version = "V1.0"
logging.basicConfig(filename=logfile,level=logging.DEBUG ,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.debug("----------- Starte Alfred {0} ---------------".format(Version))
 
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
   
def systemcheck():
    print("----Systemcheck wird durchgefuehrt")
    print(tool.get())


#Main
i = 0
try:
    print("------START------")
    while True: #System Check
        
        #if i == 100:
        #    systemcheck()
        #    i = 0
        #i+=1
        
        Mode = mode()
 
        if Mode == "1":
            print("Mode 1 - Objekt 1")
            print("\n{0}".format(pixy.get(1)))
            led.on(1,0,100,0)
            alf.hunt(1)
            if mod_changed(Mode):
                ask.say("Go to Object 1")

            
        elif Mode == "2":
            print("Mode 2 - Objekt 2")
            print("\n{0}".format(pixy.get(2)))
            led.on(1,100,0,0)
            alf.hunt(2)
            if mod_changed(Mode):
                ask.say("Back to Charging Station")
            
        elif Mode == "3": #Tool Mode
            print("Mode 3 - Toolmodus")
            led.on(1,0,0,100)
            engin.move(0,0,0,0)
            if mod_changed(Mode):    
                ask.say("Tool Mode")                      
            
        elif Mode == "4": #Test Mode
            #messure = distance.get(1)
            #print("\n\nMode 4 - Testmodus")
            print("\n\nUltraschall ----> {0}".format(messure))
            led.off(1)
            led.on(2,100,0,0)
        
        elif Mode == "5": #Face detection + follow
            if mod_changed(Mode):
                ask.say("Trying to find Humans")



except KeyboardInterrupt:
    GPIO.cleanup()
