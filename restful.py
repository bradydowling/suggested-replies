import logging
import os
import requests
import urllib
import json
import intercom
from flask import Flask, jsonify, request
from flask.ext.cors import CORS

with open('saved_replies.json') as json_data:
    saved_replies = json.load(json_data)
    json_data.close()

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def test():
    return jsonify({'message': 'It works!'})


@app.route('/reply', methods=['GET'])
def returnAll():
    return jsonify({'saved_replies': saved_replies})


@app.route('/suggested_replies/<string:conversation_id>', methods=['GET'])
def get_suggested_replies(conversation_id):
    conversation = intercom.getIntercomConversation(conversation_id)
    user_question = intercom.getConversationBody(conversation)
    user_id = intercom.getIntercomUserID(conversation)
    user_is_premium = False
    for segment in intercom.getIntercomUser(user_id).json()['segments']['segments']:
        if segment["id"] == "55954e0ef40cb51ffb000009":
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
    conversation = intercom.getIntercomConversation(conversation_id)
    subject = conversation.json()['conversation_message']['subject']
    body = intercom.getConversationBody(conversation)
    return jsonify({"subject": subject, "body": body})


if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)
