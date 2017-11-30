import os
import time

from slackclient import SlackClient

ID = os.environ.get('BOT_NAME')
TOKEN = os.environ.get('SLACK_TOKEN')

slackclient = SlackClient(TOKEN)

print ("LOLOLOLOL")