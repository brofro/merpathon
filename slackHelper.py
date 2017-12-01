from slackclient import SlackClient
import random

class Slack:


    def __init__(self, token, id):
        self.AT_BOT = "<@" + id + ">"
        self.client =  SlackClient(token)
        self.channelInfos = {}
        self.members = []
        self.validUsers = ["jette"]
        self.pointUsers = {}

    def getMembers(self):
        call = self.client.api_call("users.list")
        if call.get('ok'):
            users = call.get('members')
            for user in users:
                if 'name' in user and user.get('name') in self.validUsers:
                    self.members.append(user.get('id'))
        if self.members:
            for member in self.members:
                self.pointUsers[member] = 0

    def isChannelDM(self, channel):
        return self.client.api_call(
            "conversations.info",
            channel = channel
        ).get('channel').get('is_im', False)

    def postMessage(self, message, user=None):
        if user is None:
            channel = random.choice(self.members)
        else:
            channel = user
        self.client.api_call(
            "chat.postMessage",
            channel = channel,
            text = message,
            as_user = True)

    def parseMessage(self, message):
        if message and len(message) > 0:
            for out in message:
                if out and 'text' in out:
                    #if dm, store dm
                    if self.isChannelDM(out['channel']):
                        self.channelInfos[out['channel']] = True
                        self.pointUsers[out['user']] = 0
                    # if channel is stored as dm
                    if self.channelInfos.get(out['channel']):
                        return out['text'].lower(), out['channel'], out['user']
                    # if @ on non dm channel
                    if self.AT_BOT in out['text']:
                        return out['text'].split(self.AT_BOT)[1].strip().lower(), out['channel'], out['user']
        return None, None, None


