import time
from slackclient import SlackClient
from utils import wit_response
from DocumentAPI.handleQuestions import handle_question

BOT_TOKEN = "Your Bot Token"
CHANNEL_NAME = "general"
EXAMPLE_COMMAND = ""
# instantiate Slack & Twilio clients
slack_client = SlackClient(BOT_TOKEN)

def handle_command(command):
    categories = parse_slack_output(command)
    msg = handle_question(categories)
    return msg

def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    return wit_response(output_list)


if __name__ == "__main__":
    #READ_WEBSOCKET_DELAY = 0.5 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        slack_client.rtm_send_message(CHANNEL_NAME, "I'm ALIVE!!!")
        while True:
            for slack_message in slack_client.rtm_read():
                message = slack_message.get("text")
                user = slack_message.get("user")
                if not message or not user:
                    continue
                slack_client.rtm_send_message(CHANNEL_NAME, handle_command(message))
            #time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token")
