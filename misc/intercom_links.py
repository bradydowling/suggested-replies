import os
import json
import re
from bs4 import BeautifulSoup

urls = Counter()
convo_ids = []
# need to scan through files to get all convo ids
for id in convo_ids:
    if db[id]: # check if convo exists in database
        convo = db[id]
    else:
        convo = Conversations.find(id=id) # if it doesn't, make an api call and store the response locally as "convo"
        db[id] = convo # store convo in the database for future use
    if convo.type is "conversation" and convo.conversation_parts.type is "conversation_part.list":
        user_parts = list()
        admin_parts = list()
        for convo_part in convo.conversation_parts.conversation_parts:
            if convo_part.author.type is "user":
                user_parts.append(convo_part.body)
            else if convo_part.author.type is "admin":
                if convo_part.part_type is not "note" and convo_part.body # it could also be "close"
                admin_parts.append(convo_part.body)

    # parse admin_parts for all links and add to a dictionary
    for admin_message in admin_parts:
        soup = BeautifulSoup(user_part, 'html.parser')
        soup.find_all('a')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        for link in links:
            urls[url] += 1
