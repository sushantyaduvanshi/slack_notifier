import os
import sys
from dotenv import load_dotenv
from slack import WebClient
from slack.errors import SlackApiError

load_dotenv()
client = WebClient(token=os.getenv("SLACK_TOKEN"))
    

def send_message(msg, channel):
    try:
        response = client.chat_postMessage(
            channel=channel,
            text=msg
        )
        print(response)
    except SlackApiError as e:
        print('error :', e)
        assert e.response["error"]
        
        
def get_message_list(channel):
    response = client.conversations_list()
    for c in response.data['channels']:
        if(c['name'] == channel):
            c_id = c['id']
    response = client.conversations_history(channel = 'C018N4Z95SR')
    return response['messages']


def del_message(msg , channel):
    response = client.conversations_list()
    for c in response.data['channels']:
        if(c['name'] == channel):
            c_id = c['id']
    try:
        response = client.chat_delete(channel=c_id, ts=msg['ts'])
    except SlackApiError as e:
        print("error in deleting messgage :",e)


if(__name__ == '__main__'):

    if(len(sys.argv) > 2):

        send_message(msg=sys.argv[1], channel=sys.argv[2])

    else:

        msg = input("Enter message >>> ")
        channel = input("Provide channel name >>> ")
        send_message(msg, channel)