#
#       Alfred Modul - Arduino Connector
#
#       Stefan Dimnik, 09.03.2020
#
#       Mit dieses Programm, kann mit dem Arduion kommuniziert werden
#
#       V1.0
#       Befehl wird ausgelesen tool.conf. Datei wird ueber php script geaendert. Mit dem Befehl do() wird der Inhalt der Datei an das Tool uebertagen. 
#
#       V2.0
#       Array mit maximal 10 Stellen wird direkt an Tool uebertragen.

#Libarys
import serial
import time
import logging


#Start Logging
Version = "V2.0"
logging.basicConfig(filename='/home/pi/Alfred/Logs/Alf_ToolConnect.log',level=logging.DEBUG ,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.debug("----------- Starte Alfred Modul - Tool Connector {0} ---------------".format(Version))

#Serielle Verbindung aufbauen
#ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
#ser.flush()



#Funktion - Tool Ansteuern - Hier kann eine Funktion am Arduino ausgefuehrt werden. Ein webrequest wird gesendet - num ist die Nummer der Funktion. (Nach diesem Befehl muss ein do() ausgefuehrt werden)
def set(command):
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        ser.flush()

        ser.write("{0}\n".format(command))
        logging.debug("command wurde gesendet: {0}".format(command))
    except:
        logging.debug("{0}\ncommand kann nicht gesendet werden (kein Tool erkannt)".format(command))


    


#Funktion - Tool Auslesen - Es wird die Zahl 99 and den Arduino gesendet, der Arduino sende daraufhin sein Spezifikationen. Diese werden hier ausgelesen und Zurueckgegeben.
def get():
    #Serielle Verbindung aufbauen
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        ser.flush()
        #Uebertragen
        i=0
        while i<3:
            line = ser.readline().decode('utf-8').rstrip()
            ser.write("99\n")
            i+=1 
        var1 = str(line)
        var2 = var1.strip('\n')
        var3 = var2.split('/')
    
    except serial.serialutil.SerialException:
        var3 = False
        
    return var3