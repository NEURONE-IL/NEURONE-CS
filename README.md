# NEURONE-CS: NEURONE - evaluation Service for Compatibility with screen readers

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)

Created by Polett Pizarro P.

## Description

NEURONE-CS is a service creates for the necesity in NEURONE (oNlinE inqUiRy experimentatiON 
systEm) of verify the compatibility that have the web content that upload in this platform, with screen readers software. For this, the service delivers a general detail for each of the elements that show incompatibilies.

This service, in spite of be creates pincipally for the necesity of NEURONE, can be used of independent way.

NOTE: The screen readers software is a of the settings that used principally the visually impaired or dyslexic people, to support their web browsing. 

## User Manuals

The user manual will be published soon.

## Install instruction

### Development Environment

*Note:* The use of the Linux system is highly recommended.

#### Install in Linux:

1. Install Python:

        $ sudo apt install python3

2. Install pip library: 

        $ sudo apt install python3-pip

2. Install Flask: 

        $ pip install Flask
        $ pip install -U https://github.com/pallets/flask/archive/master.tar.gz
        $ sudo apt install python3-flask
        $ sudo apt install python3-flask-restful
        $ pip3 install -U flask_cors

2. Install library for extraction (scrapping): 
        
        $ sudo apt install python3-bs4

3. Install library for traduction:

        $ sudo apt install python3-wget easy_install Flask-Babel
        $ sudo apt install python3-flask-babel

3. Install library for cleaning content: 

        $ sudo apt-get install python-lxml

#### Run in Linux: 

##### Service of Evaluations 

1. To run the main orchestrator of all the service, and in particular for evualuation services:
    1. Open console #1.
    2. Positioned in directory of source code (.../NEURONE-CS).
    3. Run:

        $ cd CS_Evaluation/Evaluation_Service
        $ python3 main.py 

2. To run all the evaluation microservices:
    *NOTE 1:* if you wish edit the up services, you comment the lines corresponding to microservices that be you wish disable in the file start-evaluations-ubuntu-local.sh, ubicated in .../NEURONE-CS/CS_Evaluation.
    *NOTE 2:* To the correct running of orchestator service, is necessary that the microservices of extraction and cleaning is active.
    1. Open console #2.
    2. Positioned in directory of source code (.../NEURONE-CS).
    3. Run:

        $ cd CS_Evaluation
        $ sudo sh start-evaluations-ubuntu-local.sh 

##### Servicio de Recomendaciones 

1. To run the orchestrator of the recomendation services:
    *NOTE:* This service need of the evaluation serviceand the microservices of extraction and cleaning for its correct operation.
    1. Open console #3.
    2. Positioned in directory of source code (.../NEURONE-CS).
    3. Run:

        $ cd CS_Recomendation/Recomendation_Service
        $ python3 main.py 

2. To run all the recomendations microservices:
    1. Open console #4.
    2. Positioned in directory of source code (.../NEURONE-CS).
    3. Run:

        $ cd CS_Recomendation
        $ sudo sh start-recomendations-ubuntu-local.sh

#### Install in Windows

1. Install Python
2. Install pip by console
        > python -m pip install --upgrade pip

3. Install library WTForms
        > pip install WTForms
        
4. Install Flask
        > pip install --user --upgrade flask-wtf

5. Install Wget
        > pip install wget

6. Install the library for extraction (scrapping):
        > pip install beautifulsoup4

7. Install library for rest-full service
        > pip install requests
        > pip install flask_restful

8. Install the required library in content cleaning: 
        > pip install lxml


#### Run in Windows

1. For Evaluation Service:
    1. Open console #1.
    2. Positioned in directory of source code (.../NEURONE-CS).
    3. Run:
        > cd CS_Evaluation
        > python make.py

2. For Recomendation Service:
    1. Open console #2.
    2. Positioned in directory of source code (.../NEURONE-CS).
    3. Run:
        > cd CS_Recomendation
        > python make.py

_________________________________________________________________
**COMMANDS THAT MAY BE USEFUL IN DEVELOPMENTAL ENVIRONMENT**

# To eliminate processes when they are active when closing the console, in development environment in Linux:
1. List the processes associated with Python, to know its PID (Process ID):
        
        $ ps -ef | grep python3

2. Delete a process according to its ID: 
        
        $ sudo kill <pid>
_________________________________________________________________

## Production Environment (with Docker and Docker-Compose): 

*Warning:* This case has been tested running only the main services (Evaluation and Recomendations) + the microservices of extractio and cleaning, and the microservices of evaluation and recomendation associated with images. 

1. Install Docker:

        $ sudo apt-get update
        $ sudo apt-get install apt-transport-https ca-certificates curl software-properties-common unzip
        $ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
        $ sudo apt-key fingerprint 0EBFCD88
        $ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
        $ sudo apt-get update
        $ sudo apt-get install docker-ce

2. Enable Docker for your current user:

        $ sudo usermod -aG docker $(whoami)

3. Install Docker-Compose:

        $ sudo apt-get update
        $ sudo apt-get -y install python python-pip
        $ sudo pip install docker-compose

4. Runfor building and deploying NEURONE-CS (from source directory .../NEURONE-CS): 
    *NOTE 1:* All the required dependencies will be downloaded automatically. The process can take from 5 to 30 minutes, depending on the internet connection and the amount of services that are being created.
    *NOTE 2:* So far the service can be used by itself, accessing through: http://localhost:8000/. To use it within NEURONE, NEURONE must be built and deployed. The order in which NEURONE and NEURONE-CS are built does not affect their operation, and they can be used in parallel.

        $ ./cs-start.sh

5. To stop the services, run: 

        $./cs-stop.sh
_________________________________________________________________
**COMMANDS THAT MAY BE USEFUL IN A PRODUCTION ENVIRONMENT**

1. To list docker containers:
        
        $ docker ps -a 

2. To list the images created in docker: 
        
        $ docker images

3. To remove a container: 

        $ sudo docker rm <container ID>
    
4. To delete an image (it must not be used by any container):

        $ sudo docker rmi <image ID>

5. To start a container

        $ sudo docker start <name container>

6. To remove all inactive containers:

        $ docker system prune -a

7. If the .sh files are not recognized as a command, execute respectively:

        $ sudo chmod +x cs-start.sh
        $ sudo chmod +x cs-stop.sh
_________________________________________________________________

