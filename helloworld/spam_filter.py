from bs4 import BeautifulSoup
import intercom
import requests
import pprint
import os


pp = pprint.PrettyPrinter(indent=4)

QUICK_CLOSE = "174913"


def convo_is_spam(convo_id):
    is_spam = True
    convo = intercom.getConversation(convo_id)
    dom = BeautifulSoup(convo['conversation_message']['body'], 'html.parser')
    paragraphs = dom.find_all('p')
    links = dom.find_all('a')
    if convo['conversation_message']['author']['type'] is "admin":
        print convo_id + 'is not spam because it\'s from an admin'
        return False
    if not convo['conversation_message']['subject']:
        print convo_id + 'is not spam because it has no subject'
        return False
    if len(paragraphs) < 2 or len(paragraphs) > 3:
        print convo_id + 'is not spam because the paragraph numbers are off'
        return False
    if len(links) is not 2:
        print convo_id + 'is not spam because the number of links are off'
        return False
    if not paragraphs[-2].contents[-1]['href']:
        print convo_id + 'is not spam because there\'s no link in the second to last paragraph'
        return False
    if not paragraphs[-1].contents[-1]['href']:
        print convo_id + 'is not spam because it has no link in the last paragraph'
        return False
    print convo_id + " is spam"
    return is_spam


def mark_spam(convo_id):
    # "should assign to quick_close and make not that it's spam"
    intercom.makeNote(convo_id, "Filtered as spam")
    intercom.assignConversation(convo_id, QUICK_CLOSE)
    return False


def filter_all_open_convos():
    spam_count = 0
    for admin in intercom.getAdmins()['admins']:
        if admin['type'] == "team":
            continue
        print(admin['name'])
        admin_convos = intercom.listConversations(admin['id'], True)
        for convo in admin_convos['conversations']:
            if convo_is_spam(convo['id']):
                spam_count += 1
                mark_spam(convo['id'])

    return spam_count


"Just filterd " + str(filter_all_open_convos()) + " spam conversations into Quick Close for you. You're welcome ;)"