#       Servo Control
#
#       Autor:              Stefan Dimnik
#       Date:               04.11.2020
#       Python:             3.7
#       Projekt Details:    https://github.com/SDim44/Alfred
#       ------------------------------------------------------------
#       
#       V0.1
#       Control Servo Motor
#       ------------------------------------------------------------



supported_protocol = ["mqtt","i2c","serial"]
supported_commands = ["set.1000 - 6180"]
  
def writeData(value):
    from smbus import SMBus
    bus = SMBus(1)
    byteValue = StringToBytes(value)    
    bus.write_i2c_block_data(address,0x00,byteValue) #first byte is 0=command byte.. just is.
    return -1

def StringToBytes(val):
        retVal = []
        for c in val:
            retVal.append(ord(c))
        return retVal

def i2c(slave_address,command):

    while True:
        print("sending")
        writeData(command)   
        time.sleep(5)