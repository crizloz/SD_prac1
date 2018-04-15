# -*- coding: utf-8 -*-
import os, sys

#	echo -e "1. Nombre fichero"
#	echo -e "2. Número slaves"
#	echo -e "3. Programa (CountingWords = cw || WordCount = wc)"
#	echo -e "4. IP local"
#	echo -e "5. IP server"


#prints de prueba:
print "1. Nombre fichero: "+sys.argv[1]
print "2. Número slaves: "+sys.argv[2]
print "3. Programa (CountingWords = cw || WordCount = wc): "+sys.argv[3]
print "4. IP local: "+sys.argv[4]
print "5. IP server: "+sys.argv[5]

slaves=int(sys.argv[2])  	#seteamos el número de slaves

os.system("python reducer.py %s" %(sys.argv[4]))	#iniciamos el reducer con la IP local
for i in range(slaves):		#iniciamos tantos mappers como slaves haya con la IP local --> indice slave
	os.system("gnome-terminal -e 'bash -c \"python mapper.py %i %s; exec bash\"'" %(i+1,sys.argv[4]))	#cada mapper lo abrimos en un nuevo terminal --> EN UBUNTU
	#os.system("python mapper.py %i %s" %(i+1,sys.argv[4]))   #sin abrirlo en terminales diferentes
os.system("python server.py %s %i %s %s %s," %(sys.argv[1], slaves, sys.argv[3], sys.argv[4], sys.argv[5])) 	#iniciamos programa con nombre fichero, IP local e IP server