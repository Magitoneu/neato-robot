from Laser_code import NeatoLaser
import time

#TODO s'ha de probar on es el valor d'angle 0 real
# laser[0] outerleft
# laser[1] centerleft
# laser[2] center
# laser[3] centerright
# laser[4] outerright

class NeatoRobot:
	north = 0
	distance = 400
	speed = 120
	direction = 0 #0 fordward, 1 backward
	theta = 0
	tiempo = 20
	S = 121.5
	
	#Just move without crash
	def random_path(self, values, laser):
		if values[0] < 650 :
			self.theta = self.theta+3.141516/2
		elif (values[1] < self.distance) or (values[9] < self.distance):
			if(values[1] < self.distance):
				self.theta = self.theta+3.141516/3
			else:
				self.theta = self.theta-3.141516/3
		elif (values[8] < self.distance) or (values[2] < self.distance):
			if(values[8] < self.distance):
				self.theta = self.theta-3.141516/4
			else:
				self.theta = self.theta+3.141516/4
		else:
			self.theta = 0
		distancia_R = (((self.speed * pow(-1, self.direction) ) + (self.S * self.theta)) * self.tiempo) * pow(-1, self.direction)
		distancia_L = (((self.speed * pow(-1, self.direction) ) + (-self.S * self.theta)) * self.tiempo) * pow(-1, self.direction)
		laser.enviaL("SetMotor LWheelEnable RWheelEnable", "go", 0.1)
		comando = 'SetMotor LWheelDist ' + str(distancia_L) + ' RWheelDist ' + str(distancia_R) + ' Speed ' + str(self.speed * pow(-1, self.direction))
		print(comando)
		laser.enviaL(comando, 'command L R', 0.1)
		
	#Per a seguir un cami recte fa falta memoria (on es el nord per exemple)
	#FER AMB ODOMETRIA
	def straight_path(self, values, laser):
		print("NORTH: ", self.north)
		if values[0] < 650 :
			self.theta = self.theta+3.141516/2
		elif (values[1] < self.distance) or (values[9] < self.distance):
			if(values[1] < self.distance):
				self.theta = self.theta+3.141516/3
			else:
				self.theta = self.theta-3.141516/3
		elif (values[8] < self.distance) or (values[2] < self.distance):
			if(values[8] < self.distance):
				self.theta = self.theta-3.141516/4
			else:
				self.theta = self.theta+3.141516/4
		else:
			self.theta = -self.north
		print("THETA: ", self.theta)
		distancia_R = (((self.speed * pow(-1, self.direction) ) + (self.S * self.theta)) * self.tiempo) * pow(-1, self.direction)
		distancia_L = (((self.speed * pow(-1, self.direction) ) + (-self.S * self.theta)) * self.tiempo) * pow(-1, self.direction)
		laser.enviaL("SetMotor LWheelEnable RWheelEnable", "stop", 0.2)
		comando = 'SetMotor LWheelDist ' + str(distancia_L) + ' RWheelDist ' + str(distancia_R) + ' Speed ' + str(self.speed * pow(-1, self.direction))
		laser.enviaL(comando, 'command L R', 0.1)
		if(self.north != 0):
			print(comando)
		self.north = self.north + self.theta
	

if __name__ == "__main__":
	laser = NeatoLaser()
	laser.enable_laser(True)
	time.sleep(1)
	k = 0
	robot = NeatoRobot()
	try:
		while True:
			values = laser.get_laser()
			robot.straight_path(values, laser)
			#print("Laser values: ",values)
			#time.sleep(0.1)
			k = k + 1
	except KeyboardInterrupt:
		laser.enviaL("SetMotor LWheelDisable RWheelDisable", "stop", 0.2)
	laser.enable_laser(False)
