#
#       Alfred Modul - LED
#
#       Stefan Dimnik, 14.03.2020
#
#       In diesem Programm koennen 2 LED's angesteuert werden.


#Libraries einbinden
import time
import RPi.GPIO as GPIO
import logging

#GPIO Warnungen deaktivieren
GPIO.setwarnings(False)

#Logging starten
Version = "V1.0"
logging.basicConfig(filename='logs/Alf_LED.log',level=logging.DEBUG ,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.debug("----------- Starte Alfred Modul - LED {0} ---------------".format(Version))

#Variablen definieren
R1 = 22
G1 = 17
B1 = 27
R2 = 26
G2 = 18
B2 = 12

#Pins definieren
GPIO.setmode(GPIO.BCM)

GPIO.setup(R1, GPIO.OUT)
GPIO.output (R1,0)
GPIO.setup(G1, GPIO.OUT)
GPIO.output (G1,0)
GPIO.setup(B1, GPIO.OUT)
GPIO.output (B1,0)

GPIO.setup(R2, GPIO.OUT)
GPIO.setup(G2, GPIO.OUT)
GPIO.setup(B2, GPIO.OUT)


#Funktion zum einschalten (x, 1=ein 0=aus --- R,G,B) -> Farbe einstellen (0-100)
def on(LED,R=0,G=0,B=0):
    if LED == 1:
        GPIO.output (R1,R)
        GPIO.output (G1,G)
        GPIO.output (B1,B)
    if LED == 2:
        GPIO.output (R2,R)
        GPIO.output (G2,G)
        GPIO.output (B2,B) 

def off(LED):
    if LED == 1:
        GPIO.output (R1,0)
        GPIO.output (G1,0)
        GPIO.output (B1,0)
    if LED == 2:
        GPIO.output (R2,0)
        GPIO.output (G2,0)
        GPIO.output (B2,0)
        