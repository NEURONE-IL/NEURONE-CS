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

def evaluateTable(contentJson):
  contentBase= BeautifulSoup(contentJson, "lxml")

  tables = contentBase.find_all('table')
  totalQuantity = len(tables)

  failed = 0
  good = 0
  badTags = []
  flag = 0
  numId = -1

  for table in tables:
    tableRole = table.get('role')
    tableSummary = table.get('summary')

    tableNext = table.findNext()
    tableNextBS = BeautifulSoup(str(tableNext), 'lxml')

    nextCaption = tableNextBS.find('caption')
    nextTrs = tableNextBS.find_all('tr')  #verificar por que no los esta tomando todos.
    nextTds = tableNextBS.find_all('td')
    nextThs = tableNextBS.find_all('th')
    tHead = tableNextBS.find('thead')
    tFoot = tableNextBS.find('tfoot')

    tdsQuantity = len(nextTds)
    thsQuantity = len(nextThs)
    numId += 1
    '''
      typeError = 1 -> debe agregar TH o thead y tfoot
      typeError = 2 -> debe eliminar el tableRole, presentation y note no sirven.
      typeError = 3 -> puede solucionarlo agregando el atributo "columnheader" a los "td" o agregando "th".
    '''

    #ok Data table con SUMMARY y TH - 25%
    #ok Data table con CAPTION y TH - 25%
    if (thsQuantity>0 and tableSummary or nextCaption):
        good += 1

    #ok Data table con role presentation - 100%
    #ok Data table con role note - 100%
    elif (tableRole=="presentation" or tableRole=="note"):
      flag = 1
      typeError = 2

    #ok Data table con role grid - 25%
    #ok Layout table con role presentation - 25% -> ???
    elif (tableRole == "grid" or tableRole == "presentation"):
      good += 1

    elif (nextTrs):
      if (len(nextTrs)>1):
        thWithScope = True
        thWithoutScope = True
        tdWithHeaders = True
        cont = 1
        for tr in nextTrs:
          trNext = tr.findNext()
          trNextBS = BeautifulSoup(str(tr), 'lxml')
          trNextThs = tableNextBS.find_all('th')
          trNextTds = tableNextBS.find_all('td')
          # Data table con TH cell headers - 25% ->
          if(cont == 1 and trNextThs and not trNextTds):
            good += 1
          else:
            #Data table con TH row/columns headers con SCOPE - 75%
            #Data table con TH row/columns headers without SCOPE - 75%
            for th in trNextThs:
              thScope = table.get('scope')
              if (thScope):
                thWithoutScope = False
              else:
                thWithScope = False
            # Data table con TD HEADERS attribute - 50% ->
            for td in trNextTds:
              thHeaders = table.get('headers')
              if (not tdWithHeaders):
                tdWithHeaders= False
          cont += 1
        if (thWithScope or thWithoutScope or tdWithHeaders):
          good += 1
        else:
          #este caso no ha sido considerado

      elif(thsQuantity==0):
        #ok Data table con CAPTION but no TH - 100%
        if (nextCaption and tableNext.parent.name == "table"):
          flag = 1
          typeError = 1

        #ok Data table con SUMMARY but no TH - 100%
        #ok Data table con null SUMMARY but no TH - 100% -> (or tableSummary== '')
        elif (tableSummary):
          flag = 1
          typeError = 1

        #ok Data table con THEAD, TFOOT but no TH - 75%
        elif(tHead and tFoot):
          good += 1

        # ok Data table con role columnheader headers but no TH - 75%
        elif (tdsQuantity>0):
          roleColumheader = True
          for td in nextTds:
              tdAttrRole = td.get('role')
              if (tdAttrRole != "columnheader"):
                roleColumheader = False
          if (roleColumheader):
            good += 1
          else:
            flag = 1
            typeError = 3

        #ok Data table sin TH elements - 100% "
        else:
          flag = 1
          typeError = 1

      #Layout table con single cell - 25%
      else:
        trNextTds = tableNextBS.find_all('td')
        if (len(trNextTds)==1):
          good += 1
        else:
          for tr in nextTrs:
            trNext = tr.findNext()
            trNextBS = BeautifulSoup(str(tr), 'lxml')
            trNextThs = tableNextBS.find_all('th')
            trNextTds = tableNextBS.find_all('td')
            # Data table con TH cell headers - 25% ->
            if(trNextThs and not trNextTds):
              good += 1
            else:
              #esto no debería ocurrir

    else:
      good += 1

    if (flag == 1):
      failed += 1
      pos = position(contentBase, table)
      pos.append(numId)
      pos.append(typeError)
      badTags.append(pos)
      flag = 0

  dataResponse ={
    'tag' : 'table',
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
					response = evaluateTable(json_data[key])
			return response
		except requests.exceptions.RequestException as e:
			return ("error")

api.add_resource(Petition, '/table_evaluation')

class Ping(Resource):
    def get(self):
        try:
            return {'status': 'success'}
        except requests.exceptions.RequestException as e:
            return {"status":"Error"}

api.add_resource(Ping, '/ping')

if __name__ == '__main__':
	app.run( debug = False, host='0.0.0.0', port=8035)
