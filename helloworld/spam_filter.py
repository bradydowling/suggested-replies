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
    print(dom.prettify())
    if convo['conversation_message']['author']['type'] is "admin":
        print 'admin'
        return False
    if not convo['conversation_message']['subject']:
        print 'no subject'
        return False
    if len(paragraphs) < 2 or len(paragraphs) > 3:
        print 'paragraph numbers mismatch'
        return False
    if len(links) is not 2:
        print 'links number mismatch'
        return False
    if not paragraphs[-2].contents[-1]['href']:
        print 'no second to last paragraph link'
        return False
    if not paragraphs[-1].contents[-1]['href']:
        print 'no signature link'
        return False
    print "it's spam"
    return is_spam


def mark_spam(convo_id):
    # "should assign to quick_close and assign tag 'spam' and block user?"
    # quick_close = get quick close id
    # convo.assign(quick_close)
    print(intercom.makeNote(convo_id, "Automatically marked as spam"))
    print(intercom.assignConversation(convo_id, QUICK_CLOSE))
    return False


def filter_all_open_convos():
    for admin in intercom.getAdmins()['admins']:
        if admin['id'] is "174913":
            continue
        print(admin['name'])
        admin_convos = intercom.listConversations(admin['id'], True)
        for convo in admin_convos['conversations']:
            if convo_is_spam(convo['id']):
                mark_spam(convo['id'])

    return True


mark_spam("5433906541")