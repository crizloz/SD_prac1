# -*- coding: utf-8 -*-
'''
Manuel Ruiz Botella
Cristina Izquierdo Lozano
-------------------------
Practica 1 SD
'''
#-----------------------MAIN-server--------------------------------- 

from pyactor.context import set_context, create_host, serve_forever, Host
from pyactor.exceptions import TimeoutError
import commands, sys, io

global host, dicc, i
i = 0

#Clase server
#lee el fichero con palabras:
class Server(object):
	_tell = ['readFile']
	_ask = []
	_ref = ['readFile']
	
	def readFile(self, hosts_maps, host_red):
		global dicc, i
		os.system("wget"+ip_server+"/"+fichero)
		#file  = io.open(fichero, "r", encoding="latin-1")								#abre el fichero
		word_total = int(commands.getoutput("wc -w "+fichero+" | cut -d ' ' -f 1")) 	#cuenta el total de palabras
		lineas_total = int(commands.getoutput("wc -l "+fichero+" | cut -d ' ' -f l")) 	#cuenta el total de líneas
		print "cw: "+word_total	
		
		reduc = host_red.spawn('reducer', 'reducer/Reducer')
		num_lines_por_mapa = lineas_total/slaves
		if (lineas_total % slaves) != 0:
			num_lines_por_mapa += 1
		for cliente in range(0, slaves-1):
				maps[cliente] = hosts_maps[cliente].spawn(str(cliente), 'mapper/Mapper')
				print "creado cliente"+cliente
		directory = os.getcwd()+"/files"
		print "directorio es:"+directory
		if not os.path.exists(directory):
			print "creando directorio para las files"
			os.makedirs(directory)
		for cliente_d in range(0, slaves-1):
			filenueva = io.open(directory+"/file_"+str(cliente_d)+".txt", "w", encoding="latin-1")
			for linea in range(0, num_lines_por_mapa):
				line = file.readline()
				if line != "\n":
					filenueva.write(line)
			print "file para el "+cliente_d+" creada" 
			filenueva.close()
		i = 0
		reducer.iniciar_tiempo() 			#iniciamos el tiempo del sistema (entrada al primer mapper)
		for mapa in maps:
			filetratar = io.open(directory+"/file_"+str(i)+".txt", "r", encoding="latin-1")
			i += 1
			print "poniendo a mapear el mapa "+mapa
			mapa.map(filetratar, reducer)
			filetratar.close()
		file.close()
		

if __name__ == "__main__": #PARAMETROS: nombre_fichero, n_slaves, programa, ip_local, ip_server
	set_context()
#try:  con el try nunca entra aqui dentro, por lo tanto nunca define los argumentos
#	if len(sys.argv) != 5:
#		raise IndexError
	
	fichero = str(sys.argv[1])
	print "[SERVER]nombre fichero: "+fichero					#comprovación: borrar luego
	slaves = int(sys.argv[2])
	print "[SERVER]n_slaves: ",slaves 				#comprovación: borrar luego
	print "[SERVER]cw/wc: "+sys.argv[3]				#comprovación: borrar luego
	
	if (str(sys.argv[3]) == "cw"): 	#si escogen cw (CountingWords)
		countingWords = True		#haremos la función de cw
	else:							#en caso contrario, haremos la otra función (wc)
		countingWords = False
	print "Estoy dentro del if\n" 		#comprovación: borrar luego  --> NO ENTRA NUNCA
	ip_local = str(sys.argv[4])
	print "[SERVER]ip_local: "+ip_local			#comprovación: borrar luego
	ip_server = 'http://'+str(sys.argv[5])+':8000'
	print "[SERVER]ip_server: "+ip_server			#comprovación: borrar luego
#except IndexError:
	print "\nERROR: Argumentos inválidos.\nDeberían ser:\n1. Nombre fichero\n2. Número slaves\n3. Programa (CountingWords = cw || WordCount = wc)\n4. IP local\n5. IP server\n"
#finally:
	print "[SERVER]Finally: "+ip_local			#comprovación: borrar luego
	host = create_host('http://'+ip_local+':1277')
	server = host.spawn('server', 'server/Server')
	print "server listening at port 1277"
	hosts_maps = {}
	for num in range(0,slaves-1):
		hosts_maps[num] = host.lookup_url('http://'+ip_local+':130'+str(i), Host)  #NameError: name 'hosts_maps' is not defined
	host_red = host.lookup_url('http://'+ip_local+':1275', Host)
	reducer = host_red.spawn('reducer', 'reducer/Reducer')
	server.readFile(hosts_maps,host_red)
	serve_forever()