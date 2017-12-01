import tokens
import dog
import time
import slackHelper
from slackclient import SlackClient

#Constants
ID = tokens.id
TOKEN = tokens.key
AT_BOT = "<@" + ID + ">"

#add key value pair "string" - delegate
#make sure that your function delegate is imported
commands = {"dog":dog.dog, "goodboye":dog.goodboye, "nothx":dog.nothx}
slack = slackHelper.Slack(TOKEN, ID)
validUsers = ["jette"]
members =[]
pointUsers = {}

channelInfos = {}

def command_handler(command, channel, user):
    #default response
    response = "I'M MR MESEEKS LOOK AT ME, IDK WHAT YOU MEAN"
    
    #if valid command
    if command in commands:
        response = commands[command]()
        #if response resolves to score
        if isinstance(response, (int)):
            #add score to dict
            slack.pointUsers[user] = slack.pointUsers[user] + response
            slack.postMessage("THANKS FOR RESPONSE | SCORE " slack.pointUsers[user], user)
            return
        else:
            slack.postMessage(response)
            return
    slack.postMessage(response, user)

if __name__ == "__main__":
    if slack.client.rtm_connect():
        print ("RUNNING")
        slack.getMembers()
        while True:
            command, channel, user = slack.parseMessage(slack.client.rtm_read())
            if command and channel:
                command_handler(command, channel, user)
            time.sleep(1)