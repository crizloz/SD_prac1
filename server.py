#!C:\Windows\Installer\{104875A1-D083-4A34-BC4F-3F635B7F8EF7}/PythonCommandline_2DCD57AEB570448BB9DAE8BD890521FF.exe
#!/usr/bin/env python
'''
Manuel Ruiz Botella
Cristina Izquierdo Lozano
-------------------------
Practica 1 SD
'''
#-----------------------MAIN-server--------------------------------- 

from pyactor.context import set_context, create_host, serve_forever
import mapper as map

#funcion para leer el fichero con palabras:
def readFile():
	file  = open("fichero.txt", "r")
	lines = file.readlines()
	i = 0
	for line in lines:
		map.map(i,line) #map recibe el numero de lunea y la linea entera
		i+=1
	file.close()

class Echo(object):
    _tell = ['echo']
    _ask = ['get_msgs']

    def __init__(self):
        self.msgs = []

    def echo(self, msg):
        print msg
        self.msgs.append(msg)

    def get_msgs(self):
        return self.msgs


if __name__ == "__main__":
    set_context()
    host = create_host('http://127.0.0.1:1277/')
    readFile()
    e1 = host.spawn('echo1', Echo)
    serve_forever()