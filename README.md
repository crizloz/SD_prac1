# Communication models and middleware
###### Sistemas Distribuidos - Práctica 1
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/27b7d46671364ba891d2f47405c490b5)](https://www.codacy.com/app/crizloz/SD_prac1?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=crizloz/SD_prac1&amp;utm_campaign=Badge_Grade)

Implementación de un MapReduce simplificado para la primera práctica de la asignatura de Sistemas Distribuidos.
## Prerequisitos
Esta implementación utiliza el middleware pyactor. Para instalarlo:
```
sudo pip install pyactor
```
Para más información sobre pyactor y su instalación: [PyActor](https://github.com/pedrotgn/pyactor#installation)
## Diseño
El proyecto tiene una arquitectura master/slave, donde hay un reducer y el número deseado de mappers, controlados por el master.
La estructura es la siguiente:
- **server.py:** programa principal que controla el proceso. En esta implementación, se encarga de leer el fichero y partirlo para los distintos mappers.
- **mapper.py:** actor para la función map.
- **reducer.py:** actor para la función reduce. Una vez ha recibido el resultado del último mapper para el tiempo y muestra el resultado por pantalla.
- **secuencial.py:** contiene el map y el reduce en un único fichero para poder usar el programa en secuencial.
- **script_ini.py:** script para inicializar los actores en diferentes máquinas.
## Parámetros
1. **Nombre fichero:** `int` nombre del fichero que se quiere evaluar.
2. **Número slaves:** `int` número de mappers funcionando en paralelo.
3. **Programa (CountingWords = cw || WordCount = wc):** `string` función del programa deseada.
    - CountingWords (wc): devuelve el total de palabras del fichero.
    - WordCount (cw): devuelve las ocurrencias de cada una de las palabras que hay en el fichero.
4. **IP local:** `string` IP local donde se crean los actores.
5. **IP server:** `string` IP del servidor donde se guardan lo ficheros de texto.
## Ejecución
1. Acceder a la carpeta donde estan guardados los ficheros de texto desde un terminal.
2. Lanzar un servidor web de esa carpeta:
```
python -m SimpleHTTPServer
```
3. En un terminal diferente, ejecutar el script de inicialización:
```
python script_ini.py [nombre_fichero][n_slaves][programa][ip_local][ip_server]
```
## Autores
- Manuel Ruiz Botella - [manurubo](https://github.com/manurubo)
- Cristina Izquierdo Lozano - [crizloz](https://github.com/crizloz)
