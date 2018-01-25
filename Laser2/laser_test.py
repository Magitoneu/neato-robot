from Laser_code import NeatoLaser
from neatoRobot import NeatoRobot
from test_NeatoCommands import envia
import serial
import time
import sys

#TODO: exit maze, canvairel, seguir sempre paret, fins que podem anar al punt directament

if __name__ == "__main__":
	ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=0.05)
	time.sleep(1)
	robot = NeatoRobot(ser)
	robot.enviaR("SetMotor LWheelEnable RWheelEnable", 0.2)
	try:
		if sys.argv[1] == "Goto":
			robot.Goto(int(sys.argv[2]), int(sys.argv[3]))
		elif sys.argv[1] == "GotoObstacles":
			robot.GotoObstacles(int(sys.argv[2]), int(sys.argv[3]))
		elif sys.argv[1] == "Avoid":
			robot.random_path()
		elif sys.argv[1] == "FollowWall":
			robot.followWal(True)
		elif sys.argv[1] == "ExitMaze":
			print("Exit maze")
			robot.exitMaze(int(sys.argv[2]), int(sys.argv[3]))
		elif sys.argv[1] == "Predator":
			robot.fuig_segueix(False)
		elif sys.argv[1] == "Prey":
			robot.fuig_segueix(True)
		else:
			print("Name error")

	except KeyboardInterrupt:
		robot.enviaR("SetMotor LWheelDisable RWheelDisable", 0.2)
		robot.enviaR("SetLDSRotation Off", 1)