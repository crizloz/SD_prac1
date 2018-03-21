'''
Manuel Ruiz Botella
Cristina Izquierdo Lozano
-------------------------
Practica 1 SD
'''
#-----------------------MAP--------------------------------- 
import sys

#funcion map, recibe el numero de linea y la linea
def map(i,line):
	palabras = {}
	line = line.lower()
	line = line.replace('.', '').replace(',', '').replace(':', '').replace(';', '')
	splits = line.split(" ") 	#separamos la linea en palabras
	for x in splits: 			#para cada palabra en la lista de palabras de la linea
		suffix = "\r\n"			#elimina la basura del final
		if x.endswith(suffix):  
			x=x[:-2]
		palabras[x] = palabras.get(x, 0) + 1	#get(palabra, default) --> si el vector no tiene la palabra x devuelve un 0 por defecto, si la palabra esta en el diccionario te devuelve las ocurrencias de esta. A esto le sumamos 1
	print palabras
	return palabras

	#http://www.tutorialspoint.com/python/dictionary_get.htm