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

    def __init__(self, ser):
        self.ser = ser
        envia('TestMode On', 0.2)
		envia('PlaySound 1', 0.2)
		envia("SetMotor LWheelEnable RWheelEnable", 0.2)

    #Just move without crash
    def random_path(self, values, laser):
        #print(values)
        if values[0] < 650:
            auxvals = [values[1] + values[2], values[8] + values[9]]
            idx = auxvals.index(max(auxvals)) #Agafar el valor maxim
            if idx == 0:  #Girar a l'esquerre
                self.theta = self.theta+3.141516/4
                print("Turn left")
            else:
                self.theta = self.theta-3.141516/4
                print("Turn right")
        elif (values[1] < self.distance) or (values[9] < self.distance):
            if (values[1] < self.distance) and (values[9] < self.distance):
                if values[9] < values[1]:
                    self.theta = self.theta+3.141516/5
                    print("Turn left")
                else:
                    self.theta = self.theta-3.141516/5
                    print("Turn right")				
            elif(values[1] < self.distance):
                self.theta = self.theta-3.141516/5
                print("Turn right")
            else:
                self.theta = self.theta+3.141516/5
        elif (values[8] < self.distance) or (values[2] < self.distance):
            if (values[8] < self.distance) and (values[2] < self.distance):
                if values[8] < values[2]:
                    self.theta = self.theta+3.141516/6
                    print("Turn left")
                else:
                    self.theta = self.theta-3.141516/6
                    print("Turn right")
            elif(values[8] < self.distance):
                self.theta = self.theta+3.141516/6
                print("Turn left")
            else:
                self.theta = self.theta-3.141516/6
                print("Turn right")
        else:
            self.theta = 0
        print("Front: ", values[0], " OuterLeft: ", values[2], " OuterRight: ", values[8], " CenterLeft: ", values[1], " CenterRight: ", values[9])
        print("Theta: ", self.theta)
        distancia_R = (((self.speed * pow(-1, self.direction) ) + (self.S * self.theta)) * self.tiempo) * pow(-1, self.direction)
        distancia_L = (((self.speed * pow(-1, self.direction) ) + (-self.S * self.theta)) * self.tiempo) * pow(-1, self.direction)
        comando = 'SetMotor LWheelDist ' + str(distancia_L) + ' RWheelDist ' + str(distancia_R) + ' Speed ' + str(self.speed * pow(-1, self.direction))
        #print(comando)
        self.enviaR(comando, 0.1)
                
    def followWal(self, values, laser):
        print("front: ", values[0])
        print("right: ", values[8])
        if values[0] < 500:
            self.theta = self.theta + 3.141516/3
            print("turn left")
        elif values[8] > 400:
            self.theta = self.theta - 3.141516/6
            print("turn right")
        elif values[8] > 650:
            self.theta = self.theta - 3.141516/3
            print("turn right")
        elif values[8] < 300:
            self.theta = self.theta + 3.141516/6
            print("turn left")
        else:
            self.theta = 0
        distancia_R = (((self.speed * pow(-1, self.direction) ) + (self.S * self.theta)) * self.tiempo) * pow(-1, self.direction)
        distancia_L = (((self.speed * pow(-1, self.direction) ) + (-self.S * self.theta)) * self.tiempo) * pow(-1, self.direction)
        comando = 'SetMotor LWheelDist ' + str(distancia_L) + ' RWheelDist ' + str(distancia_R) + ' Speed ' + str(self.speed * pow(-1, self.direction))
        self.enviaR(comando, 0.1)

    def gotoWall(self, values, laser):
        while(values[0] > 650):
            self.theta = 0
            distancia_R = (((self.speed * pow(-1, self.direction) ) + (self.S * self.theta)) * self.tiempo) * pow(-1, self.direction)
            distancia_L = (((self.speed * pow(-1, self.direction) ) + (-self.S * self.theta)) * self.tiempo) * pow(-1, self.direction)
            comando = 'SetMotor LWheelDist ' + str(distancia_L) + ' RWheelDist ' + str(distancia_R) + ' Speed ' + str(self.speed * pow(-1, self.direction))
            self.enviaR(comando, 0.1)
            values = laser.get_laser()
        print("Wall reached")
        values = laser.get_laser()
        self.theta = self.theta + 3.141516/2
        distancia_R = (((self.speed * pow(-1, self.direction) ) + (self.S * self.theta)) * self.tiempo) * pow(-1, self.direction)
        distancia_L = (((self.speed * pow(-1, self.direction) ) + (-self.S * self.theta)) * self.tiempo) * pow(-1, self.direction)
        comando = 'SetMotor LWheelDist ' + str(distancia_L) + ' RWheelDist ' + str(distancia_R) + ' Speed ' + str(self.speed * pow(-1, self.direction))
        self.enviaR(comando, 0.1)

    def enviaR(self, msg, t):
        buffer = envia(self.ser, msg, t)
        return buffer