import os
import tokens
import time
import requests
import dog
from slackclient import SlackClient

ID = tokens.id
TOKEN = tokens.key
AT_BOT = "<@" + ID + ">"

#add key value pair "string" - delegate
#make sure that your function delegate is imported
commands = {"dog":dog.dog}
slackclient = SlackClient(TOKEN)



def message_parser(message):
    '''
    get the message, check if message contains @bot split it by command and channel
    '''
    outlist = message
    if outlist and len(outlist) > 0:
        for out in outlist:
            if out and 'text' in out and AT_BOT in out['text']:
                return out['text'].split(AT_BOT)[1].strip().lower(), \
                    out['channel']
    return None, None

def command_handler(command, channel):
    '''
    if command is in the list of available commands, call the stored function delegate in the dictionary matching this command
    '''
    response = "I'M MR MESEEKS LOOK AT ME, IDK WHAT YOU MEAN"
    if command in commands:
        response = commands[command]()
    slackclient.api_call("chat.postMessage", channel = channel, text = response, as_user=True)

if __name__ == "__main__":
    if slackclient.rtm_connect():
        print ("RUNNING")
        while True:
            command, channel = message_parser(slackclient.rtm_read())
            if command and channel:
                command_handler(command, channel)
            time.sleep(1)
            
