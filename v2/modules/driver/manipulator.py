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
  
def i2c(slave_address,command):
    from smbus import SMBus
    bus = SMBus(1)
    byteValue = []

    for c in command:
        byteValue.append(ord(c))

    bus.write_i2c_block_data(slave_address,0x00,byteValue)