from flask import Flask
from flask import request
from bs4 import BeautifulSoup
from flask_restful import Resource, Api
#from lxml.etree import tostring
import lxml.html as LH
import requests
import json
import re
import warnings

#ppp: re.sub launches the DeprecationWarning, I can not identify the reason. For this reason, this line is added.
warnings.filterwarnings("ignore", category=DeprecationWarning)

app = Flask(__name__)
app.secret_key = 'html_secret_key'
api = Api(app)

def cleanHtml(contentBaseJson):
	contentBase= (BeautifulSoup(contentBaseJson, "html.parser")).prettify()
	response = json.dumps({'status': 'success', 'data': ""})
	contentClear = contentBase

	try:
		noneScripts = re.sub(r"<(script).*?</\1>(?s)", '', contentClear, flags=0)
		if (noneScripts):
			contentClear = noneScripts

		noneFrames = re.sub(r'<(frame).*?</\1>(?s)', '', contentClear, flags=0)
		if (noneFrames):
			contentClear = noneFrames

		noneIframes = re.sub(r'<(iframe).*?</\1>(?s)', '', contentClear, flags=0)
		if (noneIframes):
			contentClear = noneIframes

		noneTarget = re.sub(r"[Tt][Aa][Rr][Gg][Ee][Tt](\s)?=(\s)?[\"\'].*?[\"\']","", contentClear)
		if (noneTarget):
			contentClear = noneTarget

		noneHref = re.sub(r"href(\s)?=(\s)?([\"\']){1}(.*?)([\"\']){1}","href=\"javascript: void(0)\"", contentClear)
		if (noneHref):
			contentClear = noneHref

		noneOnClick = re.sub(r"[oO][nN][cC][lL][iI][cC][kK](\s)?=(\s)?[\"\'].*?[\"\']","", contentClear)
		if (noneOnClick):
			contentClear = noneOnClick

		noneSubmit = re.sub(r"[Tt][Yy][Pp][Ee](\s)?=(\s)?[\"\']submit[\"\']","", contentClear)
		if (noneSubmit):
			contentClear = noneSubmit

		#contentClear = bytearray(contentClear, 'utf8')
		root = LH.fromstring(contentClear)

		for element in root.iter('input'):
			if (element.find('id')):
				del element.attrib['id']
			element.attrib['disabled'] = 'True'

		for element in root.iter('button'):
			if (element.find('id')):
				del element.attrib['id']
			element.attrib['disabled'] = 'True'

		for element in root.iter('form'):
			if (element.find('action')):
				del element.attrib['action']
			if (element.find('method')):
				del element.attrib['method']

		temp1 = LH.tostring(root, pretty_print=True)
		temp2 = BeautifulSoup(temp1, "lxml")
		contentClear = temp2.decode('utf-8')

		root = re.sub(r"disabled=\"\"","disabled=\"true\"", contentClear)
		response = json.dumps({'status': 'success', 'data': root})

	except Exception as e:
		print(e)
		print("ERROR!!!")
		response = json.dumps({'status': 'error', 'data': ""})

	return response

# aqui se recibe la Petition post
class Petition(Resource):
	def post(self):
		response = {}
		try:
			json_data = request.get_json(force=True)
			for key in json_data:
				if (key == 'html'):
					#funcion que extrae el codigo html
					response = cleanHtml(json_data[key])
			return response
		except requests.exceptions.RequestException as e:
			return ("error")

api.add_resource(Petition, '/html_cleaning')

class Ping(Resource):
    def get(self):
        try:
            return {'status': 'success'}
        except requests.exceptions.RequestException as e:
            return {"status":"Error"}

api.add_resource(Ping, '/ping')

if __name__ == '__main__':
	app.run( debug = False, host='0.0.0.0', port=8002)
