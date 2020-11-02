#
#       Alfred Main
#
#       Stefan Dimnik, 09.03.2020
#
#       Dieses Programm uebernimmt die Steuerung der Roboter-Platform.
#
#       V0.2 
#       Laufzeitfehler behoben und logging erweitert.
#

_wired = False

#Libarys
try: 
    import time
    import logging
    import os
    import RPi.GPIO as GPIO
    import Alf_WebGUI as wg
    import Alf_Modules as mdl

    if _wired:
        import Alf_Verfolgung as alf
        import Alf_Motor as engin
        import Alf_Ultraschall as distance
        import Alf_Pixy2 as pixy
        import Alf_ToolConnect as tool
        import Alf_LED as led
        import Alf_Temperatur as temperatur
    

except:
    print("!!! Library Failed")


#--------------------------------------------------------------------------------
#Variablen
global logfile
logfile = 'logs/Alf_Main.log'
global prev_mode
prev_mode = "0"

ACTIONTIME = 45
BLINK = ACTIONTIME - 2

#--------------------------------------------------------------------------------
#GPIO Warnungen deaktivieren
GPIO.setwarnings(False)

#--------------------------------------------------------------------------------
#Start Logging
Version = "V0.2"
logging.basicConfig(filename=logfile,level=logging.DEBUG ,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.FileHandler(logfile, mode="w", encoding=None, delay=False)
logging.info("----------- Starte Alfred {0} ---------------".format(Version))
print("----------- Starte Alfred {0} ---------------".format(Version))


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
#Modus in Main aendern
def setmode(num): 
    wert = str(num)
    config = open("mode.conf","w")
    config.write(wert)
    config.close

#--------------------------------------------------------------------------------
#Sprachbefehle setzten
def set_speech(text): 
    wert = str(text)
    config = open("speech.conf","w")
    config.write(wert)
    config.close

#--------------------------------------------------------------------------------
#Check ob Modus seit dem letztem durchlauf geaendert wurde
def mod_changed(m):
    global prev_mode

    if prev_mode == m:
        return False

    else:
        prev_mode = m
        return True

#--------------------------------------------------------------------------------
#Emotion aendern
def set_emotion(file): 
    wert = str(file)
    config = open("emotion.conf","w")
    config.write(wert)
    config.close

def say(speech):
    cmd = "espeak -vde -s100" + ' "' + speech + '"'
    os.system(cmd)
    logging.info("Alfred: {0}".format(speech))

#--------------------------------------------------------------------------------   
def systemcheck():

    logging.info("----Systemcheck wird durchgefuehrt----")
    print("----Systemcheck wird durchgefuehrt----")
    
    #------------
    #Tool ueberpruefen

    devicelist = mdl.load_list()
    logging.info("---->Devece list loaded")
    for dev in devicelist:
        logging.info(dev.name)
        print(dev.name)

        if dev.protocol == "i2c":
            print("in if")
            for act in dev.actuatorlist:
                print(act.name)
                act.do(dev.protocol,30)
                act.do(dev.protocol,0)



    

    logging.info("----> Ladescreen erzeugen")
    set_emotion("AKZMM_001.gif")
    time.sleep(1)
    
    #------------
    #Startmodus festlegen
    
    logging.info("----> Startmodus festlegen")
    time.sleep(1)
    
    #------------
    try:
        toolcheck = tool.get()
        logging.info("----> Tool OK: {0}".format(toolcheck))    
    except:
        logging.warning("!!! Tool check faild")
    
     #------------
    if _wired:
        tem = temperatur.readtemp()
    #------------
    #Systemcheck beenden (Zwinkern)

    time.sleep(1.5)
    set_emotion("AKZMM_004_1.gif")
    time.sleep(1)
    set_emotion("AKMU_002_1.gif")
    time.sleep(1)
    set_emotion("AKZMM_004_1.gif")
    time.sleep(1)
    set_emotion("AKMU_002_1.gif")
    if _wired:
        say("Hallo, mein name ist Alfred") 
        #time.sleep(4)
        temperat= "Die aktuelle Temperatur betregt " + str(tem) + " Grad Celsius"
        say(temperat)
    #time.sleep(5)
    setmode(3)


#--------------------------------------------------------------------------------
#Main
#--------------------------------------------------------------------------------

timer = 0
try:

#--------------------------------------------------------------------------------
#System Check
    
    systemcheck()

    
#--------------------------------------------------------------------------------
#Schleife

    logging.info("------Alfred is running!------")
    print("------Alfred is running!------")
    while True: 
        
        time.sleep(0.2) #Verhindert Laufzeitfehler
        

        #Variablen setzten
        Mode = mode() #Mode auslesen
        if _wired:
            wall = distance.wall() # Ultraschallsensoren auslesen
        #wall = False
        pixysig = "0"
 
#--------------------------------------------------------------------------------
# Mode 1  
        if Mode == "1":
            logging.info("Mode 1 - Objekt 1")
            
            if _wired:
                try:
                    pixysig = pixy.get(1)
                    print("\n{0}".format(pixysig))        
                    alf.hunt(1)

                    #-----------------------------------------
                    #Emotions
                    if pixysig[1] == 0: # mitte
                        if timer>=BLINK and timer<=ACTIONTIME:
                            set_emotion("AKZMM_004_1.gif")
                        else:
                            set_emotion("AKMU_002_1.gif")
                    
                    elif pixysig[1] >= 105 and pixysig[1] <= 210: # mitte
                        if timer>=BLINK and timer<=ACTIONTIME:
                            set_emotion("AKZMM_004_2.gif")
                        else:
                            set_emotion("AKMU_003_1.gif")

                    elif pixysig[1] < 105 and pixysig[1] > 0: #rechts
                        if timer>=BLINK and timer<=ACTIONTIME:
                            set_emotion("AKZMR_004.gif")
                        else:
                            set_emotion("AKRU_003_1.gif")
                    
                    elif pixysig[1] > 210 and pixysig[1] <= 315: #links
                        if timer>=BLINK and timer<=ACTIONTIME:
                            set_emotion("AKZML_004.gif")
                        else:
                            set_emotion("AKLU_003_1.gif")
                    #-----------------------------------------

                except:
                    logging.error("----Fehler ist aufgetreten! --> loop")
                
                if mod_changed(Mode): #wird nur beim ersten durchlauf ausgefuehrt
                    try:
                        led.on(1,0,100,0)
                        set_speech("Ich folge ihnen Master")

                    except:
                        logging.error("----Fehler ist aufgetreten! --> mod_changed")

#--------------------------------------------------------------------------------
# Mode 2              
        elif Mode == "2":
            logging.info("Mode 2 - Objekt 2")
            if _wired:
                try:
                    pixysig = pixy.get(2)
                    logging.info("\n{0}".format(pixysig))
                    alf.hunt(2)

                    #-----------------------------------------
                    #Emotions
                    if pixysig[1] == 0: # mitte
                        if timer>=BLINK and timer<=ACTIONTIME:
                            set_emotion("AKZMM_004_1.gif")
                        else:
                            set_emotion("AKMU_002_1.gif")
                    
                    elif pixysig[1] >= 105 and pixysig[1] <= 210: # mitte
                        if timer>=BLINK and timer<=ACTIONTIME:
                            set_emotion("AKZMM_004_2.gif")
                        else:
                            set_emotion("AKMU_003_1.gif")

                    elif pixysig[1] < 105 and pixysig[1] > 0: #rechts
                        if timer>=BLINK and timer<=ACTIONTIME:
                            set_emotion("AKZMR_004.gif")
                        else:
                            set_emotion("AKRU_003_1.gif")
                    
                    elif pixysig[1] > 210 and pixysig[1] <= 315: #links
                        if timer>=BLINK and timer<=ACTIONTIME:
                            set_emotion("AKZML_004.gif")
                        else:
                            set_emotion("AKLU_003_1.gif")
                    #-----------------------------------------        

                except:
                    logging.error("----Fehler ist aufgetreten! --> loop")
                
                if mod_changed(Mode): #wird nur beim ersten durchlauf ausgefuehrt
                    try:
                        led.on(1,100,0,0)
                        set_speech("ich verlasse sie nun, master")
                    except:
                        logging.error("----Fehler ist aufgetreten! --> mod_changed")
                    
#--------------------------------------------------------------------------------
# Mode 3             
        elif Mode == "3": #Tool Mode
            logging.info("Mode 3 - Toolmodus")
            try:
                if _wired:
                    engin.move(0,0,0,0)
            except:
                logging.error("----Fehler ist aufgetreten! --> loop")

            if timer>=BLINK and timer<=ACTIONTIME:
                set_emotion("AKZMM_005_1.gif")
            else:
                set_emotion("AKMU_009_2.gif")
            
            if mod_changed(Mode): #wird nur beim ersten durchlauf ausgefuehrt   
                try:
                    if _wired:
                        led.on(1,0,0,100)
                    set_speech("die manuelle steuerung wurde ausgewaehlt, was nun, master")
                    wg.run()
                    
                except:
                    logging.error("----Fehler ist aufgetreten! --> mod_changed")

#--------------------------------------------------------------------------------
# Mode 4 (keine Funktion)             
        elif Mode == "4": #Test Mode
            logging.info("\n\nMode 4 - Testmodus")
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
            logging.info("\n\nMode 5 - Testmodus")
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
#Emotionen anzeigen
        
        if _wired:
            if wall == True:
                set_emotion("AKZMM_004_1.gif")
                set_speech("oh, eine wand")
                logging.info("----> Wall detected!")
        
        if timer == ACTIONTIME:
            timer = 0
            
        timer+=1

#--------------------------------------------------------------------------------
# Exceptions
except KeyboardInterrupt:
    led.off(1)
    led.off(2)
    GPIO.cleanup()
