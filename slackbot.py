# slackbot.py
import requests
import json
import time
from flask import Flask, request, make_response, jsonify
from slacker import Slacker
from slack_cleaner2 import *
from celery import Celery

# ...

s = SlackCleaner(OAUTH_ACCESS_TOKEN)
# list of users
s.users
# list of all kind of channels
s.conversations

slack = Slacker(BOT_USER_OAUTH_ACCESS_TOKEN)

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task()
def asyncDeleteMessage(channel):
  for msg in s.msgs(filter(match(channel), s.conversations)):
    msg.delete(replies=True, files=True)

@app.route('/delete/channel_message', methods=['GET'])
def deleteMessage():
  channel = request.args.get('channel')
  task = asyncDeleteMessage.delay(channel)
  return make_response("Delete Channel Message END", 200)