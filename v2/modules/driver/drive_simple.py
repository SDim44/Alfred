#       Motor Driver simple
#
#       Autor:              Stefan Dimnik
#       Date:               04.11.2020
#       Python:             3.7
#       Projekt Details:    https://github.com/SDim44/Alfred
#       ------------------------------------------------------------
#       
#       V0.1
#       Control a 2 Wheel drive without speed configuration
#       ------------------------------------------------------------


supported_protocol = ["i2c","serial"]
supported_commands = ["stop","forward","turn_left","turn_right"]

def i2c(slave_address,command):
    from ..interfaces import i2c

    if command == "stop":
        print("stop")
        feedback = i2c.send(slave_address,0)
    elif command == "forward":
        print("forward")
        feedback = i2c.send(slave_address,1)
    elif command == "turn_left":
        print("turn_left")
        feedback = i2c.send(slave_address,2)
    elif command == "turn_right":
        print("turn_right")
        feedback = i2c.send(slave_address,3)

    return feedback

def serial(serial_port,baudrate):
    from ..interfaces import serial

    if command == "stop":
        serial.send(port,baud,0)
    elif command == "forward":
        serial.send(port,baud,1)
    elif command == "turn_left":
        serial.send(port,baud,2)
    elif command == "turn_right":
        serial.send(port,baud,3)