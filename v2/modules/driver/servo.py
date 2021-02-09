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
supported_commands = ["scale.0-40"]

def i2c(slave_address,command):
    from ..interfaces import i2c

    i2c.send(slave_address,command)

def i2c_ack(slave_address,command):
    from ..interfaces import i2c

    i2c.send_safe(slave_address,command)
    

def serial(serial_port,baudrate,command):
    from ..interfaces import serial
    serial.send(port,baud,command)



def mqtt(mac_address,command):
    #Post Number in device path
    pass