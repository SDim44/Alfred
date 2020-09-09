#
#       Alfred Verfolgung
#
#       Stefan Dimnik, 09.03.2020
#
#       V0.1
#       Dieses Programm uebernimmt die Motorsteuerung mit PixyCam2 und Ultraschallsensoren.


#Libarys
import time
import logging
import RPi.GPIO as GPIO
import Alf_Motor as engin
import Alf_Ultraschall as distance
import cvision as cv

#GPIO Warnungen deaktivieren
GPIO.setwarnings(False)

#Logging config
Version = "V1.0"
#logfile = 'logs/Alf_Verfolgung_CV.log'
#logging.basicConfig(filename=logfile,level=logging.DEBUG ,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
#logging.FileHandler(logfile, mode="w", encoding=None, delay=False)
logging.info("----------- Starte Alfred Modul - Verfolgung {0} ---------------".format(Version))

#Variablen definieren
MAXAREA     =   10000 # Maximale groesse des Objekts
MINAREA     =   5000 # Minimale groesse des Objekts


def driving(sig):  
    if  sig[0] > 0:
        xobj = (100 / 157.5) * sig[1] - 100    # Motor Geschwindigkeit berechnen
        area = sig[3] * sig[4]
        glob_area = area
        logging.debug("\n\n\tObjektgroesse: {0}".format(glob_area))
        
        if area < MINAREA and area > 0:               # Forwaerts fahren wenn Objekt zu klein ist
        
            if xobj < 0:                           #Kurve nach rechts wenn x Position > 40
                xobj = -xobj
                l_rot_speed = 100 - xobj
                engin.move(1,1,l_rot_speed,100)
                logging.debug("LINKS -> L Motor: {0}".format(l_rot_speed))
        
            elif xobj > 0:                   #Kurve nach rechts wenn x Position > 40
                r_rot_speed = 100 - xobj
                engin.move(1,1,100,r_rot_speed)
                logging.debug("RECHTS -> R Motor: {0}".format(r_rot_speed))
        
            else:
                logging.debug("VORWAERTS")
                engin.move(1,1,100,100)
        
        elif area > MAXAREA:                #Rueckwaerts fahren wenn das Objekt zu gross ist.
            engin.move(0,0,0,0)
            logging.debug("STOP\n")
    
        
        else:                                    # Stoppen, wenn sich das Objekt im Bereich "area" befindet.
        
            engin.move(0,0,0,0)
            logging.debug("STOP\n")
        
    
    else:                                      # Stoppen, wenn die Signatur 1 nicht erkannt wird.
        engin.move(1,2,50,50)
        logging.debug("DREHEN --> Nach Signal suchen\n")


def hunt(Mode):
    sig1 = pixy.get(1)
    sig2 = pixy.get(2)
    
    if Mode == 1:
        driving(sig1)
        logging.debug("Signatur 1 wird verfolgt : {}".format(sig1))
    
    elif Mode == 2:
        driving(sig2)
        logging.debug("Signatur 2 wird verfolgt : {}".format(sig2))


  