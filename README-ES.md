# NEURONE-CS: NEURONE - evaluation Service for Compatibility with screen readers

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)

Creado por Polett Pizarro P.

## Descripción

NEURONE-CS es un servicio creado por la necesidad en NEURONE (oNlinE inqUiRy experimentatiON systEm) de verificar la compatibilidad que tiene el contenido web que es cargado en esta plataforma, con los software de lectura de pantalla. Para esto, el servicio entrega un detalle general por cada elemento evaluado, permitiendo la opción de ver recomendaciones para corregir cada uno de los elementos que presentan incompatibilidad.

Este servicio, a pesar de ser creado principalmente por la necesidad de NEURONE, puede ser utilizado de manera independiente.

NOTA: Los software de lectura de pantalla es una de las herramientas que utilizan principalmente las personas con situación de discapacidad visual o con dislexia para apoyar su navegación en la web. 

## Manual de usuario

El manual de usuario será publicado proximante. 

## Instrucciones de instalación

### Ambiente de desarrollo

*Nota:* Se recomienda especialemte el uso de sistema Linux.

#### Instalación en Linux:

1. Instalación de Python:

        $ sudo apt install python3

2. Instalación de biblioteca pip: 

        $ sudo apt install python3-pip

2. Instalación de Flask: 

        $ pip install Flask
        $ pip install -U https://github.com/pallets/flask/archive/master.tar.gz
        $ sudo apt install python3-flask
        $ sudo apt install python3-flask-restful
        $ pip3 install -U flask_cors

2. Instalación de biblioteca de extracción (scrapping): 
        
        $ sudo apt install python3-bs4

3. Instalación de biblioteca de traducción:

        $ sudo apt install python3-wget easy_install Flask-Babel
        $ sudo apt install python3-flask-babel

3. Instalación de biblioteca necesaria para limpieza de contenido: 

        $ sudo apt-get install python-lxml

#### Ejecución en Linux: 

##### Servicio de Evaluaciones 

1. Para ejecutar el orquestador principal de todo el servicio y en particular de los servicios de evaluación: 
    1. Abrir consola n° 1.
    2. Posicionarse el directorio del codigo fuente (.../NEURONE-CS).
    3. Ejecutar:

        $ cd CS_Evaluation/Evaluation_Service
        $ python3 main.py 

2. Para ejecutar todos los microservicios de evaluación:
    *NOTA 1:* Si se desea editar los servicios que se levantan, comentar las lineas correspondientes a los microservicios que se quiere desactivar en el archivo start-evaluations-ubuntu-local.sh, ubicado en .../NEURONE-CS/CS_Evaluation.
    *NOTA 2:* Para un correcto funcionamiento del servicio orquestador, es necesario que los microservicios de extracción y limpieza se encuentren siempre activos.
    1. Abrir consola n° 2.
    2. Posicionarse el directorio del codigo fuente (.../NEURONE-CS)
    3. Ejecutar:

        $ cd CS_Evaluation
        $ sudo sh start-evaluations-ubuntu-local.sh 

##### Servicio de Recomendaciones 

1. Para ejecutar el orquestador de los servicios de recomendaciones: 
    *NOTA:* Este servicio requiere del servicio de evaluación y los microservicios de extracción y limpieza para su correcto funcionamiento.
    1. Abrir consola n° 3.
    2. Posicionarse el directorio del codigo fuente (.../NEURONE-CS).
    3. Ejecutar:

        $ cd CS_Recomendation/Recomendation_Service
        $ python3 main.py 

2. Para ejecutar todos los microservicios de recomendaciones:
    1. Abrir consola n° 4.
    2. Posicionarse el directorio del codigo fuente (.../NEURONE-CS).
    3. Ejecutar:

        $ cd CS_Recomendation
        $ sudo sh start-recomendations-ubuntu-local.sh

#### Instalación en Windows

1. Instalar Python
2. Instalar pip por consola
        > python -m pip install --upgrade pip

3. Instalar bilioteca WTForms
        > pip install WTForms
        
