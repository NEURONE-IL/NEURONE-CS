from flask import Flask
from flask import request #para trabajar con parametros por rutas
from bs4 import BeautifulSoup
from flask_restful import Resource, Api
import requests
import json
import warnings

#ppp: re.sub launches the DeprecationWarning, I can not identify the reason. For this reason, this line is added.
warnings.filterwarnings("ignore", category=DeprecationWarning)

app = Flask(__name__)
app.secret_key = 'html_secret_key'
api = Api(app)

def evaluateButton(contentJson):
	contentBase= BeautifulSoup(contentJson, "lxml")

	buttons = contentBase.find_all('button')
	totalQuantity = len(buttons)

	failed = 0
	good = 0
	badTags = []
	flag = 0
	numId = -1

	for button in buttons:
		numId += 1
		buttonAttrTitle = button.get('title')
		buttonAttrAriaLab = button.get('aria-label')
		nextAux = button.findNext()
		nextImg = BeautifulSoup(str(nextAux), 'lxml').find_all('img')

		if (len(nextImg)==1):
			nextImgAlt = nextImg[0].get('alt')
			nextImgTitle = nextImg[0].get('title')
			nextImgAriaLab = nextImg[0].get('aria-label')
			nextImgAriaLabBy = nextImg[0].get('aria-labelledby')
			#BUTTON contiene solo una *(IMG con atributo TITLE) - 50%
			#BUTTON contiene solo una *(IMG con aria-label) - 25%
			#BUTTON contiene solo una *(IMG con aria-labelledby) - 50%
			#elemento `button` contiene solo una `img` con atributo `alt` - 25%
			if (nextImgTitle or nextImgAriaLab or nextImgAriaLabBy or nextImgAlt):
				good += 1
			elif (nextImgAlt == ''):
				#BUTTON con TITLE, contiene solo una IMG con ALT null- 0%
				#BUTTON con aria-label, contiene solo una IMG con ALT null- 25%
				if (buttonAttrTitle or buttonAttrAriaLab):
					good += 1
				#BUTTON contiene solo una IMG con atributo ALT null - 100%
				else:
					flag = 1
					typeError = 1
			elif (not nextImgAlt):
				#BUTTON con TITLE, contiene solo una IMG sinF ALT - 25%
				#BUTTON con aria-label contiene solo una IMG sin ALT - 25%
				if (buttonAttrTitle or buttonAttrAriaLab):
					good += 1
				#BUTTON contiene solo una IMG sin ALT - 100%
				else:
					flag = 1
					typeError = 1

		if (flag == 1):
				failed += 1
				pos = position(contentBase, button)
				pos.append(numId)
				pos.append(typeError)
				badTags.append(pos)
				flag = 0

	dataResponse ={
		'tag' : 'button',
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
					response = evaluateButton(json_data[key])
			return response
		except requests.exceptions.RequestException as e:
			return ("error")

api.add_resource(Petition, '/button_evaluation')

class Ping(Resource):
    def get(self):
        try:
            return {'status': 'success'}
        except requests.exceptions.RequestException as e:
            return {"status":"Error"}

api.add_resource(Ping, '/ping')

if __name__ == '__main__':
	app.run( debug = False, host='0.0.0.0' , port=8016)
