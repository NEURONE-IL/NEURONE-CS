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

def evaluateInput(contentJson):
    contentBase= BeautifulSoup(contentJson, "lxml")
 
    inputs = contentBase.find_all('input')
    totalQuantity = len(inputs)

    failed = 0
    good = 0
    badTags = []
    flag = 0
    numId = -1

    for inpu in inputs:
        numId += 1
        inputAttrAlt = inpu.get('alt')
        inputAttrType = inpu.get('type')
        inputAttrTitle = inpu.get('title')
        inputAttrAriaLab = inpu.get('aria-label')
        inputAttrAriaLabBy = inpu.get('aria-labelledby')
        inputAttrAriaDescBy = inpu.get('aria-describedby')

        inputPlaceholder = inpu.text

        if (inputPlaceholder):
            inputPlaceholder = re.sub(r"[ \t\n\x0B\f\r]", '', inputPlaceholder, flags=0)
        
        if (inputAttrType == 'image'):
            #INPUT type=image con ALT attribute - 0%
            #INPUT type=image con TITLE attribute - 25%
            #`input type=image` con `aria-label` attribute - 25%
            #`input type=image` con `aria-labelledby` attribute - 25%
            if (inputAttrAlt or inputAttrTitle or inputAttrAriaLab or inputAttrAriaLabBy):
                good += 1

            #INPUT type=image sin ALT attribute - 100%
            #INPUT type=image con ALT null - 100%
            elif (not inputAttrAlt or inputAttrAlt == ''):
                flag = 1
                typeError = 1

        elif (inputAttrType == 'text'):
            #INPUT type=text con aria-describedby attribute - 25%
            if (inputAttrAriaDescBy):
                good += 1

            elif (inpu.parent.name == 'label'):
                #INPUT type=text inside LABEL con text before y after control - 25%
                if (inpu.parent.text and inputPlaceholder):
                    good += 1

                #INPUT type=text inside LABEL con text after control - 25%
                elif(inputPlaceholder):
                    good += 1
                
                #INPUT type=text con LABEL FOR - 0%
                elif (inpu.parent.get("for") == 'label_for'):
                    good += 1

                #INPUT type=text inside blunak LABEL - 100%
                elif (inpu.parent.text):
                    good += 1 # es un problema de label
                    #flag = 1
                    #typeError = 2
            
                #INPUT type=text inside LABEL con text before control - 0%
                elif(inpu.parent.text):
                    good += 1

                #INPUT type=text con blunak LABEL FOR - 100%
                elif (not inpu.parent.text and inpu.parent.get("for") == 'label_for'):
                    good += 1 # es un problema de label
                    #flag = 1
                    #typeError = 2

        if (flag == 1):
            failed += 1
            pos = position(contentBase, inpu)
            pos.append(numId)
            pos.append(typeError)
            badTags.append(pos)
            flag = 0

    dataResponse ={
        'tag' : 'input',
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
					response = evaluateInput(json_data[key]) 
			return response
		except requests.exceptions.RequestException as e: 
			return ("error")

api.add_resource(Petition, '/input_evaluation')

class Ping(Resource):
    def get(self):
        try:
            return {'status': 'success'}
        except requests.exceptions.RequestException as e:
            return {"status":"Error"}

api.add_resource(Ping, '/ping')

if __name__ == '__main__':
	app.run( debug = False, host='0.0.0.0', port=8027)