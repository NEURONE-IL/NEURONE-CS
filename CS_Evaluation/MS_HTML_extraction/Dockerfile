FROM python:3

# Contacto de persona encargada de esta imagen:
MAINTAINER Polett Pizarro "<polett.pizarro.p@gmail.com>"

#dependencias básicas
RUN apt-get update -y
RUN apt-get install -y python3-dev python3-pip python3-flask

RUN mkdir /ms_html_extraction
WORKDIR /ms_html_extraction

#en: copy source code
#es: copia del código fuente
COPY . /ms_html_extraction

#instalación de bibliotecas utilizadas por los servicios
RUN pip install beautifulsoup4 flask-restful requests wget lxml

EXPOSE 8001

#comandos para ejecutar servicio
ENTRYPOINT ["python3"]
CMD ["main.py"]
