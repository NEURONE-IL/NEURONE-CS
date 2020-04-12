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

def evaluateAudio(contentJson):
	contentBase= BeautifulSoup(contentJson, "lxml")
	badTags = []
	audios = contentBase.find_all('audio')
	totalQuantity = len(audios)

	failed = 0
	good = 0
	badTags = []
	flag = 0
	numId = -1

	for audio in audios:
		numId += 1
		audioAttrAriaLab = audio.get('aria-label')
		audioAttrAriaLabBy = audio.get('aria-labelledby')
		audioAttrTitle = audio.get('title')
		audioPlaceholder = audio.text

		if (audioPlaceholder):
			audioPlaceholder = re.sub(r"[ \t\n\x0B\f\r]", '', audioPlaceholder, flags=0)

		#si <AUDIO> tiene ARIA-LABEL  -100%
		#si <AUDIO> tiene ARIA-LABELLEDBY  - 100%
		#si <AUDIO> tiene TITLE  - 100%
		#si <AUDIO> tiene contenido de apoyo - 100% 
		'''^creo que esto esta mal traducido, en vez de contenido de apoyo 
		creo que se refiere a formatos alternativos, 
		es decir etiqueta source dentro de etiqueta audio :s '''
		#si <AUDIO> no tiene descripcion - 100%
		if (audioAttrAriaLab or audioAttrAriaLabBy or audioAttrTitle or audioPlaceholder or not audioPlaceholder):
			flag = 1
			typeError = 1
		else:
			#no debería ocurrir

		if (flag == 1):
			failed += 1
			pos = position(contentBase, audio)
			pos.append(numId)
			pos.append(typeError)
			badTags.append(pos)
			flag = 0

	dataResponse ={
		'tag': 'audio',
		'totalTagsAnalyzed': totalQuantity,
		'totalTagsFailed': totalQuantity,
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
					response = evaluateAudio(json_data[key])
			return response
		except requests.exceptions.RequestException as e:
			return ("error")

api.add_resource(Petition, '/audio_evaluation')

class Ping(Resource):
    def get(self):
        try:
            return {'status': 'success'}
        except requests.exceptions.RequestException as e:
            return {"status":"Error"}

api.add_resource(Ping, '/ping')

if __name__ == '__main__':
	app.run( debug = False, host='0.0.0.0' , port=8015)
