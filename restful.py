import logging
import os
import requests
from HTMLParser import HTMLParser
from flask import Flask, jsonify, request
from flask.ext.cors import CORS
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

saved_replies = [
    {
        'title': 'Blocked - Bots',
        'keywords': ['agar', 'blocked', 'access my account', 'unblock'],
    },
    {
        'title': 'Bug - Reported',
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
        'title': 'Solved (user reported)',
        'keywords': ['seems to be good', 'solved', 'ignore this', 'all fine now'],
    },
    {
        'title': 'Unstuck Workspace',
        'keywords': ['access my workspace'],
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
    return jsonify({'message' : 'It works!'})

@app.route('/reply', methods=['GET'])
def returnAll():
    return jsonify({'saved_replies' : saved_replies})
    
@app.route('/suggested_replies/<string:conversation_id>', methods=['GET'])
def get_suggested_replies(conversation_id):

    url = "https://api.intercom.io/conversations/" + conversation_id

    headers = {
        'accept': "application/json",
        'authorization': "Basic MnljbHI5dmg6cm8tMzY2ZWM1ZWYxYTIyY2Q2MWQ4ODJkMzliY2E2MWEwY2NiOTBhZjYxMQ==",
        'cache-control': "no-cache",
    }
    
    response = requests.request("GET", url, headers=headers)
    
    user_question = strip_tags(response.json()['conversation_message']['body']).lower()
    
    matchingReplies = set()
    for reply in saved_replies:
        for keyword in reply['keywords']:
            if (' ' + keyword) in user_question:
                matchingReplies.add(reply['title'])
    return jsonify({"matches": list(matchingReplies)})

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)), debug=True)