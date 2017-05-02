from pydocx import PyDocX
from flask import Flask
from pymongo import MongoClient
import sys
reload(sys)


app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client.greensheetDB


@app.route('/')
def hello_world():
    return "Hello World"



@app.route('/storeDocument')
def store_document():

    sys.setdefaultencoding('utf-8')
    # Pass in a path
    html = PyDocX.to_html(open('cmpe273-greensheet.docx', 'rb'))
    db.docCollection.insert(
        {
            "HTML": html,
            "FileName" : 'cmpe273-greensheet'
        }
    )
    return "sucess"

@app.route('/findDocument/<name>')
def find_document(name):
    data = db.docCollection.find({'FileName' : name})
    if data is not None:
        htmlContent = data.HTML




if __name__ == '__main__':
   app.run()