import os
import sys
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()
client = WebClient(token=os.getenv("SLACK_TOKEN"))
    

def send_message(msg, channel):
    try:
        if(channel[:1] != '#'):
            channel = '#'+channel
        response = client.chat_postMessage(
            channel=channel,
            text=msg
        )
        print(response)
        if(response.get('ok') and not response['ok']):
            return False, response.get('error')
        return True, None
    except SlackApiError as e:
        print('error exce:', e, 'end')
        return False, e.response.get("error")
        
        
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

    if(len(sys.argv) > 1):
        msg = sys.argv[1]
        if(len(sys.argv) > 2):
            channel = sys.argv[2]
        else:
            channel = input("Provide channel name >>> ")
    else:
        msg = input("Enter message >>> ")
        channel = input("Provide channel name >>> ")
    send_message(msg, channel)