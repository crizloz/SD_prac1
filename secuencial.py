# -*- coding: utf-8-sig -*-
'''
Manuel Ruiz Botella
Cristina Izquierdo Lozano
-------------------------
Práctica 1 SD
'''
#-------------------------------------------------------------------SECUENCIAL--------------------------------------------------------------- 

from pyactor.context import set_context, create_host, sleep, shutdown, Host
from pyactor.exceptions import TimeoutError
import commands, sys, io, os, time


global dicc 
dicc = {}

class Reducer(object):
        _tell = ['iniciar_tiempo', 'parar_tiempo', 'trabaja']   #asíncrono
        _ask = []                                               #síncrono
        global slaves

        def iniciar_tiempo(self, slaves, programa):
                self.tiempoInicial = time.time()                #nos guardamos el tiempo inicial
                self.slaves = slaves                            #seteamos el número de slaves
                print self.slaves
		self.programa = programa                        #seteamos el programa que usaremos

        def parar_tiempo(self):
                tiempoFinal = time.time()                       #nos guardamos el tiempo final
                tiempo = tiempoFinal - self.tiempoInicial       #hacemos la resta entre el inicial y el final
                print "Tiempo: ",tiempo
	
	def trabaja(self, palabras):
                global dicc
                for key in palabras.keys():
                        dicc[key] = dicc.get(key, 0) + palabras[key]            #si ya esta en el diccionario le sumamos 1 y si no está le pondrá el valor de 1
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
                                        print str(key),":",dicc[key],"\n"       #para cada clave printeamos el valor --> clave:valor            
                        self.parar_tiempo()					#paramos el tiempo (final reducer)
class Mapper(object):
        _tell = ['map']         #asíncrono
        _ask = []               #síncrono
        _ref = ['map']

        def map(self, archivo, reducer):
                diccionario = {}
		d = os.getcwd()							#obtenemos el path actual
		path = d+"/texts/"+archivo					#montamos el path donde ir a buscar los ficheros
                palabras = io.open(path, "r", encoding="utf-8-sig")
                texto = palabras.read()
                texto = texto.lower()
                #eliminamos símbolos y signos de puntuación:
                texto= texto.replace('.', '').replace(',', '').replace(':', '').replace(';', '').replace('\n', ' ').replace('\r', ' ').replace('#', '').replace('[', '').replace(']', '').replace('*','').replace('  ', ' ').replace('-', ' ').replace('_', '').replace('?', '').replace('!', '').replace('\'', ' ').replace('\"', '').replace('(', '').replace(')', '').replace('=', '').replace('<', '').replace('>', '')
                splits = texto.split(" ")               		#separamos la linea en palabras
                for x in splits:                        		#para cada palabra en la lista de palabras de la linea
                        if x.endswith('-') or x.startswith('-'):  	#eliminamos los guiones de las conversaciones
                                x.replace('-','')
                        diccionario[x] = diccionario.get(x, 0) + 1   	#get(palabra, default) --> si el vector no tiene la palabra x devuelve un 0 por defecto, si la palabra esta en el diccionario te devuelve las ocurrencias de esta. A esto le sumamos 1
                reducer.trabaja(diccionario)


	
if __name__ == "__main__": #PARÁMETROS: direccion_IP, nombre_fichero, programa
	set_context()
	direccion=str(sys.argv[1])
	fichero=str(sys.argv[2])
	if (str(sys.argv[3]) == "cw"):          #si escogen cw (CountingWords)
                countingWords = True            #haremos la función de cw
        else:                                   #en caso contrario, haremos la otra función (wc)
                countingWords = False
	host = create_host('http://'+direccion+':2000')
        reducer = host.spawn('reducer', Reducer)
	host2 = create_host('http://'+direccion+':3000')
        mapper = host2.spawn('mapper', Mapper)
	reducer.iniciar_tiempo(1,countingWords)
	mapper.map(fichero,reducer)
	sleep(5)
	shutdown()

