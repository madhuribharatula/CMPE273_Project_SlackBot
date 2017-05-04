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
db=client['slackbotDB']

@app.route('/')
def hello_world():

   return "Hello World"

@app.route('/cmpe273')
def find_document():
    db.greennsheetdocs.insert({
        "filename":"CMPE273"

    })
    return "Success"
@app.route("/get/<value>")
def get_content(value):
    collection=db.greensheetdocs.find()
    json_collection = []
    avc=[]
    for doc in collection:
       json_doc = json.dumps(doc, default=json_util.default)
       json_collection.append(json_doc) 
    html_content= str(json.dumps(json_collection))
    soup = BeautifulSoup(html_content)
    if(value=='Final Exam'):
     for each in soup.findAll(name = 'td'):
        avc.append(each)
     temp=str(avc)
     temp1=re.search(value+' (.*) pm (.*) pm',temp)
     res=temp1.group()
     return json.dumps(res)
    else:
     for each in soup.findAll(name = 'td'):
        avc.append(each)
     temp=str(avc)
     temp1=re.search(value+' (.*)',temp)
     res=temp1.group()
     return res.split(',')[1]      
if __name__=='__main__':
  app.run(debug=True, port=8080)
