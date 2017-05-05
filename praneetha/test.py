
import json
import requests

filename="cmpe273-greensheet.docx"
params = {'token': token, 'file': filename}
uri = 'https://slack.com/api/files.list'
response = json.loads(requests.get(uri, params=params).text)
if response:
    print "found"
else:
    print "not found"
