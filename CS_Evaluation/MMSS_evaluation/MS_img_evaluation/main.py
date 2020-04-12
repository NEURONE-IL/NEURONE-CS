from flask import Flask
from flask import request #para trabajar con parametros por rutas
from bs4 import BeautifulSoup
from flask_restful import Resource, Api
import requests
import re
import json
import warnings

#ppp: re.sub launches the DeprecationWarning, I can not identify the reason. For this reason, this line is added.
warnings.filterwarnings("ignore", category=DeprecationWarning)

app = Flask(__name__)
app.secret_key = 'html_secret_key'
api = Api(app)


def evaluateImgs(contentJson):
	contentBase= BeautifulSoup(contentJson, "lxml")

	images = contentBase.find_all('img')
	totalQuantity = len(images)

	failed = 0
	good = 0
	badTags = []
	flag = 0
	numId = -1

	for image in images:
		numId += 1
		imgAttrAlt = image.get('alt')
		imgAttrIsMap = image.get('ismap')
		imgAttrTitle = image.get('title')
		imgAttrFileName = image.get('src')
		imgAttrAriaLab = image.get('aria-label')
		imgAttrAriaLabBy = image.get('aria-labelledby')
		imgAttrAriaDescby = image.get('aria-describedby')

		next1 = image.findNext()
		next1Map = BeautifulSoup(str(next1), 'lxml').find('map')
		next1Figcap = BeautifulSoup(str(next1), 'lxml').find('figcaption')

		#LINK
		if (image.parent.name == "a"):
			#*A link contiene solo una IMG con ALT null - 100%
			if(imgAttrAlt ==""):
				flag = 1
				typeError = 1 
			#*A link contiene solo una IMG sin ALT - 100% !!!!!!!!!!!!!!!!!ARREGLAR!!!!!!!!!!!!!!!!!!
			#*A link con aria-labelledby contiene solo una IMG sin ALT - 50% //if(!imgAttrAlt)
			#*A link contiene solo una *(IMG con ALT) 0% //if(imgAttrAlt)
			#*A link con TITLE contiene solo una IMG sin ALT - 25% //if(!imgAttrAlt)
			#*A link contiene solo una *(IMG con TITLE) - 0%
			elif(imgAttrTitle or not imgAttrAlt):
				good += 1

		#*AREA
		elif (next1Map):
			next2 = next1Map.findNext()
			next2Area = BeautifulSoup(str(next2), 'lxml').find_all('area')
			for area in next2Area:
				next2AreaAlt = area.get('alt')
				#*AREA y *(IMG con ALT) attributes - 50% //if(imgAttrAlt)
				#*AREA con ALT attribute y IMG con ALT null - 25% //if(imgAttrAlt == '')
				if (next2AreaAlt):
					good += 1

		#*BUTTON
		elif (image.parent.name == "button"):
			#*BUTTON con TITLE contiene solo una IMG con ALT null - 0%
			#*BUTTON con TITLE contiene solo una IMG sin ALT - 25%
			if (image.parent.get('title') and (imgAttrAlt=='' or not imgAttrAlt)):
				good += 1
			#*BUTTON con aria-label contiene solo una IMG con ALT null - 25%
			#*BUTTON con aria-label contiene solo una IMG sin ALT - 25%
			elif (image.parent.get('aria-label') and (imgAttrAlt=='' or not imgAttrAlt)):
				good += 1
			#*BUTTON contiene solo una IMG sin ALT - 100%
			#*BUTTON contiene solo una IMG con ALT null attribute - 100%
			elif (imgAttrAlt =='' or not imgAttrAlt):
				flag = 1
				typeError = 1
			#BUTTON contiene solo una IMG con TITLE attribute - 50%
			#*BUTTON contiene solo una IMG con aria-label - 25%
			#*BUTTON contiene solo una IMG con aria-labelledby - 50%
			elif(imgAttrTitle or imgAttrAriaLab or imgAttrAriaLabBy):
				good += 1
			#*`button` element contiene solo una `img` con `alt` attribute - 25%
			elif (imgAttrAlt != ""):
				good += 1

		elif (image.parent.name == ("h1" or "h2" or "h3" or "h4" or "h5" or "h6")):
			#*Heading is IMG ALT="" - 100%
			#*Heading is IMG ALT=filename - 100%
			#*Heading is IMG sin ALT - 100%
			if (imgAttrAlt =='' or not imgAttrAlt):
				flag = 1
				typeError = 1
			elif (imgAttrAlt==imgAttrFileName):
				flag = 1
				typeError = 2
			#*Heading is IMG con ALT - 0%
			if(imgAttrAlt):
				good += 1


		#*IMG con FIGCAPTION - 50%
		elif (next1Figcap):
			good += 1

		#Definition lists con images as bullets - 100%
		elif (image.parent.name == "dd"):
			flag = 1
			typeError = 3

		#IMG con aria-describedby - 100%
		elif(imgAttrAriaDescby):
			flag = 1
			typeError = 4

		#IMG con ALT null y non-null TITLE attributes - 100%
		#IMG con ALT null y non-null aria-label attributes - 100%
		#IMG con ALT null y non-null aria-labelledby attributes - 100%
		#IMG sin ALT attribute - 100%

		elif((imgAttrAlt == '' and (imgAttrTitle != '' or imgAttrAriaLab != '' or imgAttrAriaLabBy != '')) or not imgAttrAlt):
			flag = 1
			typeError = 1

		#corresponde al parentesis de arriba:
		#if (imgAttrAlt == '' and imgAttrTitle != ''): flag = 1
		#if (imgAttrAlt == '' and imgAttrAriaLab != ''): flag = 1
		#if (imgAttrAlt == '' and imgAttrAriaLabBy != ''): flag = 1
		#if (!imgAttrAlt): flag = 1'''

		#IMG con ALT - 0%
		#IMG con TITLE - 0%
		#IMG con aria-label - 25%
		#IMG con aria-labelledby - 25%
		#IMG con atributo ALT null - 0%
		elif(imgAttrAlt or imgAttrTitle or imgAttrAriaLab or imgAttrAriaLabBy or imgAttrAlt == ''):
			good += 1

		#*(IMG con ALT) set to ASCII art smiley - 75%
		elif(imgAttrAlt):
			imgAltPunctuation = re.sub(r"[!\"#$%&'()*+¨,-./:;<=>?@[\]^_`{|}~°¡¿´\\¬]", '', imgAttrAlt, flags=0)
			if (imgAltPunctuation == ''):
				good += 1

		#*(IMG con ALT) set to SRC filename - 100%
		elif(imgAttrAlt==imgAttrFileName):
			flag = 1
			typeError = 2

        #IMG con server side image map - 100% //ismap es server-side y map es client-side
		elif(imgAttrIsMap):
			flag = 1
			typeError = 5

        #Image MAP sin NAME attribute - 50%
		elif (next1Map.get('name')):
			good += 1

        #*Link con `aria-label`, y contiene solo una `img` sin `alt` - 25%
		elif (imgAttrAriaLab and not imgAttrAlt):
			good += 1

		if (flag == 1):
			failed += 1
			pos = position(contentBase, image)
			pos.append(numId)
			pos.append(typeError)
			badTags.append(pos)
			flag = 0

	dataResponse ={
		'tag' : 'img',
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
	return badTags[0]

class Petition(Resource):
	def post(self):
		response = {}
		try:
			json_data = request.get_json(force=True)
			for key in json_data:
				if (key == 'html'):
					#funcion que extrae el codigo html
					response = evaluateImgs(json_data[key])
			return response
		except requests.exceptions.RequestException as e:
			return ("error")

api.add_resource(Petition, '/img_evaluation')

class Ping(Resource):
    def get(self):
        try:
            return {'status': 'success'}
        except requests.exceptions.RequestException as e:
            return {"status":"Error"}

api.add_resource(Ping, '/ping')

if __name__ == '__main__':
	app.run( debug = False, host='0.0.0.0', port=8026)
