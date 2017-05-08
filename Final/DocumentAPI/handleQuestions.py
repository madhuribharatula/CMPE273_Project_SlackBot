from pymongo import MongoClient
import re
import json
categories={}
greensheet={}
client = MongoClient('mongodb://localhost:27017/')
db=client['greensheetDB']
def handle_question(categories):
    try:
        subname=categories['subjectname']
        if subname==None:
            return 'Please Enter the Course Code'
        m = re.search(r"([A-Za-z]+)([0-9]+)", subname.replace(" ", ""))
        subname = m.group(1) + " " + m.group(2)
        del  categories['subjectname']
        regx = re.compile(".*"+re.escape(subname)+".*", re.IGNORECASE)
        greensheet=db.docCollection.find_one({"Course":regx})

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
            return "Iam Sorry!!..I dont have information about this course would you like to upload it's greensheet?"
    except AttributeError:
        return "Please specify correct course code and number"
    except:
        return ""
	pass
