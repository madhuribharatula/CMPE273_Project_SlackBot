from pydocx import PyDocX
from flask import Flask
from pymongo import MongoClient
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


html = PyDocX.to_html(open('cmpe273-greensheet.docx', 'rb'))

app = Flask(__name__);
client = MongoClient('mongodb://localhost:27017/')
db=client['greensheetdb']

@app.route('/')
def hello_world():

   return "Hello World"

@app.route('/cmpe273')
def find_document():
    db.greesnsheetdocs.insert({
        "filename":"CMPE273",
        "HTML":html

    })
    return "Success"


if __name__=='__main__':
    app.run(debug=True, port=8080)