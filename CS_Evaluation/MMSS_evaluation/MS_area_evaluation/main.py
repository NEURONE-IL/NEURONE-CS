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

def evaluateArea(contentJson):
	contentBase= BeautifulSoup(contentJson, "lxml")

	areas = contentBase.find_all('area')
	totalQuantity = len(areas)

	failed = 0
	good = 0
	badTags = []
	flag = 0
	numId = -1

	for area in areas:
		numId += 1
		parent = BeautifulSoup(str(area.parent), 'lxml')
		grandParent = BeautifulSoup(str(area.parent.parent), 'lxml')
		withMap = parent.find('map')
		withImg = grandParent.find('img')
		areaAttrAlt = area.get('alt')
		areaAttrTitle = area.get('title')
		areaAttrAriaLab = area.get('aria-label')
		areaAttrAriaLabBy = area.get('aria-labelledby')

		if (withImg):
			imgAlt = withImg.get('alt')
			#verificar si <area> e <img> tienen atributo alt  - 50%
			#verificar si <area> tiene alt e <img> con alt nulo  - 25% -> imgAlt = ''
			if((imgAlt or imgAlt == "") and areaAttrAlt):
				good += 1

			else:
				#verificar si <area> tiene atributo aria-label - 50%
				#verificar si <area> tiene atributo title  - 75 %
				#verificar si <area> tiene area-labelledby  - 75%
				if( areaAttrTitle or areaAttrAriaLab or areaAttrAriaLabBy):
					good += 1

				#si <area> no tiene atributo alt  - 100%
				#si <area>  tiene alt nulo  - 100%
				elif(not areaAttrAlt or areaAttrAlt == ''):
					flag = 1
					typeError = 1

				#verificar si image MAP (<area> dentro de <map> bajo <img>) no tiene atributo nombre   - 50%
				elif(withMap):
					mapName = withMap.get('name')
					if (not mapName):
						good += 1


		if (flag == 1):
			failed += 1
			pos = position(contentBase, area)
			pos.append(numId)
			pos.append(typeError)
			badTags.append(pos)
			flag = 0

	dataResponse ={
		'tag' : 'area',
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
					response = evaluateArea(json_data[key])
			return response
		except requests.exceptions.RequestException as e:
			return ("error")

api.add_resource(Petition, '/area_evaluation')

class Ping(Resource):
    def get(self):
        try:
            return {'status': 'success'}
        except requests.exceptions.RequestException as e:
            return {"status":"Error"}

api.add_resource(Ping, '/ping')

if __name__ == '__main__':
	app.run( debug = False, host='0.0.0.0' , port=8014)
