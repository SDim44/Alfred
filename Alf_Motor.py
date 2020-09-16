#
#       Alfred Modul - Motorsteuerung
#
#       Stefan Dimnik, 14.03.2020
#
#       Mit diesem Programm wird die Motorsteuerung (H-Bridge) angesprochen.


#Libarys einbinden
import RPi.GPIO as GPIO
import time
import logging

#GPIO Warnungen deaktivieren
GPIO.setwarnings(False)

#--------------------------------------------------------------------------------
#Logging starten
Version = "V1.0"
logfile = 'logs/Alf_Main.log'
logging.basicConfig(filename=logfile,level=logging.DEBUG ,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.FileHandler(logfile, mode="w", encoding=None, delay=False)
logging.info("----------- Starte Alfred Modul - Motorsteuerung {0} ---------------".format(Version))


#--------------------------------------------------------------------------------
#Variablen definieren
LIN1 = 16
LIN2 = 20
LEN = 21

RIN1 = 24
RIN2 = 25
REN = 23

#--------------------------------------------------------------------------------
#Pins definieren
GPIO.setmode(GPIO.BCM)
GPIO.setup(LIN1,GPIO.OUT)
GPIO.setup(LIN2,GPIO.OUT)
GPIO.setup(LEN,GPIO.OUT)
GPIO.output(LIN1,GPIO.LOW)
GPIO.output(LIN2,GPIO.LOW)

GPIO.setup(RIN1,GPIO.OUT)
GPIO.setup(RIN2,GPIO.OUT)
GPIO.setup(REN,GPIO.OUT)
GPIO.output(RIN1,GPIO.LOW)
GPIO.output(RIN2,GPIO.LOW)

PWML = GPIO.PWM(LEN,1000)
PWMR = GPIO.PWM(REN,1000)

PWML.start(0)
PWMR.start(0)


#--------------------------------------------------------------------------------
#Funktion zur Ansteuerung der Motoren --- L=Links R=Rechts --- (x,x -> 0=Stop 1=forwaerts 2=rueckwaerts --- x,x) SpeedL,SpeedR=Geschwindigkeit L=linker R=rechter Motor ((0 - 100))
def move(L=0,R=0,SpeedL=50,SpeedR=50):
    
    #SpeedL = float(SpeedL)
    #SpeedR = float(SpeedR)
    
    #if SpeedL >= 50:
    #    SpeedL-=20
    #if SpeedR >= 50:
    #    SpeedR-=20
    PWML.ChangeDutyCycle(SpeedL)
    PWMR.ChangeDutyCycle(SpeedR)
    
    if L == 0:
        GPIO.output(LIN1,GPIO.LOW)
        GPIO.output(LIN2,GPIO.LOW)
        logging.debug("L - stop")  
        
    elif L == 1:
        GPIO.output(LIN1,GPIO.HIGH)
        GPIO.output(LIN2,GPIO.LOW)
        logging.debug("L - forwaerts - {0}".format(SpeedL))
    
    elif L == 2:
        GPIO.output(LIN1,GPIO.LOW)
        GPIO.output(LIN2,GPIO.HIGH)
        logging.debug("L - rueckwaerts - {0}".format(SpeedL))
        
    if R == 0:
        GPIO.output(RIN1,GPIO.HIGH)
        GPIO.output(RIN2,GPIO.LOW)
        logging.debug("R - stop")    
        
    elif R == 1:
        GPIO.output(RIN1,GPIO.HIGH)
        GPIO.output(RIN2,GPIO.LOW)
        logging.debug("R - forwaerts - {0}".format(SpeedR))
    
    elif R == 2:
        GPIO.output(RIN1,GPIO.LOW)
        GPIO.output(RIN2,GPIO.HIGH)
        logging.debug("R - rueckwaerts - {0}".format(SpeedR))
        
def stop():
    GPIO.output(LIN1,GPIO.LOW)
    GPIO.output(LIN2,GPIO.LOW)
    GPIO.output(RIN1,GPIO.LOW)
    GPIO.output(RIN2,GPIO.LOW)
    logging.debug("stop")
