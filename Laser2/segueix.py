from neatoRobot import NeatoRobot
from test_NeatoCommands import envia
import serial
import time
import sys

if __name__ == "__main__":
    ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=0.05)
    envia(ser, "SetMotor LWheelEnable RWheelEnable", 0.2)
    time.sleep(1)
    robot = NeatoRobot(ser)

    try:
        if(sys.argv[1] == "fuig"):
            robot.fuig_segueix(True)
        else:
            robot.fuig_segueix(False)
    except KeyboardInterrupt:
        robot.enviaR("SetMotor LWheelDisable RWheelDisable", 0.2)
        robot.enviaR('SetLDSRotation Off', 1)
        
    robot.enviaR('SetLDSRotation Off', 1)