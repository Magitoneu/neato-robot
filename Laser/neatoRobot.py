from test_NeatoCommands import envia
import time
import math

class NeatoRobot:
	north = 0
	distance = 400
	speed = 120
	direction = 0 #0 fordward, 1 backward
	theta = 0
	tiempo = 20
	S = 121.5
	# initial position = [0 0] ?
	# position = [0 0]
	# angle = 0
    
    def __init__(self, ser):
		#self.laser_mutex = threading.Lock()
		self.ser = ser
		envia(self.ser, 'TestMode On', 0.2)
		envia(self.ser, 'PlaySound 1', 0.2)
		envia(self.ser, "SetMotor LWheelEnable RWheelEnable", 0.2)

	#Just move without crash
	def random_path(self, values, laser):
		if values[0] < 650:
			auxvals = [values[1] + values[2], values[8] + values[9]]
			idx = auxvals.index(max(auxvals)) #Agafar el valor màxim
			if idx == 0:  #Girar a l'esquerre
				self.theta = self.theta+3.141516/2
			else:
				self.theta = self.theta-3.141516/2
		elif (values[1] < self.distance) or (values[9] < self.distance):
			if (values[1] < self.distance) and (values[9] < self.distance):
				if values[9] < values[1]:
					self.theta = self.theta+3.141516/4
				else:
					self.theta = self.theta-3.141516/4				
			elif(values[1] < self.distance):
				self.theta = self.theta-3.141516/3
			else:
				self.theta = self.theta+3.141516/3
		elif (values[8] < self.distance) or (values[2] < self.distance):
			if (values[8] < self.distance) and (values[2] < self.distance):
				if values[8] < values[2]:
					self.theta = self.theta+3.141516/4
				else:
					self.theta = self.theta-3.141516/4
			elif(values[8] < self.distance):
				self.theta = self.theta+3.141516/4
			else:
				self.theta = self.theta-3.141516/4
		else:
			self.theta = 0
		#print("Front: ", values[0], " OuterLeft: ", values[2], " OuterRight: ", values[8], " CenterLeft: ", values[1], " CenterRight: ", values[9])
		#print("Theta: ", self.theta)
		distancia_R = (((self.speed * pow(-1, self.direction) ) + (self.S * self.theta)) * self.tiempo) * pow(-1, self.direction)
		distancia_L = (((self.speed * pow(-1, self.direction) ) + (-self.S * self.theta)) * self.tiempo) * pow(-1, self.direction)
		comando = 'SetMotor LWheelDist ' + str(distancia_L) + ' RWheelDist ' + str(distancia_R) + ' Speed ' + str(self.speed * pow(-1, self.direction))
		#print(comando)
		envia(self.ser, comando, 0.1)
		
	#Per a seguir un cami recte fa falta memoria (on es el nord per exemple)
	#FER AMB ODOMETRIA
	def straight_path(self, values, laser):
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
		comando = 'SetMotor LWheelDist ' + str(distancia_L) + ' RWheelDist ' + str(distancia_R) + ' Speed ' + str(self.speed * pow(-1, self.direction))
		envia(self.ser, comando, 0.1)
		if(self.north != 0):
			print(comando)
		self.north = self.north + self.theta
	
	def reachPoint(self, goal, laser):
		vector = goal - position
		d = math.sqrt(math.pow(vector[0],2) + math.pow(vector[1],2))
		a = math.atan2(vector[1], vector[2])
		dif = __angleDiff(a, angle)
		#Sha daconseguir desplasarse d amb un angle de dif, millor que no sigui tot recte (buscar la parabola)

	def followWall(self, values, laser):
		#Es podria fer un while apart fins que troba una paret
		#Putse dreta esquerre esta malament en els values i en l'angle a girar || Reduir velocitats?
		if values[0] < 650:
			self.theta = self.theta + 3.141516/2
		elif values[2] < 400:  #Aprop de la paret
			self.theta = self.theta + 3.141516/3
		elif values[2] > 1000: #A tuma pel cul de la paret
			self.theta = self.theta - 3.141516/2
		elif values[2] > 500: #Lluny de la paret
			self.theta = self.theta - 3.141516/3
		else: 
			self.theta = self.theta
		distancia_R = (((self.speed * pow(-1, self.direction) ) + (self.S * self.theta)) * self.tiempo) * pow(-1, self.direction)
		distancia_L = (((self.speed * pow(-1, self.direction) ) + (-self.S * self.theta)) * self.tiempo) * pow(-1, self.direction)
		comando = 'SetMotor LWheelDist ' + str(distancia_L) + ' RWheelDist ' + str(distancia_R) + ' Speed ' + str(self.speed * pow(-1, self.direction))
		envia(self.ser, comando, 0.1)
    
    def __angleDiff(b1, b2):
	r = (b2 - b1) % 360.0
	if r >= 180.0:
		r -= 360.0
	return r