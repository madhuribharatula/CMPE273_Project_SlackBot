from pydocx import PyDocX
from flask import Flask, render_template, request
from flask import jsonify
from bson import json_util
from pymongo import MongoClient
from BeautifulSoup import BeautifulSoup
from werkzeug.utils import secure_filename
from DocumentAPI.handleQuestions import handle_question

import sys
import re
import json



reload(sys)
sys.setdefaultencoding('utf-8')



app = Flask(__name__);
client = MongoClient('mongodb://localhost:27017/')
db=client['greensheetDB']

# @app.route('/handle')
# def handle():
#     dict={}
#     dict['subjectname'] = 'CMPE 273'
#
#     handle_question(dict)
#     return "handled"

@app.route('/uploader',methods = ['GET', 'POST'])
def insert_document():
   msg =''
   if request.method == 'POST':
      uploaded_file = request.files['file']
      uploaded_file.save(secure_filename(uploaded_file.filename))
      html = PyDocX.to_html(open(uploaded_file.filename, 'rb'))
      parse_store_content(html)
   return "File successfully parsed and uploaded"

def cleanhtml(raw_html):
  cleantext =raw_html
  if raw_html is not None:
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def parse_store_content(value):
    qadict = get_content(value)
    collection = db.docCollection
    posts = db.docCollection
    posts.insert_one(qadict)


def get_content(value):
    collection=value
    json_collection = []
    for doc in collection:
       json_doc = json.dumps(doc, default=json_util.default)
       json_collection.append(json_doc)
    html_content= str(json.dumps(json_collection))
    soup = BeautifulSoup(html_content)
    qadict={}
    if qadict.has_key("Course"):
        file_name = qadict["Course"]
        qadict["fileName",file_name]
    for each in soup.findAll(name = 'tr'):
        count = 1
        key1=''
        key2=''
        value=''
        for trdata in each.findAll(name = 'td'):
                trdata = trdata.text
                if count==1:
                    key1 = trdata
                elif count ==2:
                    value = trdata
                elif count ==3:
                    key2 = trdata
                count=count+1
        if key1 !='' and value!='':
            qadict[key1] = value
        if key2 != '':
            qadict[key2] = key1

    for section in soup.findAll('h2'):
        if not qadict.has_key(section.text):
            nextNode = section
            apended_value = ''
            while True:
                nextNode = nextNode.nextSibling
                try:
                    tag_name = nextNode.name
                except AttributeError:
                    tag_name = ""
                if tag_name == "p":
                    apended_value += nextNode.text
                elif tag_name == "ul":
                    for li in nextNode.findAll('li'):
                        apended_value += li.text
                elif tag_name == "table":
                     for trd in nextNode.findAll('tr'):
                         for tdd in trd.findAll('td'):
                             apended_value += tdd.text
                else:
                    break
            qadict[section.text] = apended_value

    return qadict

if __name__=='__main__':
  app.run(debug=True, port=8080)