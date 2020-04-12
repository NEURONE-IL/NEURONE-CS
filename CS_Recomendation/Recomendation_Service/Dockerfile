FROM python:3

# Contacto de persona encargada de esta imagen:
MAINTAINER Polett Pizarro "<polett.pizarro.p@gmail.com>"

#dependencias básicas
RUN apt-get update -y
RUN apt-get install -y python3-dev python3-pip python3-flask

RUN mkdir /recomendation_service
WORKDIR /recomendation_service

#en: copy source code
#es: copia del código fuente
COPY . /recomendation_service

#instalación de bibliotecas utilizadas por los servicios
RUN pip install beautifulsoup4 flask-restful requests wget wtforms lxml flask-babel

#comandos para ejecutar servicio
ENTRYPOINT ["python3"]
CMD ["main.py"]
