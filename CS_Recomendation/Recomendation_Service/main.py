# -*- coding:utf-8 -*-
from flask import Flask, make_response, url_for, redirect
from flask import request #para trabajar con parametros por rutas
from flask import render_template # para renderizar archivos html
from flask_restful import Resource, Api
from flask_babel import Babel, gettext
from bs4 import BeautifulSoup
import requests
import json
import html
import re
import os
import webbrowser

app = Flask(__name__, template_folder = "Template")
app.secret_key = 'secret_key'
api = Api(app)
babel = Babel(app)

listMMSS =[
            {'name' : 'A', 'port' : '9010'},
            {'name' : 'Abbr', 'port' : '9011'},
            {'name' : 'Acronym', 'port' : '9012'},
            {'name' : 'Applet', 'port' : '9013'},
            {'name' : 'Area', 'port' : '9014'},
            {'name' : 'Audio', 'port' : '9015'},
            {'name' : 'Button', 'port' : '9016'},
            #{'name' : 'Caption', 'port' : '9017'},
            {'name' : 'Dd', 'port' : '9018'},
            {'name' : 'Div', 'port' : '9019'},
            {'name' : 'Embed', 'port' : '9020'},
            #{'name' : 'Fieldset', 'port' : '9021'},
            #{'name' : 'Figcaption', 'port' : '9022'},
            #{'name' : 'Figure', 'port' : '9023'},
            {'name' : 'Headings', 'port' : '9024'},
            #{'name' : 'Iframe', 'port' : '9025'},
            {'name' : 'Img', 'port' : '9026'},
            {'name' : 'Input', 'port' : '9027'},
            {'name' : 'Label', 'port' : '9028'},
            #{'name' : 'Legend', 'port' : '9029'},
            {'name' : 'Link', 'port' : '9030'},
            #{'name' : 'Map', 'port' : '9031'},
            {'name' : 'Object', 'port' : '9032'},
            {'name' : 'Pre', 'port' : '9033'},
            {'name' : 'Span', 'port' : '9034'},
            {'name' : 'Table', 'port' : '9035'},
            {'name' : 'Video', 'port' : '9036'}
        ]

#para definir el lenguaje en el cual se desplega la información en la interfaz web
@babel.localeselector
def get_locale():
    return 'en'
    #return request.accept_languages.best_match(['en', 'es', 'fi'])
    
#función que llama a los microservicios segun las recomendaciones seleccionadas (checkbox)
#listRecom = listado de recomendaciones seleccionadas
#html = codigo html correspondiente al contenido analizado.
def callRecomendations(html, badResults, goodResults):
    tagsBad = {}
    tagsGood = {}
    contB = 0
    contG = 0
    result = [] #lista de los resultados obtenidos en cada tag

    for bad in badResults:
        get = bad.get('tag')
        tagsBad[get] = contB #le asigna como id el contador
        contB += 1

    for good in goodResults:
        get = good.get('tag')
        tagsGood[get] = contG #le asigna como id el contador
        contG += 1
    
    for ms in listMMSS:
        if (ms['name'] in tagsBad):
            idBad = tagsBad.get(ms['name'])
            content = json.dumps({ 'html' : html, 'badResults': list(badResults)[idBad]})
            nameEnvVar = 'MS_'+ (str(ms['name'])).upper() + '_RECOMENDATION'
            #para cuando se levanta en docker
            if (nameEnvVar in os.environ): 
                envVar = str(os.environ[nameEnvVar])
                responseRecom = requests.post('http://' + envVar, data = content)
                auxRes = json.loads(responseRecom.json())
            #para cuando se levanta sin docker
            else:
                responseRecom = requests.post('http://localhost' + str(ms['port']) + '/' + str(ms['name']), data = content)
                auxRes = json.loads(responseRecom.json())
            result.append(auxRes["data"])
        elif (ms['name'] in tagsGood):
            auxRes = {'tag': str(ms['name']), 'recomendations': [{'recomendation': 'No incompatibilities associated with this tag were detected.'}]}
            result.append(auxRes)
        #else:
            #no se evaluó
        
    return result

