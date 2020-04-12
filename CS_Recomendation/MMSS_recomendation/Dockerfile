FROM python:3

# Contacto de persona encargada de esta imagen:
MAINTAINER Polett Pizarro "<polett.pizarro.p@gmail.com>"

#dependencias básicas
RUN apt-get update -y
RUN apt-get install -y python3-dev python3-pip python3-flask

RUN mkdir /mss_recomendations
WORKDIR /mss_recomendations

COPY . /mss_recomendations

#instalación de bibliotecas utilizadas por los servicios
RUN pip install beautifulsoup4 flask-restful requests lxml flask-babel 