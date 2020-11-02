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
    int(add) = add
    int(cmd) = cmd
    print(add)
    print(cmd)
    add = hex(add)
    cmd = hex(cmd)
    print(add)
    print(cmd)
    bus.write_byte(add, cmd)
    
    feedback = True
    
    return feedback