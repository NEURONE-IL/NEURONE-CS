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
Data table con CAPTION y TH - 25%
    <table>
      <caption>Data table caption</caption>
      <tbody>
        <tr>
          <th>Morning</th>
          <th>Afternoon</th>
        </tr>
        <tr>
          <td>Free</td>
          <td>Busy</td>
        </tr>
      </tbody>
    </table>
    -h39 / f91 /

Data table con CAPTION but no TH - 100%
    <table>
      <caption>Data table caption</caption>
      <tbody>
        <tr>
          <td><strong>Morning</strong></td>
          <td><strong>Afternoon</strong></td>
        </tr>
        <tr>
          <td>Free</td>
          <td>Busy</td>
        </tr>
      </tbody>
    </table>
    -f91
'''

def evaluateCaption(contentJson):
  contentBase= BeautifulSoup(contentJson, "lxml")

  captions = contentBase.find_all('caption')
  totalQuantity = len(captions)

  failed = 0
  good = 0
  badTags = []
  flag = 0
  numId = -1

  for caption in captions:
    numId += 1
    captionAttrTitle = caption.get('title')
    captionAttrAriaLab = caption.get('aria-label')
    nextAux = caption.findNext()
    nextImg = BeautifulSoup(str(nextAux), 'lxml').find_all('img')

      if (flag == 1):
        failed += 1
        pos = position(contentBase, caption)
        pos.append(numId)
        pos.append(typeError)
        badTags.append(pos)
        flag = 0

  dataResponse ={
    'tag' : 'caption',
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
					response = evaluateCaption(json_data[key])
			return response
		except requests.exceptions.RequestException as e:
			return ("error")

api.add_resource(Petition, '/caption_evaluation')

class Ping(Resource):
    def get(self):
        try:
            return {'status': 'success'}
        except requests.exceptions.RequestException as e:
            return {"status":"Error"}

api.add_resource(Ping, '/ping')

if __name__ == '__main__':
	app.run( debug = False, host='0.0.0.0' , port=8017)
