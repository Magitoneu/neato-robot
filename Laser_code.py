from test_NeatoCommands import envia
import serial
import time

class NeatoLaser:
	angle_ini = 0
	step = 36
	
	def __init__(self):
		#self.laser_mutex = threading.Lock()
		self.ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=0.05)
		self.__envia('TestMode On', "Testmode")
		self.__envia('PlaySound 1', "Play sound")
		
	def enable_laser(self, b):
			""" Activates or deactivates the laser depending on whether the value of b is True or False. """
			msg = ''

			if b == True:
				msg = self.__envia('SetLDSRotation On',"Enable laser")
			else:
				msg = self.__envia('SetLDSRotation Off', "Disable Laser")
			print msg
			
	def laser_row(self, v1, v2, v3, v4):
		print("Angle: ", v1)
		print("Dist:  ", v2)
		return v2
	def discretize(self):
		self.discrete_values = []
		for i in range(5):
			self.discrete_values.append(min(self.laser_values[self.angle_ini + self.step*i:self.angle_ini + self.step*(i+1)]))
			print("Discrete: ", i)
			print("Value:    ", self.discrete_values[i])
		
	def getError(self, value):
		print('GETTING ERROR: ', value)
		self.ser.write('GGetErr'+'\r'+'\n')
		while self.ser.inWaiting() > 0:
			print(self.ser.readline())
		
	def get_laser(self):
			""" Ask to the robot for the current values of the laser. """
			msg = self.__envia('GetLDSScan', "GetLDSScan")
			self.laser_values = []
			for line in msg.splitlines():	
				s = line.split(',')
				if (len(s) == 4 and s[0].isdigit()):
					print('aka: ', s)
					lr = self.laser_row(s[0], s[1], s[2], s[3])
					self.laser_values.append(lr)
			print(self.laser_values)
			
			self.discretize()
			#self.laser_mutex.release()
			return self.discrete_values
	def __envia(self, msg, text):
		print(text)
		buffer = envia(self.ser, msg)
		return buffer
