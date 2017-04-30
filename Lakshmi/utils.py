from wit import Wit

access_token = "4UKJXI2RZU4WDMBXE36LUNHY3BRLB6II"

client = Wit(access_token = access_token)

message_text = "timings of CMPE 273"

def wit_response(message_text):
    resp = client.message(message_text)
    print resp
    try:
        categories = {'subjectName':None, 'whatInfo':None}
        entities = list(resp['entities'])
        for entity in entities:
         categories[entity] = resp['entities'][entity][0]['value']
    except:
        pass
    return categories

print(wit_response(message_text))
