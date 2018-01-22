from test_NeatoCommands import envia
import serial
import time
import numpy as np

class NeatoLaser:
	angle_ini = 0
	step = 36
	
	def __init__(self):
		#self.laser_mutex = threading.Lock()
		self.ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=0.05)
		self.enviaL('TestMode On', "Testmode", 0.2)
		self.enviaL('PlaySound 1', "Play sound", 0.2)
		self.enviaL("SetMotor LWheelEnable RWheelEnable", "GO", 0.2)
		self.enviaL('SetLDSRotation On', 'z', 4)
		
	def enable_laser(self, b):
			""" Activates or deactivates the laser depending on whether the value of b is True or False. """
			if b == True:
				msg = self.enviaL('SetLDSRotation On',"Enable laser", 4)
			else:
				msg = self.enviaL('SetLDSRotation Off', "Disable Laser", 2)
			print msg
			
	def laser_row(self, v1, v2, v3, v4):
		#print("Angle: ", v1)
		#print("Dist:  ", v2)
		return v2
	def discretize(self):
		self.discrete_values = []
		self.laser_values = self.laser_values[341:359] + self.laser_values[0:340]
		for i in range(10):
			rang = list(map(float,self.laser_values[self.angle_ini + self.step*i:self.angle_ini + self.step*(i+1)]))
			vals = [float('Inf') if x == 0 else x for x in rang]
			self.discrete_values.append(min(vals))
			#print("Discrete: ", i)
			#print("Value:    ", self.discrete_values[i])
		
	def getError(self, value):
		print('GETTING ERROR: ', value)
		self.ser.write('GGetErr'+'\r'+'\n')
		while self.ser.inWaiting() > 0:
			print(self.ser.readline())
		
	def get_laser(self):
			""" Ask to the robot for the current values of the laser. """
			msg = self.enviaL('GetLDSScan', "GetLDSScan", 0.2)
			self.laser_values = []
			for line in msg.splitlines():	
				s = line.split(',')
				if (len(s) == 4 and s[0].isdigit()):
					#print('aka: ', s)
					lr = self.laser_row(s[0], s[1], s[2], s[3])
					self.laser_values.append(lr)
			#print(self.laser_values)
			
			self.discretize()
			#self.laser_mutex.release()
			return self.discrete_values
	def enviaL(self, msg, text, t):
		print(text)
		buffer = envia(self.ser, msg, t)
		return buffer
