# -*- coding:utf-8 -*-
from flask import Flask, make_response, redirect, url_for, jsonify
from flask import request #para trabajar con parametros por rutas
from flask import render_template # para renderizar archivos html
from forms import UrlForm
from bs4 import BeautifulSoup
from flask_cors import CORS
from flask_babel import Babel
from flask_restful import Resource, Api
import requests
import json
import html
import re
import os
import sys

#print(sys.path)
app = Flask(__name__, template_folder = "Template")
app.secret_key = 'secret_key'
api = Api(app)
babel = Babel(app)
CORS(app)

cors = CORS(app, resources={r"/petitionEval": {"origins": "http://localhost:8000"}})
cors = CORS(app, resources={r"/ping": {"origins": "http://localhost:8000"}})
cors = CORS(app, resources={r"/": {"origins": "http://localhost:8000"}})

listMMSS =[
            {'name' : 'A', 'port': '8010'},#ok
            {'name' : 'Abbr', 'port': '8011'},#ok
            {'name' : 'Acronym', 'port': '8012'},#ok
            {'name' : 'Applet', 'port': '8013'},#ok
            {'name' : 'Area', 'port': '8014'},#ok
            {'name' : 'Audio', 'port': '8015'},#ok
            {'name' : 'Button', 'port': '8016'},#ok
            #delete{'name' : 'Caption', 'port': '8017'}, PPP: has no incompatibility
            {'name' : 'Dd', 'port': '8018'},#ok
            {'name' : 'Div', 'port': '8019'},#ok
            {'name' : 'Embed', 'port': '8020'},#ok
            #{'name' : 'Fieldset', 'port': '8021'},#ok PPP: has no incompatibility
            #delete{'name' : 'Figcaption', 'port': '8022'}, PPP: has no incompatibility
            #{'name' : 'Figure', 'port': '8023'},#ok PPP: has no incompatibility
            {'name' : 'Headings', 'port': '8024'},#ok
            #{'name' : 'Iframe', 'port': '8025'},#ok PPP: has no incompatibility
            {'name' : 'Img', 'port': '8026'},#fix
            {'name' : 'Input', 'port': '8027'},
            {'name' : 'Label', 'port': '8028'},
            #{'name' : 'Legend', 'port': '8029'}, PPP: has no incompatibility
            {'name' : 'Link', 'port': '8030'},
            #{'name' : 'Map', 'port': '8031'}, PPP: has no incompatibility
            {'name' : 'Object', 'port': '8032'},
            {'name' : 'Pre', 'port': '8033'},
            {'name' : 'Span', 'port': '8034'},
            {'name' : 'Table', 'port': '8035'},#ok
            {'name' : 'Video', 'port': '8036'}
        ]

#para definir el idioma en el cual se desplega la información en la interfaz web
@babel.localeselector
def get_locale():
    return 'en'
    #return request.accept_languages.best_match(['en', 'es', 'fi'])

#toma los resultados entregados por el microservicio y los pasa de json a variables
def response(tag, responseEval):
    if (responseEval.ok):
        respEval = json.loads(responseEval.json())
        data=respEval['data']
        resultAux = results(tag, data)
        nTags = data['totalTagsAnalyzed']
        nTagsFailed = data['totalTagsFailed']
        return nTags, nTagsFailed, resultAux;

#calcula el porcentaje de falla relativo a un tag, el "%" se agrega en el html
def results(tag, data):
    if (int(data['totalTagsAnalyzed'])>0):
        percentFailed = round(int(data['totalTagsFailed'])/int(data['totalTagsAnalyzed'])*100 , 2)
    else:
        percentFailed = 0.00
    result = {"tag":tag, 
            "evaluated": data['totalTagsAnalyzed'], 
            "failed": data['totalTagsFailed'], 
            "percent": percentFailed, 
            "positionsBadTags": data['positionsBadTags'] }
    return (result)

