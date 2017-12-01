import os
import tokens
import time
import requests
import dog
import random
from slackclient import SlackClient

ID = tokens.id
TOKEN = tokens.key
AT_BOT = "<@" + ID + ">"

#add key value pair "string" - delegate
#make sure that your function delegate is imported
commands = {"dog":dog.dog, "goodboye":dog.goodboye, "nothx":dog.nothx}
slackclient = SlackClient(TOKEN)
validUsers = ["travis.cheng", "bigexecutivestud", "andrew", "jette"]
members =[]
pointUsers = {}


def message_parser(message):
    '''
    get the message, check if message contains @bot split it by command and channel
    '''
    outlist = message
    if outlist and len(outlist) > 0:
        for out in outlist:
            if out and 'text' in out and AT_BOT in out['text']:
                return out['text'].split(AT_BOT)[1].strip().lower(), \
                    out['channel'], out['user']
    return None, None, None

def command_handler(command, channel, user):
    '''
    if command is in the list of available commands, call the stored function delegate in the dictionary matching this command
    '''
    response = "I'M MR MESEEKS LOOK AT ME, IDK WHAT YOU MEAN"
    if command in commands:
        response = commands[command]()
        if isinstance(response, (int)):
            pointUsers[user] = pointUsers[user] + response
            postMessage("THANKS FOR RESPONSE", user)
        else:
            postMessage(response)
    postMessage(response, user)

def postMessage(message, user=None):
    if user is None:
        slackclient.api_call("chat.postMessage", channel = random.choice(members), text = message, as_user=True)
    else:
        slackclient.api_call("chat.postMessage", channel = user, text = message, as_user=True)


def get_members():
    call = slackclient.api_call("users.list")
    if call.get('ok'):
        users = call.get('members')
        for user in users:
            if 'name' in user and user.get('name') in validUsers:
                members.append(user.get('id'))
    
    if members:
        for member in members:
            pointUsers[member] = 0


if __name__ == "__main__":
    if slackclient.rtm_connect():
        print ("RUNNING")
        get_members()
        while True:
            command, channel, user = message_parser(slackclient.rtm_read())
            if command and channel:
                command_handler(command, channel, user)
            time.sleep(1)
            
