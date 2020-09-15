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
import Alf_Temperatur as temperatur

#------------------------------------------------------------------------------------------------- 
#Variablen
global prev_speech
prev_speech = "0"

#------------------------------------------------------------------------------------------------- 
#Start Logging
Version = "V1.0"
logfile = 'logs/Alf_Speech.log'
logging.basicConfig(filename=logfile,level=logging.DEBUG ,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.FileHandler(logfile, mode="w", encoding=None, delay=False)
logging.info("----------- Starte Alfred Speech {0} ---------------".format(Version))


#------------------------------------------------------------------------------------------------- 
#Funktion - Modus auslesen

def speech():
    config = open("speech.conf")
    set = config.read()
    config.close()
    return set
    logging.info("speech.conf wird ausgelesen: {0}".format(set))

def speech_changed(m):
    global prev_speech

    if prev_speech == m:
        return False

    else:
        prev_speech = m
        return True
   
#Text als Sprache ausgeben
def say(speech):
  
    print(speech)
    call(["espeak",speech])
    logging.info("Alfred: {0}".format(speech))

def r2d2(file):

    cmd = 'DATA/sounds/' + file
    print(cmd)
    call(["aplay",cmd])
    logging.info("Alfred: r2d2 - {0}".format(file))


#------------------------------------------------------------------------------------------------- 
#Main

print("------START------")

while True:
    time.sleep(0.2)
      
    Speech = speech()
    print(Speech)

    if speech_changed(Speech): #wird nur beim ersten durchlauf ausgefuehrt
                try:
                    if name.find(".wav") != -1:
                        print(Speech)
                        r2d2(Speech)
                    else:
                        print(Speech)
                        say(Speech)

                except:
                    logging.error("----Fehler ist aufgetreten! --> speech_changed")

    

    
#-------------------------------------------------------------------------------------------------- 
    
#    if Speech == "1":
#        if mod_changed(Mode):
#            r2d2("verfolgung.wav")

        
#    elif Mode == "2": 
#        if mod_changed(Mode):
#            r2d2("ladestation.wav")
        
#    elif Mode == "3": #Tool Mode
#        if mod_changed(Mode):    
#            r2d2("toolmode.wav")                      

#    elif Mode == "5": #Face detection + follow
#        if mod_changed(Mode):
#            say("Trying to find Humans")

#    elif Mode == "0": #Startup
#        say("Hallo, ich bin Alfred")
#        

