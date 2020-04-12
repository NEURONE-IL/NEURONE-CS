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
'''
ARIA role=heading - 25%
    <div role='heading' aria-level='1'>First level heading</div>
    <p>Heading 1 content</p>
    <div role='heading' aria-level='2'>Second level heading</div>
    <p>Heading 2 content</p>
    -aria12

encabezados ARIA anidados - 100%
    <div role='heading' aria-level='1'>First level heading
        <div role='heading' aria-level='2'>Second level heading</div>
    </div>

    <p>Heading 2 content</p>
    -//'''
def evaluateDiv(contentJson):
	contentBase= BeautifulSoup(contentJson, "lxml")

	divs = contentBase.find_all('div')
	totalQuantity = len(divs)

	failed = 0
	badTags = []
	good = 0
	flag = 0
	numId = -1

	for div in divs:
		numId += 1

		divRole = div.get('role')
		divAria = div.get('aria-level')
		nextAux = div.findNext()
		divNested = BeautifulSoup(str(nextAux), 'lxml').find('div')
		divParent = div.parent

		if (divAria):
			#encabezados ARIA anidados - 100%
			parentAria = divParent.get('aria-level')
			parentRole = divParent.get('role')
			if (divParent.name == "div" and parentAria and parentRole=="heading" ):
				flag = 1
				typeError = 1

			#encabezados ARIA anidados - 100%
			elif (divNested):
				divNestedRole = divNested.get('role')
				divNestedAria = divNested.get('aria-level')
				if(divNestedAria and (divNestedRole == "heading")):
					flag = 1
					typeError = 1

			#ARIA role=heading -25%
			elif (divRole and divRole == "heading" and not divNested):
				good += 1
		else:
			good += 1

		if (flag == 1):
			failed += 1
			pos = position(contentBase, div)
			pos.append(numId)
			pos.append(typeError)
			badTags.append(pos)
			flag = 0

	dataResponse ={
		'tag': 'div',
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
					response = evaluateDiv(json_data[key])
			return response
		except requests.exceptions.RequestException as e:
			return ("error")

api.add_resource(Petition, '/div_evaluation')

class Ping(Resource):
    def get(self):
        try:
            return {'status': 'success'}
        except requests.exceptions.RequestException as e:
            return {"status":"Error"}

api.add_resource(Ping, '/ping')

if __name__ == '__main__':
	app.run( debug = False, host='0.0.0.0', port=8019)
