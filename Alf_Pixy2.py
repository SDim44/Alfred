#
#       Alfred Modul - Pixy Cam 2
#
#       Stefan Dimnik, 14.03.2020
#
#       Dieses Programm uebernimmt die Steuerung der Roboter-Platform.


#--------------------------------------------------------------------------------
#Libarys einbinden
from __future__ import print_function
import pixy 
from ctypes import *
from pixy import *
import RPi.GPIO as GPIO
import time
import logging

#GPIO Warnungen deaktivieren
GPIO.setwarnings(False)

#Logging starten
Version = "V1.0"
logfile = 'logs/Alf_Main.log'
logging.basicConfig(filename=logfile,level=logging.DEBUG ,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.FileHandler(logfile, mode="w", encoding=None, delay=False)
logging.info("----------- Starte Alfred Modul - Pixy Cam 2 {0} ---------------".format(Version))


#Programm start
pixy.init ()
#pixy.change_prog ("color_connected_components") /-> Speicherzugriffsfehler

class Blocks (Structure):
  _fields_ = [ ("m_signature", c_uint),
    ("m_x", c_uint),
    ("m_y", c_uint),
    ("m_width", c_uint),
    ("m_height", c_uint),
    ("m_angle", c_uint),
    ("m_index", c_uint),
    ("m_age", c_uint) ]


def get(Signatur):
    blocks = BlockArray(100)
    frame = 0
    signal = 0,0
    signal1 = 0,0
    signal2 = 0,0

    count = pixy.ccc_get_blocks (100, blocks)
    
    if count > 0:
    
        frame = frame + 1
        for index in range (0, count):
            logging.debug('[BLOCK: SIG=%d X=%3d Y=%3d WIDTH=%3d HEIGHT=%3d]' % (blocks[index].m_signature, blocks[index].m_x, blocks[index].m_y, blocks[index].m_width, blocks[index].m_height))
            signal = (blocks[index].m_signature,blocks[index].m_x,blocks[index].m_y, blocks[index].m_width, blocks[index].m_height)
            
        if signal[0] == 1 or signal[0] == 0:
            signal1 = signal
        if signal[0] == 2 or signal[0] == 0:
            signal2 = signal
        

    if Signatur == 1:
        return(signal1)
        
    elif Signatur == 2:
        return(signal2)

        