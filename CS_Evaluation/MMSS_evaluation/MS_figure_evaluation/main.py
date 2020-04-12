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
*IMG con FIGCAPTION - 50%
    <figure>
        <img src='1234.png'>
        <figcaption>Violet, taken on 12/11/2010.</figcaption>
    </figure>
    -w: f30 -a /w: f65 -a
*`applet` inside `figure` con `figcaption` element - 25%
<figure>
        <applet code='appletComponentArch.DynamicTreeApplet' archive='https://docs.oracle.com/javase/tutorial/deployment/applet/examples/dist/applet_ComponentArch_DynamicTreeDemo/DynamicTreeDemo.jar' width='300' height='300'>
            <param name='permissions' value='sandbox'></param>
        </applet>
        <figcaption>Figure caption for applet</figcaption>
    </figure>
    -w: h35 -a
*`embed` inside `figure` con `figcaption` - 25%
 <figure>
        <embed type='video/mp4' src='small.mp4' width='100' height='100'></embed>
        <figcaption>Figure caption for embed</figcaption>
    </figure>
    -h35
'''

def evaluateFigure(contentJson):
	contentBase= BeautifulSoup(contentJson, "lxml")

	figures = contentBase.find_all('figure')
	totalQuantity = len(figures)

	failed = 0
	good = 0
	badTags = []
	flag = 0
	numId = -1

	for figure in figures:
		numId += 1
		good += 1

		if (flag == 1):
			failed += 1
			pos = position(contentBase, figure)
			pos.append(numId)
			pos.append(typeError)
			badTags.append(pos)
			flag = 0

	dataResponse ={
		'tag' : 'figure',
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
					response = evaluateFigure(json_data[key])
			return response
		except requests.exceptions.RequestException as e:
			return ("error")

api.add_resource(Petition, '/figure_evaluation')

class Ping(Resource):
    def get(self):
        try:
            return {'status': 'success'}
        except requests.exceptions.RequestException as e:
            return {"status":"Error"}

api.add_resource(Ping, '/ping')

if __name__ == '__main__':
	app.run( debug = False, host='0.0.0.0' , port=8023)
