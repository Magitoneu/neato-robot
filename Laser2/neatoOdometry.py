import time
import math
import numpy as np

class NeatoOdometry:
    speed = 120.0
    S = 121.5

    def __init__(self, Lini, Rini):
        self.L_ini, self.R_ini = Lini, Rini
        self.X_k, self.V, self.X, self.sum_theta =  [[0.0],[0.0],[0.0]], [[0.00002, 0.0],[0.0, 0.0002]], [[0.0],[0.0],[0.0]], 0.0
        self.Fx = [[0 for x in range(3)] for y in range(3)]
        self.Fv = [[0 for x in range(2)] for y in range(3)]
        self.P_k = [[0 for x in range(3)] for y in range(3)]
        #P_k[0][0], P_k[1][1], P_k[2][2] = 1, 1, 1
        
    def updateOdometry(self, L, R):
        new_L, new_R = L - self.L_ini, R - self.R_ini
        d_k = (new_L+new_R)/2.0
        theta_k = (new_R-new_L)/243.0
        vk = [self.V[0][0], self.V[1][1]]
        
        self.Fx[0][0], self.Fx[0][1], self.Fx[0][2] = 1.0, 0.0, -(d_k * math.sin(self.sum_theta + theta_k))
        self.Fx[1][0], self.Fx[1][1], self.Fx[1][2] = 0.0, 1.0, (d_k * math.cos(self.sum_theta + theta_k))
        self.Fx[2][0], self.Fx[2][1], self.Fx[2][2] = 0.0, 0.0, 1.0
        
        self.Fv[0][0], self.Fv[0][1] = math.cos(self.sum_theta + theta_k), -d_k*math.sin(self.sum_theta + theta_k)
        self.Fv[1][0], self.Fv[1][1] = math.sin(self.sum_theta + theta_k), d_k*math.cos(self.sum_theta + theta_k)
        self.Fv[2][0], self.Fv[2][1] = 0.0, 1.0
        
        self.X_k = np.add(self.X_k, np.dot(self.Fx, np.subtract(self.X, self.X_k)))
        self.X_k = np.add(self.X_k, np.dot(self.Fv, vk))
            
        x_word = self.X_k[0][0]
        y_word = self.X_k[1][0]
        theta_word = self.X_k[2][0]
        
        self.X[0][0] = self.X[0][0] + d_k * math.cos(self.sum_theta + theta_k)
        self.X[1][0] = self.X[1][0] + d_k * math.sin(self.sum_theta + theta_k)
        self.X[2][0] = self.X[2][0] + theta_k
        self.sum_theta = (self.sum_theta + theta_k)
        
        if self.sum_theta > (math.pi):
            self.sum_theta = self.sum_theta - (2*math.pi)
            
        if (self.sum_theta < -(math.pi)):
            self.sum_theta = self.sum_theta + (2*math.pi)
        
        self.P_k = np.add(np.dot(np.dot(self.Fx, self.P_k), np.transpose(self.Fx)), np.dot(np.dot(self.Fv, self.V), np.transpose(self.Fv)))

        self.L_ini, self.R_ini = L, R
        return
        
    def getTheoricPose(self):
        return self.X
        
    def getEstimatedPose(self):
        return self.X_k
        
    def getGoToPoint(self, xpos, ypos):
        xpos = xpos - self.X[0][0]
        ypos = ypos - self.X[1][0]
        
        print("Where to go: ", [xpos, ypos])
        
        distance = math.sqrt(math.pow(xpos, 2.0) + math.pow(ypos, 2.0))
        angle = self.__angle_diff(math.atan2(ypos, xpos), self.sum_theta)
        time = 0.75
        
        # print("Distance: ", distance)
        # print("Angle: ", angle)
        # print("Atan2: ", math.atan2(ypos, xpos))
        # print("Suma_theta: ", self.sum_theta)
        # print("Time: ", time)
        
        if (distance < 50):
            return 0, 0
        
        distancia_R = ((self.speed + (self.S * angle)) * time)
        distancia_L = ((self.speed + (-self.S * angle)) * time)
        
        return int(round(distancia_L)), int(round(distancia_R)), angle
        
    def __angle_diff(self, a, b):
        return math.atan2(math.sin(a-b), math.cos(a-b))
        