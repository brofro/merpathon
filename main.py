import os
import time
import requests
import dog
from slackclient import SlackClient

ID = ''
TOKEN = ''
AT_BOT = "<@" + ID + ">"
dogCommand = "dog"

slackclient = SlackClient(TOKEN)



def message_parser(message):
    outlist = message
    if outlist and len(outlist) > 0:
        for out in outlist:
            if out and 'text' in out and AT_BOT in out['text']:
                return out['text'].split(AT_BOT)[1].strip().lower(), \
                    out['channel']
    return None, None

def command_handler(command, channel):
    response = "I'M MR MESEEKS LOOK AT ME, IDK WHAT YOU MEAN"
    if command.startswith(dogCommand):
        response = dog.dog()
    slackclient.api_call("chat.postMessage", channel = channel, text = response, as_user=True)

if __name__ == "__main__":
    if slackclient.rtm_connect():
        print ("RUNNING")
        while True:
            command, channel = message_parser(slackclient.rtm_read())
            if command and channel:
                command_handler(command, channel)
            time.sleep(1)
            
