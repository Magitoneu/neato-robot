from test_NeatoCommands import envia
from neatoOdometry import NeatoOdometry
from Laser_code import NeatoLaser
from multiprocessing import Process, Queue
import threading
import time
import math

class NeatoRobot:
    north = 0
    distance = 430
    speed = 120
    direction = 0 #0 fordward, 1 backward
    theta = 0
    tiempo = 20
    S = 121.5

    def __init__(self, ser):
        self.ser = ser
        envia(self.ser, 'TestMode On', 0.2)
        envia(self.ser, 'PlaySound 1', 0.2)
        envia(self.ser, "SetMotor LWheelEnable RWheelEnable", 0.2)
        #envia(self.ser, 'SetLDSRotation On', 2)
        self.laser = NeatoLaser(ser)
        
        self.pose_queue = Queue()
        self.laser_queue = Queue()
        
        self.viewer = http_viewer.HttpViewer(8000, self.pose_queue, self.laser_queue)
        
        L_read, R_read = self.__get_motors()
        self.odometry = NeatoOdometry(L_read, R_read)
        
    def __odometry_queue(self):
        current_odometry = self.odometry.getTheoricPose()
        self.pose_queue.put([(current_odometry[0][0], current_odometry[1][0])])
        
    def Goto(self, x, y):
        print("Going to point")
        L, R = self.odometry.getGoToPoint(x, y)
        
        while (L+R) > 0:
            comando = 'SetMotor LWheelDist ' + str(L) + ' RWheelDist ' + str(R) + ' Speed ' + str(self.speed)
            self.enviaR(comando, 0.1)
            L_read, R_read = self.__get_motors()
            self.odometry.updateOdometry(L_read, R_read)
            L, R = self.odometry.getGoToPoint(x, y)
            
        comando = 'SetMotor LWheelDist 0 RWheelDist 0 Speed 0'
        self.enviaR(comando, 0.1)
        
    def GotoObstacles(self, x, y):
        print("Going to point without crashing")
        L, R = self.odometry.getGoToPoint(x, y)
        
        while ((L+R) > 0):
            if not self.__esquiva():
                comando = 'SetMotor LWheelDist ' + str(L) + ' RWheelDist ' + str(R) + ' Speed ' + str(self.speed)
                self.enviaR(comando, 0.1)
                print("Commands ODOMETRY")
            else:
                print("ESQUIVA")

            L_read, R_read = self.__get_motors()
            self.odometry.updateOdometry(L_read, R_read)
            L, R = self.odometry.getGoToPoint(x, y)
            
        comando = 'SetMotor LWheelDist 0 RWheelDist 0 Speed 0'
        self.enviaR(comando, 0.1)   
     
    def __get_motors(self):
        msg = self.enviaR('GetMotors LeftWheel RightWheel', 0.1).split('\n')
                
        L = int(msg[4].split(',')[1])
        R = int(msg[8].split(',')[1])
        
        return (L, R)
        
        #Just move without crash
    def __esquiva(self):
        dist_28 = 300
        #print(values)
        values = self.laser.get_laser()
        if values[0] < 620:
            auxvals = [values[1] + values[2], values[8] + values[9]]
            idx = auxvals.index(max(auxvals)) #Agafar el valor maxim
            if idx == 0:  #Girar a l'esquerre
                self.theta = +3.141516/4.5
                print("Turn left")
            else:
                self.theta = -3.141516/4.5
                print("Turn right")
            esq = True
        elif (values[1] < self.distance) or (values[9] < self.distance):
            if (values[1] < self.distance) and (values[9] < self.distance):
                if values[9] < values[1]:
                    self.theta = +3.141516/8
                    print("Turn left")
                else:
                    self.theta = -3.141516/8
                    print("Turn right")                
            elif(values[1] < self.distance):
                self.theta = -3.141516/8
                print("Turn right")
            else:
                self.theta = +3.141516/8
            esq = True
        elif (values[8] < dist_28) or (values[2] < dist_28):
            if (values[8] < dist_28) and (values[2] < dist_28):
                if values[8] < values[2]:
                    self.theta = +3.141516/10
                    print("Turn left")
                else:
                    self.theta = -3.141516/10
                    print("Turn right")
            elif(values[8] < dist_28):
                self.theta = +3.141516/10
                print("Turn left")
            else:
                self.theta = -3.141516/10
                print("Turn right")
            esq = True
        else:
            self.theta = 0
            esq = False
        print("Front: ", values[0], " OuterLeft: ", values[2], " OuterRight: ", values[8], " CenterLeft: ", values[1], " CenterRight: ", values[9])
        print("Theta: ", self.theta)
        if(esq):
            distancia_R = (((self.speed * pow(-1, self.direction) ) + (self.S * self.theta)) * self.tiempo) * pow(-1, self.direction)
            distancia_L = (((self.speed * pow(-1, self.direction) ) + (-self.S * self.theta)) * self.tiempo) * pow(-1, self.direction)
            comando = 'SetMotor LWheelDist ' + str(distancia_L) + ' RWheelDist ' + str(distancia_R) + ' Speed ' + str(self.speed * pow(-1, self.direction))
            #print(comando)
            self.enviaR(comando, 0.4)
        return(esq)
    
    #Just move without crash
    def random_path(self):
        print("Starting random path without crashing")
        while True:
            values = self.laser.get_laser()
            #print(values)
            if values[0] < 650:
                auxvals = [values[1] + values[2], values[8] + values[9]]
                idx = auxvals.index(max(auxvals)) #Agafar el valor maxim
                if idx == 0:  #Girar a l'esquerre
                    self.theta = +3.141516/3.5
                    print("Turn left")
                else:
                    self.theta = -3.141516/3.5
                    print("Turn right")
            elif (values[1] < self.distance) or (values[9] < self.distance):
                if (values[1] < self.distance) and (values[9] < self.distance):
                    if values[9] < values[1]:
                        self.theta = +3.141516/6
                        print("Turn left")
                    else:
                        self.theta = -3.141516/6
                        print("Turn right")                
                elif(values[1] < self.distance):
                    self.theta = -3.141516/6
                    print("Turn right")
                else:
                    self.theta = self.theta+3.141516/6
            elif (values[8] < self.distance) or (values[2] < self.distance):
                if (values[8] < self.distance) and (values[2] < self.distance):
                    if values[8] < values[2]:
                        self.theta = +3.141516/8
                        print("Turn left")
                    else:
                        self.theta = -3.141516/8
                        print("Turn right")
                elif(values[8] < self.distance):
                    self.theta = +3.141516/8
                    print("Turn left")
                else:
                    self.theta = -3.141516/8
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
                
    def followWal(self):
        self.gotoWall()
        print("Following wall now")
        while True:
            values = self.laser.get_laser()
            if values[0] < 650:
                self.theta = 3.141516/4
                print("FRONT")
            elif (values[8] > 330 or values[9] > 330):
                self.theta =  -3.141516/12
                print("Turn right")
            elif (values[8] < 300 or values[9] < 300):
                self.theta = 3.141516/26
                print("Turn left")
            else:
                self.theta = 0
            distancia_R = (((self.speed * pow(-1, self.direction) ) + (self.S * self.theta)) * self.tiempo) * pow(-1, self.direction)
            distancia_L = (((self.speed * pow(-1, self.direction) ) + (-self.S * self.theta)) * self.tiempo) * pow(-1, self.direction)
            comando = 'SetMotor LWheelDist ' + str(distancia_L) + ' RWheelDist ' + str(distancia_R) + ' Speed ' + str(self.speed * pow(-1, self.direction))
            self.enviaR(comando, 0.1)

    def gotoWall(self):
        print("Going to wall")
        values = self.laser.get_laser()
        while(values[0] > 750):
            print(values)
            self.theta = 0
            distancia_R = (((self.speed * pow(-1, self.direction) ) + (self.S * self.theta)) * self.tiempo) * pow(-1, self.direction)
            distancia_L = (((self.speed * pow(-1, self.direction) ) + (-self.S * self.theta)) * self.tiempo) * pow(-1, self.direction)
            comando = 'SetMotor LWheelDist ' + str(distancia_L) + ' RWheelDist ' + str(distancia_R) + ' Speed ' + str(self.speed * pow(-1, self.direction))
            self.enviaR(comando, 0.1)
            values = self.laser.get_laser()
        print("Wall reached")
        values = self.laser.get_laser()
        comando = 'SetMotor LWheelDist 0 RWheelDist ' + str(int(round((math.pi/2) * self.S))) + ' Speed ' + str(self.speed * pow(-1, self.direction))
        self.enviaR(comando, 2)
        
    def fuig_segueix(self, fuig):
        get_angle = self.__get_angle_fuig
        if fuig:
            print("Fugint")
        else:
            get_angle = self.__get_angle_persegueix
            print("Perseguint")
        while True:
            closer = self.laser.get_closer_object()
            self.theta, direct = get_angle(closer)
            print("Closer: ", closer)
            print("Angle: ", self.theta)
            distancia_R = (((250 ) + (self.S * self.theta)) * self.tiempo) * pow(-1, direct)
            distancia_L = (((250 ) + (-self.S * self.theta)) * self.tiempo) * pow(-1, direct)
            print("RL: ", [distancia_R, distancia_L])
            comando = 'SetMotor LWheelDist ' + str(distancia_L) + ' RWheelDist ' + str(distancia_R) + ' Speed ' + str(250)
            print("Comando: ", comando)
            self.enviaR(comando, 0.5)
    
    def __get_angle_fuig(self, closer):
        if closer == 0:
            return 0, 1
        elif closer < 5:
            return -math.pi + (closer * math.pi/5), 0
        elif closer > 5:
            return math.pi - (abs(closer - 8) * math.pi/5), 0
        else:
            return 0, 0
            
    def __get_angle_persegueix(self, closer):
        if closer == 5:
            return 0, 1
        elif closer > 0 and closer < 6:
            return math.pi - (abs(closer-5) * math.pi/5), 0
        elif closer > 5:
            return -math.pi + (abs(closer-5) * math.pi/5), 0
        else:
            return 0, 0

    def enviaR(self, msg, t):
        buffer = envia(self.ser, msg, t)
        return buffer
        
    def stop(self):
        comando = 'SetMotor LWheelDist 0 RWheelDist 0 Speed 0'
        self.enviaR(comando, 0.1)
        self.laser.enable(False)
        self.viewer.quit()
