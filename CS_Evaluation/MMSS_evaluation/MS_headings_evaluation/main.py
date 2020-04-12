from flask import Flask
from flask import request #para trabajar con parametros por rutas
from bs4 import BeautifulSoup
from flask_restful import Resource, Api
import requests
import json
import re
import warnings

#ppp: re.sub launches the DeprecationWarning, I can not identify the reason. For this reason, this line is added.
warnings.filterwarnings("ignore", category=DeprecationWarning)

app = Flask(__name__)
app.secret_key = 'html_secret_key'
api = Api(app)

def evaluateHeadings(contentJson):
    contentBase= BeautifulSoup(contentJson, "lxml")
    tags = ['h1','h2','h3','h4','h5','h6']
    totalFailed = 0
    totalQuantity = 0
    badTags = []
    num_id = -1

    for t in tags:
        failedAux, totalAux, badTagsAux, num = evalByH(contentBase, t, num_id)
        totalFailed += failedAux
        totalQuantity += totalAux
        num_id = num
        if (len(badTagsAux)>0):
            badTags += badTagsAux

    dataResponse ={
        'tag': 'Headings',
        'totalTagsAnalyzed': totalQuantity,
        'totalTagsFailed': totalFailed,
        'positionsBadTags': badTags
    }
    response = json.dumps({'status': 'success', 'data': dataResponse})
    return response

def evalByH(contentBase, tag, num_id):
    headings = contentBase.find_all(tag)
    failed = 0
    good = 0
    badTags = []
    flag = 0
    numId = num_id

    #para recorrer el listado de los elementos encontrados
    for h in headings:
        numId += 1
        #para buscar el siguiente tag
        next1 = h.findNext()
        #para buscar un tag en especifico dentro del next1.
        img = BeautifulSoup(str(next1), 'lxml').find('img')
        h1 = BeautifulSoup(str(next1), 'lxml').find('h1')
        h2 = BeautifulSoup(str(next1), 'lxml').find('h2')
        h3 = BeautifulSoup(str(next1), 'lxml').find('h3')
        h4 = BeautifulSoup(str(next1), 'lxml').find('h4')
        h5 = BeautifulSoup(str(next1), 'lxml').find('h5')
        h6 = BeautifulSoup(str(next1), 'lxml').find('h6')

        #next1.parent.name == 'img' es para saber si el padre de next1 es el tag "img"
        if ((next1 != None) and (next1 == img ) and (next1.parent.name == tag)):
            imgAttrAlt = img.get('alt')
            imgAttrSrc = img.get('src')
            if (imgAttrAlt and imgAttrAlt != ''):
                #Heading is IMG ALT=filename
                if(imgAttrSrc==imgAttrAlt):
                    good += 1 #es problema de la imagen, no de heading
                    #flag = #Tipo de incompatibilidad 1:
                    #typeError = 1
                #Heading is *(IMG con ALT)
                else:
                    good += 1
            #Heading is IMG ALT=""
            elif (imgAttrAlt and imgAttrAlt == ''):
                good += 1 #es problema de la imagen, no de heading
                #flag = 1
                #typeError = 2
            #Heading is IMG sin ALT
            elif(not imgAttrAlt):
                good += 1 #es problema de la imagen, no de heading
                #flag = 1
                #typeError = 3
            else :
                #no deberia ocurrir

        #Nested headings
        elif((next1 != None) and (next1.parent.name == tag) and ((next1 == h1) or (next1 == h2) or (next1 == h3) or (next1 == h4) or (next1 == h5) or (next1 == h6))):
            flag = 1
            typeError = 1
        elif((h.parent.name == "h1") or (h.parent.name == "h2") or (h.parent.name == "h3") or (h.parent.name == "h4") or (h.parent.name == "h5") or (h.parent.name == "h6")):
            flag = 1
            typeError = 1
        #Empty heading
        elif(img == None):
            if(h.string == None):
                good += 1

            else:
                headingSpaces = re.sub(r"[ \t\n\x0B\f\r]", '', h.string, flags=0)
                headingPunctuation = re.sub(r"[\t\n\x0B\f\r !\"#$%&'()*+¨,-./:;<=>?@[\]^_`{|}~°¡¿´\\¬]", '', h.string, flags=0)
                #Heading non-breaking spaces or Heading only spaces
                if (headingSpaces == ''):
                    good += 1
                #Heading only punctuation
                elif (headingPunctuation == ""):
                    flag = 1
                    typeError = 2
                else:
                    # este caso no ha sido considerado

        else:
            good += 1

        if (flag == 1):
            failed += 1
            pos = position(contentBase, h)
            pos.append(numId)
            pos.append(typeError)
            badTags.append(pos)
            flag = 0

    return(failed, len(headings), badTags, numId)

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
                    response = evaluateHeadings(json_data[key])
            return response
        except requests.exceptions.RequestException as e:
            return ("error")

api.add_resource(Petition, '/headings_evaluation')

class Ping(Resource):
    def get(self):
        try:
            return {'status': 'success'}
        except requests.exceptions.RequestException as e:
            return {"status":"Error"}

api.add_resource(Ping, '/ping')

if __name__ == '__main__':
    app.run( debug = False, host='0.0.0.0' , port=8024)
