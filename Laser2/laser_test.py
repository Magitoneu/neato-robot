from Laser_code import NeatoLaser
from neatoRobot import NeatoRobot
from test_NeatoCommands import envia
import serial
import time

if __name__ == "__main__":
	ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=0.05)
	time.sleep(1)
	robot = NeatoRobot(ser)
	robot.enviaR("SetMotor LWheelEnable RWheelEnable", 0.2)
	#envia(ser, 'SetLDSRotation On', 4)
	k = 0
	try:	
		robot.GotoObstacles(3500,0)
	except KeyboardInterrupt:
		robot.enviaR("SetMotor LWheelDisable RWheelDisable", 0.2)
		robot.enviaR("SetLDSRotation Off", 1)