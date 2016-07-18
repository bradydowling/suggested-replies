import intercomlib
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, PunktSentenceTokenizer
from collections import Counter
from intercom import Admin, Conversation, Intercom, Segment, User
from HTMLParser import HTMLParser

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


def tokenize_conversation_body(cid):
    conversation = Conversation.find(id=cid)
    conversation_body = strip_tags(conversation.conversation_message.body)
    print conversation_body
    words = word_tokenize(conversation_body)
    return words


def make_search_term(cid):
    question_words = tokenize_conversation_body(cid)
    tagged = nltk.pos_tag(question_words)
    print tagged
    # whittle down all sentences to search terms
    # get top three most popular community topics from those search terms

    stop_words = set(stopwords.words("english"))
    search_term = []
    for word in question_words:
        if word not in stop_words:
            search_term.append(word)

    search_term = ' '.join(search_term)
    return search_term

def stuff_with_all_convos():
    for admin in Admin.all():
        # need to add unassigned since there will be a lot of those
        for convo in Conversation.find_all(type='admin', id=admin.id):
            print convo.id

def intercom_conversations():
    conversations = Conversation.find_all(open=True)
    print(conversations)


Intercom.app_id = '2yclr9vh'
Intercom.app_api_key = 'ro-ab6190048b6c8db0bedf55ab9249789cf1e3fe6f'


# List all admins and id's
# for admin in Admin.all():
#    print admin.name + "'s admin ID is " + admin.id
        
print make_search_term("5208390640")





"""
conversations = [] # get these from the intercom api
links = []
for conversation in conversations:
    # intercom api call to get admin messages in this conversation
    conversation_links = [] # parse this conversation to find links in conversation
    for link in conversation_links:
        links.append(link)

links_by_usage_frequency = Counter(links)
print(links_by_usage_frequency)
"""