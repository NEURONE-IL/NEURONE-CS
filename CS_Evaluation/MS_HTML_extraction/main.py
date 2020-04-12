from flask import Flask
from flask import request #para trabajar con parametros por rutas
from bs4 import BeautifulSoup
from flask_restful import Resource, Api
import requests
import json

app = Flask(__name__)
app.secret_key = 'html_secret_key'
api = Api(app)

def readURL(url):
	try:
		#Petition a la web
		req = requests.get(url)

		#verificiación destatus code de la Petition
		status_code = req.status_code

		if status_code == 200:
			try:
				encod = str(req.encoding)
				utf8 = req.content.decode(encod).encode('utf8')
				#pasa el contenido html de la web, a un objeto beautiful Soup
				html = BeautifulSoup(utf8, "html.parser")
				pretti = html.prettify()
				response = json.dumps({'status': 'success', 'data': pretti})
			except Exception as e:
				print("ERROR!!!")
				response = json.dumps({'status': "error", 'data' : "" })
		else:
			print("ERROR!!!")
			response = json.dumps({'status': "error", 'data' : "" })
	except Exception as e:
		print("ERROR!!!")
		response = json.dumps({'status': "error", 'data' : "" })

	return response

# aqui se recibe la Petition post
class Petition(Resource):
	def post(self):
		response = {}
		try:
			json_data = request.get_json(force=True)
			for key in json_data:
				if (key == 'url'):
					#funcion que extrae el codigo html
					response = readURL(json_data[key])
			return response
		except requests.exceptions.RequestException as e:
			return ("error")

api.add_resource(Petition, '/html_extraction')

class Ping(Resource):
    def get(self):
        try:
            return {'status': 'success'}
        except requests.exceptions.RequestException as e:
            return {"status":"Error"}

api.add_resource(Ping, '/ping')

if __name__ == '__main__':
	app.run( debug = False, host='0.0.0.0', port=8001 )
