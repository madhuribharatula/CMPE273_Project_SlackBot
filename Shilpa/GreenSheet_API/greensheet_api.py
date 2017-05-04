from pydocx import PyDocX
from flask import Flask, render_template, request
from flask import jsonify
import json
from bson import json_util
from pymongo import MongoClient
import sys
import re
from werkzeug.utils import secure_filename
from BeautifulSoup import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')


app = Flask(__name__);
client = MongoClient('mongodb://localhost:27017/')
db=client['slackbotDB']

@app.route('/')
def hello_world():

   return "Hello World"

@app.route('/find_doc/<collection_name>')
def find_document(collection_name):
    if(collection_name in db.collection_names()):
      return "Success"
    else:
      return "File Not Found"
@app.route('/upload')
def upload_file():
   return render_template('upload.html')
    
@app.route('/uploader',methods = ['GET', 'POST'])
def insert_document():   
   if request.method == 'POST':
      f = request.files['file']
   f.save(secure_filename(f.filename))
   html = PyDocX.to_html(open(f.filename, 'rb'))
   db.greensheetdocs.insert({
        "filename":"CMPE273",
        "HTML":html
    })
   return "Successfully Uploaded"

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
