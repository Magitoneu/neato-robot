from test_NeatoCommands import envia
from Laser_code import NeatoLaser
from neatoRobot import NeatoRobot
import time
import math
#Ranges:
#	FRONTAL
#0 - Front
#1 - Center left ?
#9 - Center right ? 
#2 - Outer left 
#8 - Outer right
#   BACK
#5 - Back
#6 - Central right
#4 - Central left
#3 - Outer left
#7 - Outer right
#sumar a theta es girar a l'esquerre
if __name__ == "__main__":
	ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=0.05)
	laser = NeatoLaser(ser)
	laser.enable_laser(True)
	time.sleep(1)
	robot = NeatoRobot(ser)
	envia("SetMotor LWheelEnable RWheelEnable", "go", 0.1)
	try:
		while True:
			values = laser.get_laser()
			robot.random_path(values, laser)
	except KeyboardInterrupt:
		envia(ser, "SetMotor LWheelDisable RWheelDisable", 0.2)
	laser.enable_laser(False)