#funcion que extraccion el contenido, es replica del servicio de evaluación. y llama al ms de extraccion de cs_evaluation
def extraction(url):
    #request.post realiza la solicitud y la respuesta de esta es guardada en responseExtraction
    
    #para cuando se levanta en docker
    if ('MS_HTML_EXTRACTION' in os.environ): 
        envVar = str(os.environ['MS_HTML_EXTRACTION'])
        responseExtraction = requests.post('http://' + envVar, data = json.dumps({'url' : str(url)}))
    else:
        responseExtraction = requests.post('http://localhost:8001/html_extraction', data = json.dumps({'url' : str(url)}))

    if (responseExtraction.ok):
        #extraccion de respuesta Een json correspondiente a la petición, en formato str
        respExtraction= json.loads(responseExtraction.json())
        if (respExtraction["status"] != "error" ):
            #traspaso del codigo deL contenido html de la extraccion para la limpieza.
            contentBase= json.dumps({ 'html' : respExtraction['data'] })
            return 1, contentBase
        else:
            print ("la extracción presentó un error")
            print (respExtraction['status'])
            return 0, respExtraction['status']        
    else:
        print ("la extracción presentó un error")
        print (respExtraction['status'])
        return 0, respExtraction['status'] 

#funcion que limpia el contenido, es replica del servicio de evaluación. y llama al ms de limpieza de cs_evaluation
def cleaning(contentBase):
     #para cuando se levanta en docker
    if ('MS_HTML_CLEANING' in os.environ): 
        envVar = str(os.environ['MS_HTML_CLEANING'])
        responseCleaning = requests.post('http://' + envVar, data = contentBase )
    else:
        responseCleaning = requests.post('http://localhost:8002/html_cleaning', data = contentBase)
    if (responseCleaning.ok):
        respCleaning = json.loads(responseCleaning.json())
        if (respCleaning["status"] != "error"):
            return 1, respCleaning['data']
        else:
            print ("la limpieza presentó un error")
            print (respCleaning['status'])
            return 0, respCleaning['status']

#funcion orquestadora, toma la data de la petición del json para llamar a las funciones de forma ordenada.
def core(resultsRecom):
    url = resultsRecom['url']
    data = resultsRecom['data']
    badResults = []
    goodResults = []
    for result in data:
        failed = result.get('failed')
        if (failed>0):
            badResults.append(result)
        else:
            goodResults.append(result)

    if (len(badResults)>0):
        statusE, contentBase = extraction(url)
        if (statusE == 1): #1 = sin errores y por tanto, data tiene data
            statusC, html = cleaning(contentBase)
            return statusC, html, badResults, goodResults
        else:

            return 0, "no data", badResults, goodResults
    else: 
        return 1, "no data", badResults, goodResults


def activeServices():
    result = [] #lista de los resultados obtenidos en cada tag
    lengEval = 0 #cantidad de evaluaciones realizadas

    while (lengEval<len(listMMSS)): #listMMSS = listado de los microservicios
        name = str(listMMSS[lengEval]['name'])
        nameEnvVar = 'MS_'+ name.upper() + '_RECOMENDATION'
        #para cuando se levanta en docker
        port = (str(listMMSS[lengEval]['port'])) + '/ping'
        if (nameEnvVar in os.environ): 
            url = 'http://ms_' + str(name.lower()) + '_recomendation:' 
        #para cuando se levanta sin docker
        else:
            url = 'http://localhost:'
        completeURL = url + port
        try:
            response = requests.get(completeURL)
            if (response.ok):
                result.append(('name', name))
        except requests.exceptions.RequestException as e:
            print ("Error")
            print (e)
        lengEval+=1
    return result

#muestra en el navegador si el servicio se encuentra activo.
@app.route('/')
def index():
    return "<h1> El servicio de recomendaciones esta funcionando </h1>"

#recibe la petición realizada desde el servicio de evaluación, o un cliente externo.
class Petition(Resource):
    def post(self):
        try: 
            dataResponse = {}
            jd = request.get_json(force=True)
            status, html, badResults, goodResults = core(jd)
            if (status == 1):#1 = sin errores, y html tiene data
                dataResponse = callRecomendations(html, badResults, goodResults)
                status = 200
            else:
                status = 500

            response = app.response_class(
                response=json.dumps({'data' : list(dataResponse)}),
                status=status,
                mimetype='application/json'
            )
            return response

        except requests.exceptions.RequestException as e: 
            response = app.response_class(
                status=e.code,
                mimetype='application/json'
            )
            return 'error'

#crea la ruta /petition y la asocia a funcion Petition 
api.add_resource(Petition, '/petition')

#funcion que pemite al cliente externo conocer los servicios activos. 
class Ping(Resource):
    def get(self):
        try: 
            recomActives = activeServices()
            response = {'status': 'success', 'recomendations': recomActives}
            return response
        except requests.exceptions.RequestException as e:
            return {"status":"Error"}

#crea la ruta /ping y la asocia a funcion Ping 
api.add_resource(Ping, '/ping')

if __name__ == '__main__':
	app.run(debug = True, host='0.0.0.0', port=9000)