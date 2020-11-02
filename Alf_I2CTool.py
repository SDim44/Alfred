#       I2C Tool Connect
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


#Import Libraries
fromo smbus import SMBus

bus = SMBus(1)

def send(add,cmd):
    # add = Address in Hex
    # cmd = Command in Hex
    try:
        bus.write_byte(add, cmd)
        feedback = True
    except:
        feedback = False
    
    return feedback