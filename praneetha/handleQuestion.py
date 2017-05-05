from pymongo import MongoClient
import re
import json

client = MongoClient('mongodb://localhost:27017/')
db=client['greensheetDB']
def handle_question(categories):
    categories = json.dumps(categories)
    try:
        subname=categories['subjectname']
        print subname
        if subname==None:
            return 'LOL'
        del  categories['subjectname']
        regx = re.compile("."+re.escape(subname)+".", re.IGNORECASE)
        greensheet=db.docCollection.find_one({"Course:":regx})
        # if greensheet:
        #     #for key,value in categories.iteritems():
        #     key ='Instructor:'
        #     if greensheet.has_key('Instructor:'):
        #         print  greensheet[key]
        #         return greensheet[key]
        # else:
        #     return "Iam Sorry!!..I dont have information about this subject would you like to upload it's greensheet?"

        if greensheet:
            for key,value in categories.iteritems():
                #key ='Instructor:'
                key +=':'
                if greensheet.has_key(key):
                    print  greensheet[key]
                    return greensheet[key]
        else:
            return "Iam Sorry!!..I dont have information about this subject would you like to upload it's greensheet?"
    except:
        pass