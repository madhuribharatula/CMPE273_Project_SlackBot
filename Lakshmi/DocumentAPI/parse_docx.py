from pydocx import PyDocX
from flask import Flask
from flask import jsonify
import json
from bson import json_util
from pymongo import MongoClient
import sys
import re
from BeautifulSoup import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

html = PyDocX.to_html(open('cmpe273-greensheet.docx', 'rb'))

app = Flask(__name__);
client = MongoClient('mongodb://localhost:27017/')
db=client['greensheetDB']

@app.route('/')
def hello_world():

   return "Hello World"

@app.route('/cmpe273')
def find_document():
    db.docCollection.insert({
        "filename":"CMPE273"

    })
    return "Success"
def cleanhtml(raw_html):
  cleantext =raw_html
  if raw_html is not None:
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

@app.route("/get/<value>")
def get_content(value):
    collection=db.docCollection.find({'FileName' : value})
    json_collection = []
    avc=[]
    for doc in collection:
       json_doc = json.dumps(doc, default=json_util.default)
       json_collection.append(json_doc)
    html_content= str(json.dumps(json_collection))
    soup = BeautifulSoup(html_content)
    dict={}
    for each in soup.findAll(name = 'tr'):
        count = 1
        key1=''
        key2=''
        value=''
        for trdata in each.findAll(name = 'td'):
                trdata = cleanhtml(str(trdata))
                if count==1:
                    key1 = trdata
                elif count ==2:
                    value = trdata
                elif count ==3:
                    key2 = trdata
                count=count+1
        if key1 !='' and value!='':
            dict[key1] = value
        if key2 != '':
            dict[key2] = key1
    print dict
    # for hdata in each.findAll(name ='h2'):
    #     if(hdata.text not in dict):
    #            print hdata.text
    # print "****"


    return "hello"

if __name__=='__main__':
  app.run(debug=True, port=8080)