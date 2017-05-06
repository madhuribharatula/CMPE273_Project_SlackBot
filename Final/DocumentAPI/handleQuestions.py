from pymongo import MongoClient
import re
import json
categories={}
greensheet={}
client = MongoClient('mongodb://localhost:27017/')
db=client['greensheetDB']
def handle_question(categories):
    print categories
    try:
        subname=categories['subjectname']
        #print subname
        if subname==None:
            return 'LOL'
        del  categories['subjectname']
        regx = re.compile(".*"+re.escape(subname)+".", re.IGNORECASE)
        greensheet=db.docCollection.find_one({"Course":regx})
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
		key = key.replace('_',' ')
                #regx = re.compile(".*"+re.escape(key)+".*", re.IGNORECASE)
		#print key
                for k in greensheet:
                  if key.lower()==k.lower():
                    print greensheet[k]
                    return k+" "+greensheet[k]
                for k in greensheet:
                  if (re.search(key,k,re.IGNORECASE)):
                    print greensheet[k]
                    return k+" "+greensheet[k]
                  #elif(re.search(key,k,re.IGNORECASE)):
                   # print greensheet[k]
                #if greensheet.has_key("Instructor"):
                    #print  greensheet[key]
                    #return greensheet[k]
        else:
            return "Iam Sorry!!..I dont have information about this subject would you like to upload it's greensheet?"
    except:
        print "got an error"
	pass
