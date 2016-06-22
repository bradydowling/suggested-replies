import logging
import os
import requests
import urllib
from HTMLParser import HTMLParser
from flask import Flask, jsonify, request
from flask.ext.cors import CORS
"""
from pprint import pprint

with open('saved_replies.json') as data_file:    
    new_saved_replies = json.load(data_file)

pprint(new_saved_replies)
"""
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


def getIntercomQuestion(conversation_id):
    url = "https://api.intercom.io/conversations/" + conversation_id

    headers = {
        'accept': "application/json",
        'authorization': "Basic MnljbHI5dmg6cm8tMzY2ZWM1ZWYxYTIyY2Q2MWQ4ODJkMzliY2E2MWEwY2NiOTBhZjYxMQ==",
        'cache-control': "no-cache",
    }

    response = requests.request("GET", url, headers=headers)

    user_question = strip_tags(response.json()['conversation_message']['body']).lower()

    return user_question

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

    return user_question

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

saved_replies = [
    {
        'title': 'Blocked - First Response',
        'keywords': ['agar', 'blocked', 'access my account', 'unblock'],
    },
    {
        'title': 'Bug - Reported',
        'keywords': ['ran into an issue', 'usersnap feedback', 'look into this'],
    },
    {
        'title': 'Community Redirect (upsell)',
        'keywords': ['ran into an issue', 'usersnap feedback', 'look into this'],
    },
    {
        'title': 'Education',
        'keywords': ['university', 'class', 'school', 'education'],
    },
    {
        'title': 'FTP Issues',
        'keywords': ['ftp', 'mount', 'sftp'],
    },
    {
        'title': 'Invoices from Zuora',
        'keywords': ['invoices'],
    },
    {
        'title': 'Invoices from Zuora - Sent',
        'keywords': ['invoices'],
    },
    {
        'title': 'Job Applicant (Not hiring)',
        'keywords': ['cv', 'resume', 'work at Cloud9']
    },
    {
        'title': 'Monthly to yearly payments',
        'keywords': ['monthly', 'year'],
    },
    {
        'title': 'Red Alert Solved',
        'keywords': ['unable to access your workspace']
    },
    {
        'title': 'Refund - Downgrade First',
        'keywords': ['refund', 'billed', 'thanks for your purchase with cloud9 ide']
    },
    {
        'title': 'Refunded',
        'keywords': ['refund', 'billed', 'thanks for your purchase with cloud9 ide']
    },
    {
        'title': 'Share Email Reply',
        'keywords': ['I\'ve shared a workspace']
    },
    {
        'title': 'Solved (user reported)',
        'keywords': ['seems to be good', 'solved', 'ignore this', 'all fine now'],
    },
    {
        'title': 'Unstuck Workspace',
        'keywords': ['access my workspace'],
    },
    {
        'title': 'Unsubscribe',
        'keywords': ['stop sending']
    },
    {
        'title': 'Unsupported browser',
        'keywords': ['internet explorer', 'ie', 'mobile', 'iphone', 'ipad', 'android', 'tablet'],
    },
    {
        'title': 'Username change',
        'keywords': ['change my username'],
    },
    {
        'title': 'Workspace extra large',
        'keywords': ['gb'],
    },
    {
        'title': 'Yearly signup mistake',
        'keywords': ['monthly', 'year'],
    }
]


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
            if (' ' + keyword) in user_question:
                replies_from_conversation.add(reply['title'])
    logging.warn(replies_from_conversation)
    return jsonify({"matches": list(replies_from_conversation)})


@app.route('/get_conversation/<string:conversation_id>', methods=['GET'])
def get_related_topics(conversation_id):
    conversation = getIntercomConversation(conversation_id)
    subject = conversation.json()['conversation_message']['subject']
    body = getConversationBody(conversation)
    logging.warn(body)
    return jsonify({"subject": subject, "body": body})


if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)
