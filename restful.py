import logging
import os
import requests
import urllib
import json
from pprint import pprint
from HTMLParser import HTMLParser
from flask import Flask, jsonify, request
from flask.ext.cors import CORS
import talon
from talon import quotations
from nltk.stem.snowball import SnowballStemmer

talon.init()

with open('saved_replies.json') as json_data:
    saved_replies = json.load(json_data)
    json_data.close()

app = Flask(__name__)
CORS(app)


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def getIntercomConversation(conversation_id):
    url = "https://api.intercom.io/conversations/" + conversation_id

    headers = {
        'accept': "application/json",
        'authorization': "Basic MnljbHI5dmg6cm8tMzY2ZWM1ZWYxYTIyY2Q2MWQ4ODJkMzliY2E2MWEwY2NiOTBhZjYxMQ==",
        'cache-control': "no-cache",
    }

    response = requests.request("GET", url, headers=headers)

    return response

def getConversationBody(conversation):
    user_question = strip_tags(conversation.json()['conversation_message']['body']).lower()
    user_question = quotations.extract_from(user_question, 'text/plain')
    user_question = quotations.extract_from_plain(user_question)
    logging.warn(user_question)
    return user_question
    
def getConversationSubject(conversation):
    user_question = getConversationBody(conversation)
    

def getIntercomUserID(conversation):
    user_id = conversation.json()['user']['id']

    return user_id
    
def getIntercomUser(user_id):
    url = "https://api.intercom.io/users/" + user_id

    headers = {
        'accept': "application/json",
        'authorization': "Basic MnljbHI5dmg6cm8tMzY2ZWM1ZWYxYTIyY2Q2MWQ4ODJkMzliY2E2MWEwY2NiOTBhZjYxMQ==",
        'cache-control': "no-cache",
    }

    user = requests.request("GET", url, headers=headers)
    
    return user


@app.route('/', methods=['GET'])
def test():
    return jsonify({'message': 'It works!'})


@app.route('/reply', methods=['GET'])
def returnAll():
    return jsonify({'saved_replies': saved_replies})


@app.route('/suggested_replies/<string:conversation_id>', methods=['GET'])
def get_suggested_replies(conversation_id):
    conversation = getIntercomConversation(conversation_id)
    user_question = getConversationBody(conversation)
    # user_id = getIntercomUserID(conversation)
    # user_is_premium = getIntercomUser(user_id).json()['segments']['segments'] # need to loop through these segments and look for premium users id: 55954e0ef40cb51ffb000009

    replies_from_conversation = set()
    #if not (user_is_premium):
    #    replies_from_conversation.add('Community Redirect')

    for reply in saved_replies:
        for keyword in reply['keywords']:
            key = " " + keyword
            if (key) in user_question:
                replies_from_conversation.add(reply['title'])
    return jsonify({"matches": list(replies_from_conversation)})


@app.route('/get_conversation/<string:conversation_id>', methods=['GET'])
def get_related_topics(conversation_id):
    conversation = getIntercomConversation(conversation_id)
    subject = conversation.json()['conversation_message']['subject']
    body = getConversationBody(conversation)
    return jsonify({"subject": subject, "body": body})


if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)
