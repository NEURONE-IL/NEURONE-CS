from flask import Flask
from flask import request #para trabajar con parametros por rutas
from bs4 import BeautifulSoup
from flask_restful import Resource, Api
import requests
import json
import warnings

#### ppp: ESTE SERVICIO NO SE EJECUTA

#ppp: re.sub launches the DeprecationWarning, I can not identify the reason. For this reason, this line is added.
warnings.filterwarnings("ignore", category=DeprecationWarning) 

app = Flask(__name__)
app.secret_key = 'html_secret_key'
api = Api(app) 

def recomFigcaption(contentJson, badEvaluations):
	contentBase= BeautifulSoup(contentJson, "lxml") 
	
	images = contentBase.find_all('figcaption')
	badEvalsPos = badEvaluations.get('positionsBadTags')

	recomendations = []
	count = 0
	lenEvals=len(badEvalsPos)
	messages = {}
	messages[0] = "No se detectaron incompatibilidades correspondientes a este tag."
	#Tipo de incompatibilidad 1:
	messages[1] = "tipo incompatibilidad 1"

	if (lenEvals == 0):
		recomendations.append({'recomendation' : messages.get(0)})
	else :
		while count<lenEvals:
			message=messages.get((badEvalsPos[count][2]))
			recomendations.append({'element' : str(images[badEvalsPos[count][1]]), 'recomendation' : message})
			count += 1

	dataResponse ={
		'tag' : 'figcaption',
		'recomendations': recomendations
	}
	response = json.dumps({'status': 'success', 'data': dataResponse})
	return response

	
class Petition(Resource):
	def post(self):
        response = {}
        try: 
          json_data = request.get_json(force=True)
          response = recomFigcaption(json_data['html'], json_data['badResults']) 
          return response
        except requests.exceptions.RequestException as e: 
          return ("error")

api.add_resource(Petition, '/figcaption_recomendation')

class Ping(Resource):
    def get(self):
        try:
            return {'status': 'success'}
        except requests.exceptions.RequestException as e:
            return {"status":"Error"}

api.add_resource(Ping, '/ping')

if __name__ == '__main__':
	app.run( debug = False, host='0.0.0.0', port=9022)