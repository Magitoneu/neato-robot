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
	distance = 20
	speed = 150
	direction = 0 #0 fordward, 1 backward
	tita_dot = 0
	tiempo = 20
	
	#Just move without crash
	def random_path(self, values):
		if values[0] > self.distance :
			tita_dot = 3.141516/4
		elif values[1] > self.distance:
			tita_dot = 3.141516/3
		elif values[2] > self.distance:
			tita_dot = 3.141516/2
		elif values[3] > self.distance:
			tita_dot = -3.141516/3
		elif values[4] > self.distance:
			tita_dot = -3.141516/4
		else:
			self.tita_dot = 0
		#distancia_R = (((speed * pow(-1, direccion) ) + (S * tita_dot)) * tiempo) * pow(-1, direccion)
		#distancia_L = (((speed * pow(-1, direccion) ) + (-S * tita_dot)) * tiempo) * pow(-1, direccion)
		
		
	#Per a seguir un cami recte fa falta memoria (on es el nord per exemple)
	def straight_path(self, values):
		if values[0] > self.distance :
			tita_dot = 3.141516/4
		elif values[1] > self.distance:
			tita_dot = 3.141516/3
		elif values[2] > self.distance:
			tita_dot = 3.141516/2
		elif values[3] > self.distance:
			tita_dot = -3.141516/3
		elif values[4] > self.distance:
			tita_dot = -3.141516/4
		else:
			self.tita_dot = self.north
		#distancia_R = (((speed * pow(-1, direccion) ) + (S * tita_dot)) * tiempo) * pow(-1, direccion)
		#distancia_L = (((speed * pow(-1, direccion) ) + (-S * tita_dot)) * tiempo) * pow(-1, direccion)
		self.noth = self.north + self.tita_dot
	

if __name__ == "__main__":
	laser = NeatoLaser()
	laser.enable_laser(True)
	time.sleep(1)
	k = 0
	robot = NeatoRobot()
	while k < 2:
		values = laser.get_laser()
		robot.random_path(values)
		print("Laser values: ",values)
		time.sleep(1)
		k = k + 1
