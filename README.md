# CMPE 273 GreenSheetBot(Team#15)

### Requirements:

Make sure the following requirements are satisfied:
- $pip install slackclient
- $pip install pymongo
- $pip install flask
- $pip install wit
- $pip install BeautifulSoup
- $pip install werkzeug.utils

### Introduction:

Greensheetbot is a Slack chatbot responding to user questions related to the SJSU courses. User can interact with the greensheetbot through slackAPI and request for any information from the course greensheet. The interaction could be about the instructor details, class details, due dates and many more.

 A new greensheet can be uploaded by user which is then dynamically parsed on backend and get stored into mongoDB. Parsing the greensheet uploaded involves converting the greensheet document to html. The converted html file is then parsed to a set of question and answer pairs using BeatifulSoup package and loaded into database.
 
 When user requests for any information, the request message is passed to wit.ai. Wit API processes the request and removes all the unwanted words returning a group of entities back to slackAPI. Entities returned from wit are searched against the question and answer pairs stored in database. When a match a found answer is redirected to slack.
 
### Execution:

You need to clone this repository, replace Bot token and wit access key.
- Slack Bot:
  * $python greenBot.py 
- DocumentAPI:
  * $python parse_doc.py