4. Instalar Flask
        > pip install --user --upgrade flask-wtf

5. Instalar Wget
        > pip install wget

6. Instalar bilioteca para extracción (scrapping):
        > pip install beautifulsoup4

7. Instalar biliotecas para servicio rest-full
        > pip install requests
        > pip install flask_restful

8. Instalar biblioteca necesaria en limpieza de contenido: 
        > pip install lxml


#### Ejecución en Windows

1. Para el servicio de evaluación:
    1. Abrir consola n° 1.
    2. Posicionarse el directorio del codigo fuente (.../NEURONE-CS).
    3. Ejecutar: 
        > cd CS_Evaluation
        > python make.py

2. Para el servicio de recomendaciones:
    1. Abrir consola n° 2.
    2. Posicionarse el directorio del codigo fuente (.../NEURONE-CS).
    3. Ejecutar: 
        > cd CS_Recomendation
        > python make.py

_________________________________________________________________
**COMANDOS QUE PUEDEN RESULTAR UTILES EN AMBIENTE DE DESARROLLO**

# Para eliminar procesos cuando quedan activos al cerrar la consola, en ambiente de desarrollo en Linux:
1. Listar los procesos asociados a Python, para conocer su PID (Process ID):
        
        $ ps -ef | grep python3

2. Eliminar un proceso segun su ID: 
        
        $ sudo kill <pid>
_________________________________________________________________

## Ambiente de Producción (con Docker y Docker-Compose): 

*Alerta:* Este caso a sido probado corriendo unicamente los servicios principales (Evaluacion y Recomendaciones) + los microservicios de extracción y limpieza y los microservicios de evaluacion y recomendación asociados a imágenes. 

1. Instalación de Docker:

        $ sudo apt-get update
        $ sudo apt-get install apt-transport-https ca-certificates curl software-properties-common unzip
        $ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
        $ sudo apt-key fingerprint 0EBFCD88
        $ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
        $ sudo apt-get update
        $ sudo apt-get install docker-ce

2. Habilitar docker para su usuario de Linux:

        $ sudo usermod -aG docker $(whoami)

3. Instalación de Docker-Compose:

        $ sudo apt-get update
        $ sudo apt-get -y install python python-pip
        $ sudo pip install docker-compose

4. Construcción y despliegue de NEURONE-CS: ubicarse en directorio del codigo fuente (.../NEURONE-CS) y ejecutar: 
    *NOTA 1:* Todas las dependencias requeridas seran descargadas automaticamente. El proceso puede tardar de 5 a 30 minutos, dependiendo de la conexion a internet y la cantidad de servicios que se este levantando. 
    *NOTA 2:* Hasta aquí el servicio se puede utilizar por si solo, accediendo a traves de: http://localhost:8000/. Para utilizarlo dentro de NEURONE, se debe contruir y desplegar NEURONE. El orden en que se construyan NEURONE y NEURONE-CS no afecta su funcionamiento, y se pueden utilizar en paralelo.

        $ ./cs-start.sh

5. Para detener los servicios, ejecutar: 

        $./cs-stop.sh
_________________________________________________________________
**COMANDOS QUE PUEDEN RESULTAR UTILES EN AMBIENTE DE PRODUCCION**

1. Para listar los contenedores de docker:
        
        $ docker ps -a 

2. Para listar las imágenes creadas en docker: 
        
        $ docker images

3. Para eliminar un contenedor: 

        $ sudo docker rm <container ID>
    
4. Para eliminar una imágen (esta no debe estar siendo utilizada por ningun contenedor):

        $ sudo docker rmi <image ID>

5. Para iniciar un contenedor

        $ sudo docker start <name container>

6. Para eliminar todos los contenedores inactivos: 

        $ docker system prune -a

7. Si los archivos .sh no son reconocidos como comando, ejecutar respectivamente: 

        $ sudo chmod +x cs-start.sh
        $ sudo chmod +x cs-stop.sh
_________________________________________________________________

