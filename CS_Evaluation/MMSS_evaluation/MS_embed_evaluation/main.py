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


def evaluateEmbed(contentJson):
	contentBase= BeautifulSoup(contentJson, "lxml")

	embeds = contentBase.find_all('embed')
	totalQuantity = len(embeds)

	failed = 0
	good = 0
	badTags = []
	flag = 0
	numId = -1

	for embed in embeds:
		numId += 1
		embedAttrAriaLabBy = embed.get('aria-labelledby')
		embedAttrAriaLab = embed.get('aria-label')
		embedAttrTitle = embed.get('title')
		embedAttrAlt = embed.get('alt')
		embedParent = embed.parent
		embedPlaceholder = embed.text

		if (embedPlaceholder):
			embedPlaceholder = re.sub(r"[ \t\n\x0B\f\r]", '', embedPlaceholder, flags=0)


		#EMBED con ARIA-LABEL attribute	- 75%
		if (embedAttrAriaLab):
			good += 1

		#`embed` inside `figure` con `figcaption` - 25%
		elif (embedParent.name == 'figure'):
			figureWithFigcaption = BeautifulSoup(str(embedParent), 'lxml').find('figcaption')
			if (figureWithFigcaption):
				good += 1

		#EMBED con ARIA-LABELLEDBY attribute - 100%
		#EMBED con ALT attribute - 100%
		#EMBED con TITLE attribute - 100%
		#EMBED sin description - 100%
		elif (embedAttrAriaLabBy or embedAttrAlt or embedAttrTitle or not embedPlaceholder):
			flag = 1
			typeError = 1

		if (flag == 1):
			failed += 1
			pos = position(contentBase, embed)
			pos.append(numId)
			pos.append(typeError)
			badTags.append(pos)
			flag = 0

	dataResponse ={
		'tag' : 'embed',
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
					response = evaluateEmbed(json_data[key])
			return response
		except requests.exceptions.RequestException as e:
			return ("error")

api.add_resource(Petition, '/embed_evaluation')

class Ping(Resource):
    def get(self):
        try:
            return {'status': 'success'}
        except requests.exceptions.RequestException as e:
            return {"status":"Error"}

api.add_resource(Ping, '/ping')

if __name__ == '__main__':
	app.run( debug = False, host='0.0.0.0' , port=8020)
