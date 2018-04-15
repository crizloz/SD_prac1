# -*- coding: utf-8 -*-
'''
Manuel Ruiz Botella
Cristina Izquierdo Lozano
-------------------------
Practica 1 SD
'''
#-----------------------REDUCE--------------------------------- 

from pyactor.context import set_context, create_host, serve_forever, Host
from pyactor.exceptions import TimeoutError
import sys, time

#global url_reducer
#url_reducer = 'http://127.0.0.1:1275/'

global dicc
dicc = {}
global slaves
slaves = 8
global countingWords		#global para saber cual de las funciones debemos ejecutar
#countingWords = True 		

#funcion reduce
#devuelve clave:suma_valores
class Reducer(object):
	_tell = ['iniciar_tiempo', 'parar_tiempo', 'trabaja'] 				#asincrono
	_ask = [] 									#sincrono

	def iniciar_tiempo(self):
		self.tiempoInicial = time.time() 	#nos guardamos el tiempo inicial

	def parar_tiempo(self):
		tiempoFinal = time.time() 			#nos guardamos el tiempo final
		tiempo = tiempoFinal - self.tiempoInicial 	#hacemos la resta entre el inicial y el final
		print "Tiempo: "+tiempo
	

	def trabaja(palabras):
		global dicc
		global slaves
		print "Estoy en el reduce\n"
		for key in palabras.keys():
			if key in dicc.keys():
				dicc[key] = dicc.get(key, 0) + palabras[key]    #si ya esta en el diccionario le sumamos 1
			else:
				dicc[key] = palabras.get(key, 0)           		#si no esta, anadimos la clave al nuevo diccionario con las ocurrencias de esta en la linea
		slaves-=1
		if(slaves==0):
			if countingWords:
				result = 0 
				for key in dicc.keys():
					result = result+"\n"+ dicc[key] 
				self.parar_tiempo()									#paramos el tiempo (final reducer)
				print "Counting Words: "+result	
			else:
				result = 0 
				print "Word count: \n"
				for key in dicc.keys():
					print key+", "+dicc[key]+";\n" 				#para cada clave printeamos el valor
				self.parar_tiempo()									#paramos el tiempo (final reducer)
		
#main
if __name__ == "__main__": #PARAMETROS: ip_local
	set_context()
	direccion = sys.argv[1]
	print "[REDUCE]direccion: "+direccion
	host = create_host('http://'+direccion+':1275')
	
	print "reducer creado en http://"+direccion+":1275"

	serve_forever()