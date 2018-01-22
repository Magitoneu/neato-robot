from Laser_code import NeatoLaser
from neatoRobot import NeatoRobot
import serial
import time

if __name__ == "__main__":
	ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=0.05)
	laser = NeatoLaser(ser)
	laser.enable_laser(True)
	time.sleep(1)
	robot = NeatoRobot(ser)
	robot.enviaR("SetMotor LWheelEnable RWheelEnable", 0.2)
	envia(self.ser, 'SetLDSRotation On', 'z', 4)
	k = 0
	try:
		while True:
			values = laser.get_laser()
			if k == 0:
				robot.gotoWall(values, laser)
			robot.followWal(values, laser)
			#robot.random_path(values, laser)
			#print("Laser values: ",values)
			time.sleep(2)
			k = k + 1
	except KeyboardInterrupt:
		robot.enviaR("SetMotor LWheelDisable RWheelDisable", 0.2)
	laser.enable_laser(False)