#función que llama a los microservicios segun las evaluaciones seleccionadas (checkbox)
#listEval = listado de evaluaciones seleccionadas
#html = codigo html
def callEvaluations(listEval, html):
    content = json.dumps({ 'html' : html})
    htmlAux = BeautifulSoup(html, "lxml")
    tagsInContent = len(htmlAux.find_all()) #para saber la cantidad total de tags

    totalTagsEvaluated = 0 #suma la cantidad total de tags evaluados
    totalTagsFailed = 0 #suma la cantidad total de los tag que al evaluarlos fallaron
    result = [] #lista de los resultados obtenidos en cada tag
    lengEval = 0 #cantidad de evaluaciones realizadas

    while (lengEval<len(listMMSS)): #listMMSS = listado de los microservicios
        if(listMMSS[lengEval]['name'] in listEval): #identifica el nombre del microservistMMSS[lengEval]['paticio
            nameEnvVar = 'MS_'+ (str(listMMSS[lengEval]['name'])).upper() + '_EVALUATION'
            #para cuando se levanta en docker
            if (nameEnvVar in os.environ): 
                envVar = str(os.environ[nameEnvVar])
                responseEval = requests.post('http://' + envVar, data = content)
            #para cuando se levanta sin docker
            else:
                responseEval = requests.post('http://localhost:' + str(listMMSS[lengEval]['port']) + '/' + str(listMMSS[lengEval]['name']).lower() + '_evaluation', data = content)
            nTags, nTagsFailed, resultAux = response(str(listMMSS[lengEval]['name']), responseEval)
            totalTagsEvaluated += nTags
            totalTagsFailed += nTagsFailed
            result.append(resultAux)
        lengEval+=1

    if(totalTagsEvaluated>0):
        finalPercent=round(totalTagsFailed/totalTagsEvaluated*100 , 2)
    else:
        finalPercent = 0.00

    result.append({'finalPercent' : finalPercent})
    result.append({'tagsInContent' : tagsInContent})
    return result

@app.route('/error', methods=['GET'])
def error():
    return redirect(url_for('index'))

@app.route('/recomendation',methods=['POST'])
def recomendation():
    data = request.form['dataResults']
    url = request.form['urlJson']
    contentA = eval(data)

    dataAux3 = json.dumps({'data' : contentA, 'url':  url})
    #PPP :With Docker
    if ('CS_RECOMENDATION' in os.environ): 
        envVar = str(os.environ['CS_RECOMENDATION'])
        responseAux = requests.post('http://' + envVar + '/petition', data = dataAux3 )
    else:
        responseAux = requests.post('http://localhost:9000/petition', data = dataAux3 )

    if (responseAux.ok):
        res = responseAux.json()
        data = res['data']
        return render_template('recomendations.html', recomendations=data)
    else: 
        return render_template('error.html')

def extraction(url_json):
    #request post realiza la solicitud y la respuesta de esta, es guardada en responseExtraction
    #PPP: With Docker
    if ('MS_HTML_EXTRACTION' in os.environ): 
        envVar = str(os.environ['MS_HTML_EXTRACTION'])
        responseExtraction = requests.post('http://' + envVar, data = url_json )
    else:
        responseExtraction = requests.post('http://localhost:8001/html_extraction', data = url_json)

    if (responseExtraction.ok):
        #extraccion de respuesta json correspondiente a la petición, en formato str
        respExtraction= json.loads(responseExtraction.json())
        if (respExtraction["status"] != "error" ):
            #traspaso del codigo de contenido html de la extraccion para la limpieza.
            contentBase= json.dumps({ 'html' : respExtraction['data'] })
            return 1, contentBase
        else:
            print ("La extracción presentó un error")
            print (respExtraction['status'])
            return 0, respExtraction['status']

def cleaning(contentBase):
    #PPP: With Docker
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

def core(url):
    #PPP: json.dumps gives format JSON to the parameters 
    url_json = json.dumps({'url' : str(url)})

    statusE, contentBase = extraction(url_json)
    if (statusE == 1): #PPP: 1 = without errors and data have info
        return cleaning(contentBase)
    else:
        return 0, []

#función que llama a los microservicios segun las evaluaciones seleccionadas (checkbox)
#function that invoke the microservices selected in checkboxs in the web
def activeServices():
    #list of results associated to each tag
    #lista de los resultados obtenidos en cada tag
    result = [] 

    #quantity of evaluations carried out
    #cantidad de evaluaciones realizadas
    lengEval = 0 

    #listMMSS = listado de los nombres y puertos de cada microservicios
    #listMMSS = list of ports and name's each microservice
    while (lengEval<len(listMMSS)): 
        name = str(listMMSS[lengEval]['name'])
        nameEnvVar = 'MS_'+ name.upper() + '_EVALUATION'
        #PPP: With docker
        port = (str(listMMSS[lengEval]['port'])) + '/ping'
        if (nameEnvVar in os.environ): 
            url = 'http://ms_' + str(name.lower()) + '_evaluation:' 
        #PPP: Without docker
        else:
            url = 'http://localhost:'
        completeURL = url + port
        try:
            response = requests.get(completeURL)
            if (response.ok):
                result.append(('name', name))
        except requests.exceptions.RequestException as e:
            print ("Error")
        lengEval+=1
    return result

