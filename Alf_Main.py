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

#Variablen
logfile = 'logs/Alf_Main.log'
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
    config = open("mode.conf")
    set = config.read()
    config.close()
    set = set.strip(' \n\t')
    return set
    logging.debug("mode.conf wird ausgelesen: {0}".format(set))

def mod_changed(m):
    global prev_mode

    if prev_mode == m:
        return False

    else:
        prev_mode = m
        return True

def set_emotion(num): 
    wert = str(num)
    config = open("emotion.conf","w")
    config.write(wert)
    config.close
   
def systemcheck():
    print("----Systemcheck wird durchgefuehrt")
    logging.debug("----Systemcheck wird durchgefuehrt")
    
    #Tool ueberpruefen
    try:
        toolcheck = tool.get()
        print(toolcheck)
        logging.debug("Tool OK: {0}".format(toolcheck))
    
    except:
        logging.debug("Tool check faild")
    
    
    
    #Systemcheck beenden (Zwinkern)
    set_emotion("2.gif")
    time.sleep(1.5)
    set_emotion("1.gif")









#Main
i = 0
try:

    #System Check
    set_emotion("1.gif")
    systemcheck()

    #--------------------------------
    #Schleife

    print("------START------")
    while True: 
        
        Mode = mode()
 
        if Mode == "1":
            print("Mode 1 - Objekt 1")
            print("\n{0}".format(pixy.get(1)))
            print("\nWall detected: {0}".format(distance.wall()))
            led.on(1,0,100,0)
            alf.hunt(1)
            if mod_changed(Mode):
                pass

            
        elif Mode == "2":
            print("Mode 2 - Objekt 2")
            print("\n{0}".format(pixy.get(2)))
            print("\nWall detected: {0}".format(distance.wall()))
            led.on(1,100,0,0)
            alf.hunt(2)
            if mod_changed(Mode):
                pass
            
        elif Mode == "3": #Tool Mode
            print("Mode 3 - Toolmodus")
            led.on(1,0,0,100)
            engin.move(0,0,0,0)
            if mod_changed(Mode):    
                pass                    
            
        elif Mode == "4": #Test Mode
            #messure = distance.get(1)
            #print("\n\nMode 4 - Testmodus")
            print("\n\nUltraschall ----> {0}".format(messure))
            led.off(1)
            led.on(2,100,0,0)
        
        elif Mode == "5": #Face detection + follow
            if mod_changed(Mode):
                pass



except KeyboardInterrupt:
    GPIO.cleanup()
