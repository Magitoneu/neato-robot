# To import the function "envia" from the file "test_NeatoCommands.py"
from test_NeatoCommands import envia

import serial
import time
import math
import numpy as np


def get_motors():
    """ Ask to the robot for the current state of the motors. """
    msg = envia(ser, 'GetMotors LeftWheel RightWheel').split('\n')
    
    # For better understanding see the neato commands PDF.
    
    L = int(msg[4].split(',')[1])
    R = int(msg[8].split(',')[1])
    
    return (L, R)

                
def odometry(L, R):
    #Implement the pos integration. Assume initial conditions [0,0,0].

    #Use global variables, discoment this line
    
    #X -> Teoric Pose
    #X_k -> Estimated pose
    #P_k -> Covariance 
    
    global new_L, new_R
    global X_k, vk, X, theta_word, P_k            
    new_L, new_R = L - L_ini, R - R_ini
    d_k = (new_L+new_R)/2
    theta_k = (new_R-new_L)/243
    
    X[0][0] = X[0][0] + d_k * math.cos(theta_word + theta_k)
    X[1][0] = X[1][0] + d_k * math.sin(theta_word + theta_k)
    X[2][0] = X[2][0] + theta_k
    
    Fx[0][0], Fx[0][1], Fx[0][2] = 1, 0, -(d_k * math.sin(theta_k + theta_word))
    Fx[1][0], Fx[1][1], Fx[1][2] = 0, 1, (d_k * math.cos(theta_k + theta_word))
    Fx[2][0], Fx[2][1], Fx[2][2] = 0, 0, 1
    
    Fv[0][0], Fv[0][1] = math.cos(theta_k + theta_word), -d_k*math.sin(theta_k+theta_word)
    Fv[1][0], Fv[1][1] = math.sin(theta_k + theta_word), d_k*math.cos(theta_k+theta_word)
    Fv[2][0], Fv[2][1] = 0, 1
    
    
    X_k = np.add(X_k, np.dot(Fx, np.subtract(X, X_k)))
    X_k = np.add(X_k, np.dot(Fv, vk))
        
    x_word = X_k[0][0]
    y_word = X_k[1][0]
    theta_word = X_k[2][0]
    
    
    print("X_k", X_k)
    print("Fx", Fx)
    print("Fv", Fv)
    print("vk", vk)
    P_k = np.add(np.dot(np.dot(Fx, P_k), np.transpose(Fx)), np.dot(np.dot(Fv, vk), np.transpose(Fv))) 
    
    print(X_k)
    print(P_k)
    return x_word, y_word, theta_word

if __name__ == "__main__":
    # Open the Serial Port.
    global ser
    ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=0.05)
    envia(ser, 'TestMode On')

    envia(ser, 'PlaySound 1')    

    envia(ser ,'SetMotor RWheelEnable LWheelEnable')

    global L_ini, R_ini
    L_ini, R_ini = get_motors()
    global theta_k
    theta_k = 0
    global X_k, vk, X, theta_word
    X_k, vk, X, theta_word =  [[0],[0],[0]], [[0.00002, 0],[0, 0.0002]], [[0],[0],[0]], 0    
    
    speed = 100    # en mm/s
    envia(ser, 'SetMotor LWheelDist '+ str(1000) +' RWheelDist ' + str(1000) + ' Speed ' + str(speed*2))
    global Fx, Fv, P_k
    Fx = [[0 for x in range(3)] for y in range(3)]
    Fv = [[0 for x in range(2)] for y in range(3)]
    P_k = [[0 for x in range(3)] for y in range(3)]
    P_k[0][0], P_k[1][1], P_k[2][2] = 1, 1, 1

    try:
        while True:
            L, R = get_motors()
            X_k = odometry(L, R)
            time.sleep(0.1)
    except ValueError:
        print("ValueError: {0}".format(err))
        envia(ser ,'SetMotor RWheelDisable LWheelDisable')
    except KeyboardInterrupt:
        print("Damn son")
        envia(ser ,'SetMotor RWheelDisable LWheelDisable')

    envia(ser, 'TestMode Off', 0.2)

    # Close the Serial Port.
    ser.close()      

    print "Final"