#
#       Alfred Modul - Ultraschall Sensoren
#
#       Stefan Dimnik, 14.03.2020
#
#       In diesem Programm koennen 2 Stueck Ultraschall Sensoren ausglesen werden.
#
#       ACHTUNG!! Aufrufe muessen Zeitlich abgegrenz werden (Fehler bei schnellen aufrufen)


#Libraries einbinden
import RPi.GPIO as GPIO
import time
import logging

#GPIO Warnungen deaktivieren
GPIO.setwarnings(False)

#Logging starten
Version = "V0.2" #Funktioniert nicht - Sensor scheinbar defekt
#logfile = 'logs/Alf_Ultraschall.log'
#logging.basicConfig(filename=logfile,level=logging.DEBUG ,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
#logging.FileHandler(logfile, mode="w", encoding=None, delay=False)
logging.info("----------- Starte Alfred Modul - Ultraschall Sensoren {0} ---------------".format(Version))


#Variablen definieren
MAXDISTANCE = 15


#Pins definieren
US1 = 5,6 #Trigger,Echo
US2 = 13,19 #Trigger,Echo

GPIO.setmode(GPIO.BCM)
GPIO.setup(US1[0],GPIO.OUT) #Trigger
GPIO.setup(US1[1],GPIO.IN)  #Echo
GPIO.setup(US2[0],GPIO.OUT) #Trigger
GPIO.setup(US2[1],GPIO.IN)  #Echo

#Funktion zur durchfuehrung der Messung
def distance(GPIO_TRIGGER,GPIO_ECHO):
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance  
    logging.debug("Trigger: {0}   Echo: {1}  - Distance gemessen: {2}".format(GPIO_TRIGGER,GPIO_ECHO,distance))

        
#Funktion zum Auslesen
def get(Ultrasonic):

    if Ultrasonic == 1:
        DistanceOut = distance(US1[0],US1[1])
    elif Ultrasonic == 2:
        DistanceOut = distance(US2[0],US2[1])
    
    DistanceOut = int(DistanceOut)
    return(DistanceOut)
    logging.debug("Rueckgabewert Sensor {0} : {1}".format(Ultrasonic,DistanceOut))

def wall(cap=MAXDISTANCE):
    if cap > distance(US1[0],US1[1]) or cap > distance(US2[0],US2[1]):
        return True
    else:
        return False

