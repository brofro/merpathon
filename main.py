import os
import tokens
import time
import requests
import dog
import random
from slackclient import SlackClient

#Constants
ID = tokens.id
TOKEN = tokens.key
AT_BOT = "<@" + ID + ">"

#add key value pair "string" - delegate
#make sure that your function delegate is imported
commands = {"dog":dog.dog, "goodboye":dog.goodboye, "nothx":dog.nothx}
slackclient = SlackClient(TOKEN)
validUsers = ["jette"]
members =[]
pointUsers = {}

channelInfos = {}

def message_parser(message):
    outlist = message
    if outlist and len(outlist) > 0:
        for out in outlist:
            #check if command is directed at bot and has text
            if out and 'text' in out:
                if channelInfos.get(out['channel']):
                    #existing dm conversation
                    return out['text'].lower(), out['channel'], out['user']
                if AT_BOT in out['text']:
                    #return command, channel, users
                    return out['text'].split(AT_BOT)[1].strip().lower(), \
                    out['channel'], out['user']
    return None, None, None

def command_handler(command, channel, user):
    #default response
    response = "I'M MR MESEEKS LOOK AT ME, IDK WHAT YOU MEAN"
    
    #if valid command
    if command in commands:
        response = commands[command]()
        #if response resolves to score
        if isinstance(response, (int)):
            #add score to dict
            pointUsers[user] = pointUsers[user] + response
            postMessage("THANKS FOR RESPONSE", user)
            return
        else:
            postMessage(response)
            return
    postMessage(response, user)

def postMessage(message, user=None):
    if user is None:
        slackclient.api_call("chat.postMessage", channel = random.choice(members), text = message, as_user=True)
    else:
        slackclient.api_call("chat.postMessage", channel = user, text = message, as_user=True)

def channelInfo(channel):
    channelInfos[channel] = slackclient.api_call("conversations.info", channel = channel).get('channel').get('is_im', False)


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
                channelInfo(channel)
                command_handler(command, channel, user)
            time.sleep(1)
            
