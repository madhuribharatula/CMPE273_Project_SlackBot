from wit import Wit
	
access_token = "KDQJNST6346EUVVI7MQIKMJ2ZSVLB2BE"
	
client = Wit(access_token = access_token)
	
message_text = "what is the location of cmpe273 class"
	
def wit_response(message_text):
    resp = client.message(message_text)
    print resp
    try:
	categories = {'location':None}
	entities = list(resp['entities'])
	for entity in entities:
	  categories[entity] = resp['entities'][entity][0]['value']
    except:
	pass
    return categories
	
print(wit_response(message_text))
