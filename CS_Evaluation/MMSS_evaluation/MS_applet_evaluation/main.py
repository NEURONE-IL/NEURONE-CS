from flask import Flask
from flask import request #para trabajar con parametros por rutas
from bs4 import BeautifulSoup
from flask_restful import Resource, Api
import requests
import json
import warnings
import re

#ppp: re.sub launches the DeprecationWarning, I can not identify the reason. For this reason, this line is added.
warnings.filterwarnings("ignore", category=DeprecationWarning)

app = Flask(__name__)
app.secret_key = 'html_secret_key'
api = Api(app)

def evaluateApplet(contentJson):
	contentBase= BeautifulSoup(contentJson, "lxml")

	applets = contentBase.find_all('applet')
	totalQuantity = len(applets)

	failed = 0
	good = 0
	badTags = []
	flag = 0
	numId = -1

	for applet in applets:
		numId += 1
		appletAttrAriaLabBy = applet.get('aria-labelledby')
		appletAttrAriaLab = applet.get('aria-label')
		appletAttrTitle = applet.get('title')
		appletAttrAlt = applet.get('alt')
		parent = BeautifulSoup(str(applet.parent), 'lxml')
		appletNameParent = applet.parent.name
		appletPlaceholder = applet.text

		if (appletPlaceholder):
			appletPlaceholder = re.sub(r"[ \t\n\x0B\f\r]", '', appletPlaceholder, flags=0)

		#verificar si <applet> tiene atributo aria-label - 75%
		#verificar si <applet> tiene contenido alternativo - 50%
		if (appletAttrAriaLab or appletPlaceholder ):
			good += 1

		#verificar si <applet> esta dentro de un <figure>, junto con <figcaption> - 25%
		elif (appletNameParent == "figure" and parent.find("figcaption")):
			good += 1

		#si <applet> tiene atributo aria-labelledby - 100%
		elif(appletAttrAriaLabBy):
			flag = 1
			typeError = 1

		#si <applet> con atributo alt - 100%
		#si <applet> con atributo title - 100%
		#si <applet> sin descripcion - 100%
		elif (appletAttrAlt or appletAttrTitle or not appletPlaceholder):
			flag = 1
			typeError = 1 #debe utilizar una descripción y no utilizar los atributos "alt" ni "title" dentro del applet

		else:
			# no denería ocurrir
		if (flag == 1):
			failed += 1
			pos = position(contentBase, applet)
			pos.append(numId)
			pos.append(typeError)
			badTags.append(pos)
			flag = 0

	dataResponse ={
		'tag' : 'applet',
		'totalTagsAnalyzed': totalQuantity,
		'totalTagsFailed': failed,
		'positionsBadTags': badTags
	}
	response = json.dumps({'status': 'success', 'data': dataResponse})
	return response

def position(contentBase, tag):
	contentStr = str(contentBase) #no funciona con contentBase.prettify() !!!
	lenContent = len(contentStr)

	tagStr = str(tag)
	lenTag = len(tagStr)

	start = contentStr.find(tagStr)

	startPosition=0
	flagAux=0
	listAux = []
	badTags = []

	while(startPosition<lenContent and flagAux==0):
		start = contentStr.find(tagStr,startPosition)
		if(start in listAux):
			if (startPosition == start):
				flagAux = 1
			else:
				startPosition = start
		else:
			positionTuple = []
			listAux.append(start)
			positionTuple.append(start)
			positionTuple.append(start+len(tagStr))
			startPosition = start
			badTags.append(positionTuple)
	return badTags


class Petition(Resource):
	def post(self):
		response = {}
		try:
			json_data = request.get_json(force=True)
			for key in json_data:
				if (key == 'html'):
					#funcion que extrae el codigo html
					response = evaluateApplet(json_data[key])
			return response
		except requests.exceptions.RequestException as e:
			return ("error")

api.add_resource(Petition, '/applet_evaluation')

class Ping(Resource):
    def get(self):
        try:
            return {'status': 'success'}
        except requests.exceptions.RequestException as e:
            return {"status":"Error"}

api.add_resource(Ping, '/ping')

if __name__ == '__main__':
	app.run( debug = False, host='0.0.0.0', port=8013)
