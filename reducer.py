# -*- coding: utf-8-sig -*-
'''
Manuel Ruiz Botella
Cristina Izquierdo Lozano
-------------------------
Práctica 1 SD
-------------
Reducer
'''
from pyactor.context import sleep, set_context, create_host, serve_forever
import sys, time

global dicc
dicc={}

class Reducer(object):
	_tell = ['iniciar_tiempo', 'parar_tiempo', 'trabaja'] 	#asíncrono
	_ask = [] 						#síncrono

	def iniciar_tiempo(self, slaves, programa):
		self.tiempoInicial = time.time() 		#nos guardamos el tiempo inicial
		self.slaves = slaves				#seteamos el número de slaves
		self.programa = programa			#seteamos el programa que usaremos

	def parar_tiempo(self):
		tiempoFinal = time.time() 			#nos guardamos el tiempo final
		tiempo = tiempoFinal - self.tiempoInicial 	#hacemos la resta entre el inicial y el final
		print "Tiempo: ",tiempo
	

	def trabaja(self, palabras):
		global dicc
		for key in palabras.keys():
			dicc[key] = dicc.get(key, 0) + palabras[key]    	#si ya esta en el diccionario le sumamos 1 y si no está le pondrá el valor de 1
		self.slaves=self.slaves-1
		if(self.slaves==0):
			if (self.programa==True):
				result = 0
				for key in dicc.keys():
					result = result +int(dicc[key])
				print "Counting Words: ",result
			else:
				result = 0
				print "Word count: \n"
				for key in dicc.keys():
					print str(key),":",dicc[key],"\n"	#para cada clave printeamos el valor --> clave:valor
			self.parar_tiempo()					#paramos el tiempo (final reducer)

if __name__ == "__main__": #PARAMETROS: ip_local
	set_context()
	direccion = sys.argv[1]
	host = create_host('http://'+direccion+':1275')
	print "Reducer creado en http://"+direccion+":1275\n"
	serve_forever()
