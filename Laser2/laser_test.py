from Laser_code import NeatoLaser
from neatoRobot2 import NeatoRobot
from test_NeatoCommands import envia
import serial
import time

if __name__ == "__main__":
	ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=0.05)
	laser = NeatoLaser(ser)
	#laser.enable_laser(True)
	time.sleep(1)
	robot = NeatoRobot(ser)
	robot.enviaR("SetMotor LWheelEnable RWheelEnable", 0.2)
	#envia(ser, 'SetLDSRotation On', 4)
	k = 0
	b0 = False
	b1 = False
	b2 = False
	b3 = False
	try:
		while True:
			values = laser.get_laser()
			#print(values)
			if k == 0:
				robot.gotoWall(values, laser)
				time.sleep(0.5)
			b0,b1,b2,b3 = robot.followWal(values, laser, b0, b1, b2, b3)
			#robot.random_path(values, laser)
			#print("Laser values: ",values)
			time.sleep(0.35)
			k = k + 1
	except KeyboardInterrupt:
		robot.enviaR("SetMotor LWheelDisable RWheelDisable", 0.2)
	laser.enable_laser(False)