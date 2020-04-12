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


def evaluateFieldset(contentJson):
    contentBase= BeautifulSoup(contentJson, "lxml")

    fieldsets = contentBase.find_all('fieldset')
    totalQuantity = len(fieldsets)

    failed = 0
    good = 0
    badTags = []
    flag = 0
    numId = -1

    for fieldset in fieldsets:
        numId += 1

        nextAux = fieldset.findNext()
        nextA = BeautifulSoup(str(nextAux), 'lxml').find('a')
        nextInputs = BeautifulSoup(str(nextAux), 'lxml').find_all('input')
        nextLegend = BeautifulSoup(str(nextAux), 'lxml').find('legend')
        nextP = BeautifulSoup(str(nextAux), 'lxml').find('p')

        #*FIELDSET containing links - 50%
        if (nextA and nextA.parent.name == "fieldset"):
            good += 1

        #Yes/No radio buttons inside `fieldset` element - 25%
        elif (nextInputs):
            isRadio = True
            for inputradio in nextInputs:
                if (inputradio.get('type') != 'radio'):
                    isRadio = False
            if (isRadio):
                good += 1

        elif (nextLegend):
            legendPlaceholder = nextLegend.text
            if (legendPlaceholder):
                legendPlaceholder = re.sub(r"[ \t\n\x0B\f\r]", '', legendPlaceholder, flags=0)

            #FIELDSET containing no controls - 25%
            if(nextLegend == nextAux):
                good += 1

            #FIELDSET con blank LEGEND - 75%
            #FIELDSET sin LEGEND - 50%
            elif (legendPlaceholder == '' or not legendPlaceholder):
                good += 1
            else: 
                # no se ha considerado deste caso

        #FIELDSET used to put border round text - 25%
        elif (nextP):
            good += 1
        
        else: 
            # no se ha considerado deste caso

        if (flag == 1):
            failed += 1
            pos = position(contentBase, fieldset)
            pos.append(numId)
            pos.append(typeError)
            badTags.append(pos)
            flag = 0

    dataResponse ={
        'tag' : 'fieldset',
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
					response = evaluateFieldset(json_data[key])
			return response
		except requests.exceptions.RequestException as e:
			return ("error")

api.add_resource(Petition, '/fieldset_evaluation')

class Ping(Resource):
    def get(self):
        try:
            return {'status': 'success'}
        except requests.exceptions.RequestException as e:
            return {"status":"Error"}

api.add_resource(Ping, '/ping')

if __name__ == '__main__':
	app.run( debug = False, host='0.0.0.0' , port=8021)
