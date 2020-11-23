#       I2C Interface
#
#       Autor:              Stefan Dimnik
#       Date:               02.11.2020
#       Python:             3.7
#       Projekt Details:    https://github.com/SDim44/Alfred
#       ------------------------------------------------------------
#       
#       V0.1
#       Communication Module for I2C-Bus
#       ------------------------------------------------------------

#Libarys
import serial
import time

#------------------------------------------------------------------------------------------------- 
#Send Data

def send(port='/dev/ttyACM0',baud,cmd):

    ser = serial.Serial(port, baud, timeout=1)
    ser.flush()
    ser.write("{0}\n".format(cmd))


#------------------------------------------------------------------------------------------------- 
#Recieve Data while "\n"
def recieve(port='/dev/ttyACM0',baud,cmd):
    #Serielle Verbindung aufbauen
    try:
        ser = serial.Serial(port, baud, timeout=1)
        ser.flush()

        i=0
        while i<3:
            line = ser.readline().decode('utf-8').rstrip()
            ser.write("cmd\n")
            i+=1 
        var1 = str(line)
        var2 = var1.strip('\n')
        var3 = var2.split('/')
    
    except serial.serialutil.SerialException:
        var3 = False
        
    return var3