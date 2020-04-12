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

def evaluateLegend(contentJson):
	contentBase= BeautifulSoup(contentJson, "lxml")

	legends = contentBase.find_all('legend')
	totalQuantity = len(legends)

	failed = 0
	good = 0
	badTags = []
	flag = 0
	numId = -1

	for legend in legends:
		numId += 1
		good += 1

		if (flag == 1):
			failed += 1
			pos = position(contentBase, legend)
			pos.append(numId)
			pos.append(typeError)
			badTags.append(pos)
			flag = 0

	dataResponse ={
		'tag' : 'legend',
		'totalTagsAnalyzed': totalQuantity,
		'totalTagsFailed': failed,
		'positionsBadTags': badTags
	}
	response = json.dumps({'status': 'success', 'data': dataResponse})
	return response

class Petition(Resource):
	def post(self):
		response = {}
		try:
			json_data = request.get_json(force=True)
			for key in json_data:
				if (key == 'html'):
					#funcion que extrae el codigo html
					response = evaluateLegend(json_data[key])
			return response
		except requests.exceptions.RequestException as e:
			return ("error")

api.add_resource(Petition, '/legend_evaluation')

class Ping(Resource):
    def get(self):
        try:
            return {'status': 'success'}
        except requests.exceptions.RequestException as e:
            return {"status":"Error"}

api.add_resource(Ping, '/ping')

if __name__ == '__main__':
	app.run( debug = False, host='0.0.0.0' , port=8029)
