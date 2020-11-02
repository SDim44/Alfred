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


def send(add,cmd):
    # add = Address in Hex
    # cmd = Command in Hex

    from smbus import SMBus
    bus = SMBus(1)
    print(type(add))
    print(type(cmd))
    add = int(add,16)
    add = hex(add)
    cmd = hex(cmd)
    print(add)
    print(cmd)
    bus.write_byte(add, cmd)
    
    feedback = True
    
    return feedback