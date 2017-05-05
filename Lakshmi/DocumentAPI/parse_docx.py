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

def cleanhtml(raw_html):
  cleantext =raw_html
  if raw_html is not None:
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleanr = re.compile('{.*?}')
    cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

@app.route("/parseDocument/<value>")
def get_content(value):
    collection=db.docCollection.find({'FileName' : value})
    json_collection = []
    for doc in collection:
       json_doc = json.dumps(doc, default=json_util.default)
       json_collection.append(json_doc)
    html_content= str(json.dumps(json_collection))
    soup = BeautifulSoup(html_content)
    dict={}
    header_list = []
    para_list = []
    bullet_list = []
    print "start of the program"
    dict2 = {}
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
            dict[key1] = value
        if key2 != '':
            dict[key2] = key1

    # for hdata in soup.findAll(name = 'h2'):
    #
    #    if(hdata.text not in dict):
    #        header_list.append(cleanhtml(str(hdata)))
    # print header_list

    # for pdata in soup.findAll(name = 'p'):
    #     pdata = cleanhtml(str(pdata))
    #     #print pdata
    #     para_list.append(str(pdata))
    #
    # for ldata in soup.findAll(name = 'ul'):
    #     bullet_list.append(str(ldata))
    #
    # for hdat in header_list:
    #     print hdat
    #     for pdat in para_list:
    #
    #         print pdat
    #         if pdat in hdat:
    #             dict2[hdat] = pdat
    #             break
    #     print "############################"
    # #print dict2

    # string_content =cleanhtml(str(html_content))
    # print string_content
    # for hl in header_list:
    #     temp1 = re.search(hl + ' (.*)', string_content)
    #     print temp1

#trying to find the next sibiling after h2
    for section in soup.findAll('h2'):
        if not dict.has_key(section.text):
            nextNode = section
            print section.text
            while True:
                nextNode = nextNode.nextSibling
                try:
                    tag_name = nextNode.name
                except AttributeError:
                    tag_name = ""
                if tag_name == "p":
                    print nextNode.text

                else:
                    print "*****"
                    break

    return "hello"

if __name__=='__main__':
  app.run(debug=True, port=8080)