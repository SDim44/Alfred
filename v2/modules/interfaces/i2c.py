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


#Import Libraries


def send(add,cmd):
    # add = Address in Hex
    # cmd = Command in Hex

    from smbus import SMBus
    bus = SMBus(1)
    cmd = ("0x"+str(cmd))

    add = int(add,16)
    cmd = int(cmd,16)

    add = hex(add)
    cmd = hex(cmd)

    add = int(add,16)
    cmd = int(cmd,16)
    
    bus.write_byte(add, cmd)
    
    #feedback = bus.read_byte_data(add,0)
    
    #return feedback

def send_safe(add,cmd):

    from smbus import SMBus
    bus = SMBus(1)
    temp = None

    i2cData = False
    while True:
        i2cData = not i2cData
        send(add,cmd)

        temp = bus.read_byte(add)
        print(value)
        time.sleep(1)
        if temp == None:
            continue
        else:
            break
    
    return temp