@app.route('/', methods = ['GET', 'POST'])
def index():
    #PPP: brings the form for the URL
    #PPP: trae el formulario correspondiente a la url.
    urlForm = UrlForm(request.form)

    if request.method == 'POST':
        if urlForm.validate():
            #PPP: extraction the content associated this url
            #PPP: se extrae la url contenida en el campo input del formulario
            url = urlForm.url.data
            status, data = core(url)
            if (status == 1):#PPP: 1 = without errors and data have info
                aux = request.form
                results = callEvaluations(aux, data)
                #PPP: "pop" extract, removing from the list, the last element
                #PPP: "pop" extrae (lo elimina de la lista) el ultimo elemento
                tagsInContent = results.pop()['tagsInContent']
                percentFinalFailed = results.pop()['finalPercent']
                return render_template('result.html', percentFinalFailed = percentFinalFailed, tagsInContent = tagsInContent, results = results, url = url)
            else:
                return render_template('error.html')
    else :
        return render_template('index.html', form = urlForm, option_list=activeServices() )

#@app.route('/petitionEval', methods = ['POST']) # option 1
class PetitionEval(Resource):
    def post(self):
        try:
            jsonData = request.get_json(force=True)
            url = jsonData['url']

            #data corresponde al codigo html de la pagina.
            status, data = core(url)
            if (status == 1):#1 = sin errores y data tiene results
                results = callEvaluations(jsonData['data'], data)
                results.append({'url' : url})
                status = 200
                #results.append({'html' : data})
            else:
                results = data
                status = 500

            response = app.response_class(
                response=json.dumps({'data' : results}),
                status=status,
                mimetype='application/json'
            )
            #response = json.dumps({'status': 'success', 'data': results})
            return response
        except requests.exceptions.RequestException as e:
            response = app.response_class(
                response=json.dumps({'data' : str(e)}),
                status=e.code,
                mimetype='application/json'
            )
            return response

api.add_resource(PetitionEval, '/petitionEval') #option 2, PPP: to assign a url, you can do it in these two ways

#@app.route('/petitionRecom', methods = ['POST'])
class PetitionRecom(Resource):
    def post(self):
        try:
            jsonData = request.get_json(force=True)
            url = jsonData['url']
            data = jsonData['data']
            dataAux = json.dumps({'data' : data, 'url':  url})
            #With docker
            if ('CS_RECOMENDATION' in os.environ): 
                envVar = str(os.environ['CS_RECOMENDATION'])
                responseAux = requests.post('http://' + envVar + '/petition', data = dataAux )
            else:
                responseAux = requests.post('http://localhost:9000/petition', data = dataAux )
            
            if (responseAux.ok):
                res = responseAux.json()
                data = res['data']
                results = data
                status = 200

            else:
                results = "error"
                status = 500

            response = app.response_class(
                response=json.dumps({'data' : results}),
                status=status,
                mimetype='application/json'
            )
            return response
        except requests.exceptions.RequestException as e:
            response = app.response_class(
                response=json.dumps({'data' : str(e)}),
                status=e.code,
                mimetype='application/json'
            )
            return response

api.add_resource(PetitionRecom, '/petitionRecom')

class Ping(Resource):
    def get(self):
        try:
            evalActives = activeServices()
            response = {'status': 'success', 'validations': evalActives}
            return response
        except IntegrityError:
            return {"status":"Error"}

api.add_resource(Ping, '/ping')

if __name__ == '__main__':
	app.run(debug = True, host='0.0.0.0', port=8000) 
    #PPP: 0.0.0.0:so that the server listens to the requests coming from any IP
    #PPP: 0.0.0.0: para que el servidor escuche las peticiones provenientes de cualquier IP
    
    #PPP: if port is not defined, by default it will be 5000
    #PPP: si no se define port, por defecto sera el 5000
    
    #PPP: debug = True is for flask to enter debug mode, default is False, for docker (which is a production environment) it must be False
    #PPP: debug = True es para que flask entre en modo de depración, por defecto es False, para docker que es ambiente de producción debe ser False.
