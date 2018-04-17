# -*- coding: utf-8-sig -*-
'''
Manuel Ruiz Botella
Cristina Izquierdo Lozano
-------------------------
Práctica 1 SD
--------------
Mapper
'''
from pyactor.context import set_context, create_host, serve_forever, sleep, shutdown
import server, sys, io, urllib


class Mapper(object):
	_tell = ['map'] 	#asíncrono
	_ask = [] 		#síncrono
	_ref = ['map']

	def map(self,ip_server, num_archivo, reducer):
		dicc = {}
		palabras = urllib.urlopen(ip_server+"/partes/file_"+str(num_archivo))
		texto = palabras.read()
		texto = texto.lower()
		#eliminamos símbolos y signos de puntuación:
		texto= texto.replace('.', '').replace(',', '').replace(':', '').replace(';', '').replace('\n', ' ').replace('\r', ' ').replace('#', '').replace('[', '').replace(']', '').replace('*','').replace('  ', ' ').replace('-', ' ').replace('_', '').replace('?', '').replace('!', '').replace('\'', ' ').replace('\"', '').replace('(', '').replace(')', '').replace('=', '').replace('<', '').replace('>', '')	
		splits = texto.split(" ")				#separamos la linea en palabras
		for x in splits: 					#para cada palabra en la lista de palabras de la linea
			if (x==''):
				continue
			if x.endswith('-') or x.startswith('-'):  	#eliminamos los guiones de las conversaciones
				x.replace('-','')
			dicc[x] = dicc.get(x, 0) + 1			#get(palabra, default) --> si el vector no tiene la palabra x devuelve un 0 por defecto, si la palabra esta en el diccionario te devuelve las ocurrencias de esta. A esto le sumamos 1
		reducer.trabaja(dicc)


if __name__ == "__main__": #PARAMETROS: indice_mapper, ip_local
	set_context()
	direccion = sys.argv[2]
	i = sys.argv[1]
	host = create_host('http://'+direccion+':130'+i)	#creamos un server para el mapper
	print "Mapper creado en http://"+direccion+":130"+i
	serve_forever()
