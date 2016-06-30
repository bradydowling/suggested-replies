import logging
import requests
from HTMLParser import HTMLParser
import re
import talon
from talon import quotations
from nltk.corpus import stopwords
talon.init()


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
