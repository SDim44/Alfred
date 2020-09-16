#
#       Alfred Main
#
#       Stefan Dimnik, 28.07.2020
#
#       Dieses Programm steuert die Soundausgabe von Alfred.


#Libarys
import time
import logging
import os
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
    cmd = "espeak -vde -s100" + ' "' + speech + '"'
    os.system(cmd)
    logging.info("Alfred: {0}".format(speech))

def r2d2(file):

    cmd = '/home/pi/Alfred/DATA/sounds/' + file
    call(["aplay",cmd])
    logging.info("Alfred: r2d2 - {0}".format(file))


#------------------------------------------------------------------------------------------------- 
#Main

print("------START AUDIO-INTERFACE------")

try:

    while True:
        
        time.sleep(0.2)

        Speech = speech()

        if speech_changed(Speech): #wird nur beim ersten durchlauf ausgefuehrt
                    try:
                        if Speech.find(".wav") != -1:
                            print("wav file")
                            Speech = Speech.strip(' \n\t')
                            r2d2(Speech)
                        else:
                            print("speech")
                            say(Speech)

                    except:
                        logging.error("----Fehler ist aufgetreten! --> speech_changed")
                        print("----Fehler ist aufgetreten! --> speech_changed")

except KeyboardInterrupt:
    print("------STOP AUDIO-INTERFACE------")