#
#       Alfred Main
#
#       Stefan Dimnik, 09.03.2020
#
#       Dieses Programm uebernimmt die Steuerung der Roboter-Platform.
#
#       V0.2 
#       Laufzeitfehler behoben und logging erweitert
#


#Libarys
import time
import logging
import os
import RPi.GPIO as GPIO
import Alf_Motor as engin
import Alf_Verfolgung as alf
import Alf_Ultraschall as distance
import Alf_Pixy2 as pixy
import Alf_ToolConnect as tool
import Alf_LED as led

#--------------------------------------------------------------------------------
#Variablen
global logfile
logfile = 'logs/Alf_Main.log'
global prev_mode
prev_mode = "0"

#--------------------------------------------------------------------------------
#GPIO Warnungen deaktivieren
GPIO.setwarnings(False)

#--------------------------------------------------------------------------------
#Start Logging
Version = "V0.2"
logging.basicConfig(filename=logfile,level=logging.debug ,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.FileHandler(logfile, mode="w", encoding=None, delay=False)
logging.info("----------- Starte Alfred {0} ---------------".format(Version))


#--------------------------------------------------------------------------------
#Funktionen
#--------------------------------------------------------------------------------
#Funktion - Modus auslesen
def mode():
    try:    
        config = open("mode.conf")
        set = config.read()
        config.close()
        set = set.strip(' \n\t')
        return set
        logging.info("mode.conf wird ausgelesen: {0}".format(set))
    except:
        logging.error("!!! Mode kann nicht ausgelesen werden!")

#--------------------------------------------------------------------------------

def mod_changed(m):
    global prev_mode

    if prev_mode == m:
        return False

    else:
        prev_mode = m
        return True

#--------------------------------------------------------------------------------

def set_emotion(num): 
    wert = str(num)
    config = open("emotion.conf","w")
    config.write(wert)
    config.close

#--------------------------------------------------------------------------------   
def systemcheck():
    logging.info("----Systemcheck wird durchgefuehrt----")
    
    #Tool ueberpruefen
    logging.info("----> Ladescreen erzeugen")
    set_emotion("99.gif")
    
    #------------
    
    try:
        logging.info("----> Alte logfiles entfernen")
        for root, dirs, files in os.walk("logs/"):
            for file in files:
                os.remove(os.path.join(root, file))
    except:
        logging.warning("!!! Tool check faild")
    
    #------------
    
    try:
        toolcheck = tool.get()
        logging.info("----> Tool OK: {0}".format(toolcheck))    
    except:
        logging.warning("!!! Tool check faild")
    
    
    #Systemcheck beenden (Zwinkern)
    set_emotion("1.gif")
    time.sleep(1)
    set_emotion("2.gif")
    time.sleep(1)
    set_emotion("1.gif")


#--------------------------------------------------------------------------------
#Main
#--------------------------------------------------------------------------------

i = 0
try:

#--------------------------------------------------------------------------------
#System Check
    
    systemcheck()

    
#--------------------------------------------------------------------------------
#Schleife

    logging.info("------START------")
    while True: 
        
        Mode = mode()
        time.sleep(0.2) #Verhindert Laufzeitfehler
 
#--------------------------------------------------------------------------------
# Mode 1  
        if Mode == "1":
            #logging.info("Mode 1 - Objekt 1")
            try:          
                print("\n{0}".format(pixy.get(1)))
                print("\nWall detected: {0}".format(distance.wall()))
                alf.hunt(1)
            except:
                logging.error("----Fehler ist aufgetreten! --> loop")
            
            if mod_changed(Mode): #wird nur beim ersten durchlauf ausgefuehrt
                try:
                    led.on(1,0,100,0)

                except:
                    logging.error("----Fehler ist aufgetreten! --> mod_changed")

#--------------------------------------------------------------------------------
# Mode 2              
        elif Mode == "2":
            print("Mode 2 - Objekt 2")
            try:
                print("\n{0}".format(pixy.get(2)))
                print("\nWall detected: {0}".format(distance.wall()))
                alf.hunt(2)
            except:
                logging.error("----Fehler ist aufgetreten! --> loop")
            
            if mod_changed(Mode): #wird nur beim ersten durchlauf ausgefuehrt
                try:
                    led.on(1,100,0,0)
                except:
                    logging.error("----Fehler ist aufgetreten! --> mod_changed")
#--------------------------------------------------------------------------------
# Mode 3             
        elif Mode == "3": #Tool Mode
            print("Mode 3 - Toolmodus")
            try:
                engin.move(0,0,0,0)
            except:
                logging.error("----Fehler ist aufgetreten!")
            
            if mod_changed(Mode): #wird nur beim ersten durchlauf ausgefuehrt   
                try:
                    led.on(1,0,0,100)
                except:
                    logging.error("----Fehler ist aufgetreten! --> mod_changed")

#--------------------------------------------------------------------------------
# Mode 4 (keine Funktion)             
        elif Mode == "4": #Test Mode
            print("\n\nMode 4 - Testmodus")
            try:
                led.off(1)
                led.on(2,100,0,0)
            except:
                logging.error("----Fehler ist aufgetreten!")
            
            if mod_changed(Mode): #wird nur beim ersten durchlauf ausgefuehrt
                try:
                    pass
                except:
                    logging.error("----Fehler ist aufgetreten! --> mod_changed")    
#--------------------------------------------------------------------------------
# Mode 5  (keine Funktion)      
        elif Mode == "5": #Face detection + follow
            print("\n\nMode 5 - Testmodus")
            try:
                led.off(1)
                led.on(2,100,0,0)
            except:
                logging.error("----Fehler ist aufgetreten!")
            
            if mod_changed(Mode): #wird nur beim ersten durchlauf ausgefuehrt
                try:
                    pass
                except:
                    logging.error("----Fehler ist aufgetreten! --> mod_changed")


#--------------------------------------------------------------------------------
# Exceptions

except KeyboardInterrupt:
    GPIO.cleanup()
    led.off(1)
    led.off(2)
