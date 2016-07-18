import logging
import os
import requests
import urllib
import json
from flask import Flask, jsonify, request
from flask.ext.cors import CORS
from HTMLParser import HTMLParser
import re
import talon
from talon import quotations
from nltk.corpus import stopwords
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
    user_question = quotations.extract_from_html(user_question)
    logging.warn(user_question)
    return user_question


def guessConversationSubject(conversation):
    stopWords = set(stopwords.words('english'))

    user_question = getConversationBody(conversation)
    user_question = re.sub("[^a-zA-Z]", " ", user_question)
    subject = [word for word in user_question if word not in stopWords]
    return subject

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
    user_id = getIntercomUserID(conversation)
    user_is_premium = False
    premium_segment_id = "55954e0ef40cb51ffb000009"
    for segment in getIntercomUser(user_id).json()['segments']['segments']:
        # user_is_premium = True if segment["id"] == premium_segment_id else False
        if segment["id"] == premium_segment_id:
            user_is_premium = True

    suggested_replies = set()
    if not (user_is_premium):
        suggested_replies.add('Community Redirect (Upsell)')

    for reply in saved_replies:
        for keyword in reply['keywords']:
            key = " " + keyword
            if (key) in user_question:
                suggested_replies.add(reply['title'])
    
    if not suggested_replies:
        suggested_replies.add("Bug - Reported")
    return jsonify({"matches": list(suggested_replies)})


@app.route('/get_conversation/<string:conversation_id>', methods=['GET'])
def get_related_topics(conversation_id):
    conversation = getIntercomConversation(conversation_id)
    subject = conversation.json()['conversation_message']['subject']
    body = getConversationBody(conversation)
    return jsonify({"subject": subject, "body": body})


if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)
