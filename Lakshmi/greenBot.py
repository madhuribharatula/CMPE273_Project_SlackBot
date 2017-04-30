import time
from slackclient import SlackClient
from utils import wit_response


CHANNEL_NAME = "general"
EXAMPLE_COMMAND = ""
# instantiate Slack
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def handle_command(command):
    categories = parse_slack_output(command)
    print categories
    return categories



def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            return wit_response(output)
    return None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 0.5 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        slack_client.rtm_send_message(CHANNEL_NAME, "I'm ALIVE!!!")
        while True:
            for slack_message in slack_client.rtm_read():
                message = slack_message.get("text")
                user = slack_message.get("user")
                if not message or not user:
                    continue
                slack_client.rtm_send_message(CHANNEL_NAME, handle_command(message).format(user))
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token")
