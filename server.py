# -*- coding: utf-8-sig -*-
'''
Manuel Ruiz Botella
Cristina Izquierdo Lozano
-------------------------
Practica 1 SD
'''
#-----------------------MAIN-server--------------------------------- 

from pyactor.context import set_context, create_host, serve_forever, Host
from pyactor.exceptions import TimeoutError
import commands, sys, io, os, urllib

global host, dicc, i 
i = 0

#Clase server
#lee el fichero con palabras:
class Server(object):
	_tell = ['readFile']
	_ask = []
	_ref = ['readFile']
	
	def readFile(self, hosts_maps, reducer, ip_server, fichero, slaves, countingWords):
		global dicc, i 
		print ip_server+"/"+fichero
		urllib.urlretrieve(ip_server+"/"+fichero, fichero)
		print "hola 2"
		fich  = io.open(fichero, "r", encoding="utf-8-sig")				#abre el fichero
		
		lineas_total = int(commands.getoutput("wc -l "+fichero+" | cut -d ' ' -f1")) 	#cuenta el total de líneas

		

		num_lines_por_mapa = lineas_total/slaves
		if (lineas_total % slaves) != 0:
			num_lines_por_mapa += 1
		maps={}
		for cliente in range(0, slaves):
				maps[cliente] = hosts_maps[cliente].spawn('mapa'+str(cliente), 'mapper/Mapper')
				print "creado cliente"+str(cliente)
		directory = os.getcwd()
		print "directorio es:"+directory
		for cliente_d in range(0, slaves):
			filenueva = io.open(directory+"/texts/partes/file_"+str(cliente_d)+".txt", "w", encoding="utf-8-sig")
			for linea in range(0, num_lines_por_mapa):
				line = fich.readline()
				if line != "\n":
					filenueva.write(line)
			print "file para el "+str(cliente_d)+" creada" 
			filenueva.close()
		reducer.iniciar_tiempo(slaves, countingWords) 			#iniciamos el tiempo del sistema (entrada al primer mapper)
		for mapa in range(0,slaves):
			print "poniendo a mapear el mapa "+str(mapa)
			maps[mapa].map(ip_server,str(mapa)+".txt", reducer)
		fich.close()
		

if __name__ == "__main__": #PARAMETROS: nombre_fichero, n_slaves, programa, ip_local, ip_server
	set_context()
#try:  con el try nunca entra aqui dentro, por lo tanto nunca define los argumentos
#	if len(sys.argv) != 5:
#		raise IndexError
	
	fichero = str(sys.argv[1])
	slaves = int(sys.argv[2])
	if (str(sys.argv[3]) == "cw"): 		#si escogen cw (CountingWords)
		countingWords = True		#haremos la función de cw
	else:					#en caso contrario, haremos la otra función (wc)
		countingWords = False
	ip_local = str(sys.argv[4])
	ip_server = 'http://'+str(sys.argv[5])+':8000'
#except IndexError:
	print "\nERROR: Argumentos inválidos.\nDeberían ser:\n1. Nombre fichero\n2. Número slaves\n3. Programa (CountingWords = cw || WordCount = wc)\n4. IP local\n5. IP server\n"
#finally:
	host = create_host('http://'+ip_local+':1277')
	server = host.spawn('server', 'server/Server')
	print "server listening at port 1277"
	hosts_maps = {}


	for num in range(0,slaves):
		hosts_maps[num] = host.lookup_url('http://'+ip_local+':130'+str(num), Host)
	host_red = host.lookup_url('http://'+ip_local+':1275', Host)
	reducer = host_red.spawn('reducer', 'reducer/Reducer')
	server.readFile(hosts_maps,reducer,ip_server,fichero,slaves,countingWords)
	serve_forever()
