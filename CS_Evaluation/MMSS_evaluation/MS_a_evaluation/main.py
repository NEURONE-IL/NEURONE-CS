# coding:utf-8
from flask import Flask
from flask import request #para trabajar con parametros por rutas
from bs4 import BeautifulSoup
from flask_restful import Resource, Api
import requests
import json
import re
import warnings

#ppp: re.sub launches the DeprecationWarning, I can not identify the reason. For this reason, this line is added.
warnings.filterwarnings("ignore", category=DeprecationWarning)

app = Flask(__name__)
app.secret_key = 'html_secret_key'
api = Api(app)


def evaluateA(contentJson):
	contentBase= BeautifulSoup(contentJson, "lxml")
	links = contentBase.find_all('a')
	totalQuantity = len(links)
	failed = 0
	good = 0
	badTags = []
	flag = 0
	numId = -1

	for link in links:
		aAttrAriaLabBy = link.get('aria-labelledby')
		aAttrTitle = link.get('title')
		aAttrAriaLab = link.get('aria-label')
		aAttrHref = link.get('href')
		aAttrOnclick = link.get('onclick')
		aAttrEvent = link.get('event')
		aAttrTarget = link.get('target')

		aPlaceholder = link.string #placeholder = label
		if (aPlaceholder):
			labelSpaces = re.sub(r"[ \t\n\x0B\f\r]", '', aPlaceholder, flags=0)

		aNext = link.findNext()
		img = BeautifulSoup(str(aNext), 'lxml').find('img')

		numId += 1
		#verificar que <a> contiene solo una IMG con atributo alt
		#verificar que <a> contiene solo una IMG con atributo title
		#verificar si <a> tiene aria-label y contiene solo una imagen (img) sin alt
		if ((aNext != None) and (aNext == img ) and (aNext.parent.name == "a")): #verificar que <a> contiene solo una IMG...
			imgAttrAlt = img.get('alt') #con atributo alt
			imgAttrTitle = img.get('title') #con atributo title

			#verificar si <a> tiene TITLE y contiene solo una imagen (IMG) sin Alt
			if (aAttrTitle and not imgAttrAlt):
				good += 1

			#este error no corresponde aqui. 
			#si <a> contiene solo una imagen con alt nulo - 100%
			#si <a> contiene solo una imagen sin alt - 100%
			elif((imgAttrAlt == "") or (not imgAttrAlt)):
				flag = 1
				typeError = 1

			elif(imgAttrAlt or imgAttrTitle):
				good += 1

			#verificar si <a> tiene aria-labelledby y contiene solo una imagen (IMG) sin alt
			elif (not imgAttrAlt):
				if (aAttrAriaLabBy or aAttrAriaLab):
					good += 1

		#verificar que <a> tenga titulo
		#**!!!VERIFICAR EL FUNCIONAMIENTO DE ESTO  #verificar que <a> tenga aria-describedby
		#verificar si hay fieldset con <a>s
		#verificar si <a> tiene aria-label
		#vericar si <a> tiene label vacio (<a>null</a>)
		elif (aAttrTitle or aAttrAriaLabBy or (link.parent.name == "fieldset") or aAttrAriaLab or not aPlaceholder):
			good += 1

		elif(aAttrOnclick and not aAttrHref ): #verificar si <a> tiene onclick pero no href
			good += 1

		#VERIFICAR LOS EVENTHANDLER
		elif(aPlaceholder):
			#si <a> tiene como etiqueta un espacio - 100%
			labelSpaces = re.sub(r"[ \t\n\x0B\f\r]", '', aPlaceholder, flags=0)
			if (labelSpaces == ""):
				flag = 1
				typeError = 2
			#verificar si se define un <a> con placeholder y sin href o event handler
			elif (not aAttrHref or not aAttrOnclick or not aAttrEvent):
				good += 1

		#**!!!VERIFICAR EL FUNCIONAMIENTO DE ESTO  #si <a> se abre en una nueva ventana por un TARGET - 100%
		elif (aAttrTarget):
			flag = 1
			typeError = 3

		else:
			# no debería ocurrir 
			
		if (flag == 1):
			failed += 1
			pos = position(contentBase, link)
			pos.append(numId)
			pos.append(typeError)
			badTags.append(pos)
			flag = 0

	dataResponse ={
		'tag' : 'a',
		'totalTagsAnalyzed': totalQuantity,
		'totalTagsFailed': failed,
		'positionsBadTags': badTags
	}

	response = json.dumps({'status': 'success', 'data': dataResponse})
	return response

def position(contentBase, tag):
	contentStr = str(contentBase) #no funciona con contentBase.prettify() !!! o.o
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
					response = evaluateA(json_data[key])
			return response
		except requests.exceptions.RequestException as e:
			return json.dumps({'status': 'error', 'data': response})

api.add_resource(Petition, '/a_evaluation')

class Ping(Resource):
    def get(self):
        try:
            return {'status': 'success'}
        except requests.exceptions.RequestException as e:
            return {"status":"Error"}

api.add_resource(Ping, '/ping')

if __name__ == '__main__':
	app.run( debug = False, host='0.0.0.0', port=8010)
