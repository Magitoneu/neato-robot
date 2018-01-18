#!/usr/bin/python
#coding: utf8

"""
Imports de Procesos
"""
"""
Imports
"""
import time
from turtle import *
import math

"""
Imports de Procesos
"""
from multiprocessing import Queue
from Queue import Empty

def getValues(msg):
	values = msg.split("\n")

	LWSm = values[8]
	RWSm = values[12]

	R_p_mm = int(RWSm[24:])
	L_p_mm = int(LWSm[23:])
	return R_p_mm, L_p_mm

def theoricOdometry(oldIncR, oldIncL, S, msg):
	(nIncR, nIncL) = getValues(msg)
	incR = nIncR - oldIncR
	incL = nIncL - oldIncL
	oldIncR = nIncR
	oldIncL = nIncL

	d_d = (incR+incL)/2
	d_theta = (incR-incL)/(2*S)
	return d_d, d_theta

def poseIntegration(oldIncR, oldIncL, x, y, theta, S, msg):
	(d_d, d_theta) = theoricOdometry(oldIncR, oldIncL, S, msg)
	theta = (theta + d_theta)%(2*3.141592)
	x = x + (d_d)*math.cos(theta)
	y = y + (d_d)*math.sin(theta)
	return x, y, theta

def getLaserValues(msg):
	Lv = []
	values = msg.split("\n")
	#Eliminar informacion que no son valores
	del values[0]
	del values[0]
	del values[360]
	del values[360]
	i = 0
	for s in values:
		auxv = s.split(",")
		Lv.append( ((int(auxv[1])*math.cos(i)), (int(auxv[1])*math.sin(i))) )
		i+=1
	return Lv

def run(queue_in, queue_out, queue_out2):
	
	print "#### Start OdometryLaser Process."
	
	S = float(queue_in.get())
	print "#### OdometryLaser Process: S = " + str(S)

	print '#### OdometryLaser Process: Started.'
	
	x_r_last = 999.9
	y_r_last = 999.9
	tita_dot = 0

	oldIncR = 0
	oldIncL = 0


	queue_out.put('Odo')

	while True:

		try:
			
			msg = queue_in.get()
			#msg = queue_in.get_nowait()
			#start_total = time.time()

		except Empty:
			
			#print '#### OdometryLaser Process: Nothing.'
			pass
		
		else:
            
			#print "#### OdometryLaser Process: msg -> " + msg

			if msg == 'quit':
				
				break

			elif msg[0] == 'O':
				
				# ODO
				msg = msg[1:]
				#print msg
				
				x_r = 0 # Pos X robot
				y_r = 0 # Pos Y robot

				pos_robot = [] # Vector of 2 positions (x, y of robot)
				
				#########################################################################################################################				
			# AFEGIR AQUI CODI ODOMETRIA
				(x_r, y_r, tita_dot) = poseIntegration(oldIncR, oldIncL, x_r_last, y_r_last, tita_dot, S, msg)
				#print "x = \n"
				#print x_r
				#print "y = \n"
				#print y_r
				pos_robot = [x_r, y_r]
			#########################################################################################################################
				
				if x_r_last != x_r or y_r_last != y_r:
					
					queue_out2.put(pos_robot)
					x_r_last = x_r
					y_r_last = y_r
			
			elif msg[0] == 'L':

				# Laser
				msg = msg[1:]
				#print msg

				datos_laser = [] # Vector of 720 or fewer positions always but always pair (x, y)
				
				#########################################################################################################################
				
				# AFEGIR AQUI LA RECONSTRUCIÓ INFORMACIÓ LASER
				datos_laser = getLaserValues(msg)
				#########################################################################################################################

				queue_out2.put(datos_laser)
			
			queue_out.put('Odo')
			time.sleep(1.75)
			#print "\nTiempo Total p_OdometryLaser: " + str(time.time() - start_total) + " segundos.\n"

	print "#### Finished OdometryLaser Process."