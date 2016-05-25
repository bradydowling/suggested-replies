# https://www.youtube.com/watch?v=2gunLuqHvc8
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
        'keywords': ['agar', 'blocked', 'access', 'account', 'unblock'],
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
        'title': 'Unsupported browser',
        'keywords': ['internet explorer', 'mobile', 'iphone', 'ipad', 'android'],
    },
    {
        'title': 'Username change',
        'keywords': ['change', 'mobile'],
    }
]

@app.route('/', methods=['GET'])
def test():
    return jsonify({'message' : 'It works!'})

@app.route('/reply', methods=['GET'])
def returnAll():
    return jsonify({'saved_replies' : saved_replies})

@app.route('/reply/<string:searchText>', methods=['GET'])
def getReplies(searchText):
    matchingReplies = list()
    for reply in saved_replies:
        for keyword in reply['keywords']:
            if keyword in searchText:
                matchingReplies.append(reply['title'])
    return jsonify({"matches": matchingReplies})
    
@app.route('/suggested_replies/<string:conversation_id>', methods=['GET'])
def get_suggested_replies(conversation_id):

    url = "https://api.intercom.io/conversations/" + conversation_id

    headers = {
        'accept': "application/json",
        'authorization': "Basic MnljbHI5dmg6cm8tMzY2ZWM1ZWYxYTIyY2Q2MWQ4ODJkMzliY2E2MWEwY2NiOTBhZjYxMQ==",
        'cache-control': "no-cache",
    }
    
    response = requests.request("GET", url, headers=headers)
    
    user_question = strip_tags(response.json()['conversation_message']['body'])
    
    matchingReplies = set()
    for reply in saved_replies:
        for keyword in reply['keywords']:
            if keyword in user_question:
                matchingReplies.add(reply['title'])
    return jsonify({"matches": list(matchingReplies)})






@app.route('/reply', methods=['POST'])
def newReply():
    reply = {'title' : request.json['title']}
    saved_replies.append(reply)
    return jsonify({'saved_replies' : saved_replies })
    
@app.route('/reply/<string:title>', methods=['PUT'])
def editOne(title):
    replies = [reply for reply in saved_replies if reply['title'] == title]
    replies[0]['title'] = request.json['title']
    return jsonify({'reply': replies[0]})
    
@app.route('/reply/<string:title>', methods=['DELETE'])
def removeOne(title):
    replies = [reply for reply in saved_replies if reply['title'] == title]
    saved_replies.remove(replies[0])
    return jsonify({'saved_replies' : saved_replies })

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)), debug=True)