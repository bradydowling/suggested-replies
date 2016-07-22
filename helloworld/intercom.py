import logging
import requests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import json
import pprint

pp = pprint.PrettyPrinter(indent=4)


"""

78334<- id and name ->Brady Dowling
88560<- id and name ->Mutahhir Ali Hayat
88620<- id and name ->Nikolai Onken
99197<- id and name ->Harutyun
99209<- id and name ->Valeria Boshnakova
99252<- id and name ->Matthijs van Henten
99282<- id and name ->Alex
99323<- id and name ->Lennart Kats
99380<- id and name ->Tim Robinson
99464<- id and name ->Ruben Daniels
100424<- id and name ->Bas
100780<- id and name ->Fabian Jakobs
107349<- id and name ->John Dunham
177131<- id and name ->Arron Bailiss
189201<- id and name ->Justin Dray
206864<- id and name ->Dana Ivan
545686<- id and name ->Public Relations
170191<- id and name ->Red Alert
174913<- id and name ->Quick Close
488299<- id and name ->Abuse / Security
545626<- id and name ->Announcement Related
554651<- id and name ->Need Restore

"""

BRADY = "78334"



def getConversation(conversation_id):
    url = "https://api.intercom.io/conversations/" + conversation_id

    headers = {
        'accept': "application/json",
        'authorization': "Basic MnljbHI5dmg6cm8tMzY2ZWM1ZWYxYTIyY2Q2MWQ4ODJkMzliY2E2MWEwY2NiOTBhZjYxMQ==",
        'cache-control': "no-cache",
    }

    response = requests.request("GET", url, headers=headers)

    return response.json()


def listConversations(admin_id, open):
    url = 'https://api.intercom.io/conversations?type=admin&admin_id=' + admin_id + '&open=' + str(open)

    headers = {
        'accept': "application/json",
        'authorization': "Basic MnljbHI5dmg6cm8tMzY2ZWM1ZWYxYTIyY2Q2MWQ4ODJkMzliY2E2MWEwY2NiOTBhZjYxMQ==",
        'cache-control': "no-cache",
    }
    
    response = requests.request("GET", url, headers=headers)
    
    return response.json()


def getUser(user_id):
    url = "https://api.intercom.io/users/" + user_id

    headers = {
        'accept': "application/json",
        'authorization': "Basic MnljbHI5dmg6cm8tMzY2ZWM1ZWYxYTIyY2Q2MWQ4ODJkMzliY2E2MWEwY2NiOTBhZjYxMQ==",
        'cache-control': "no-cache",
    }

    response = requests.request("GET", url, headers=headers)
    
    return response.json()

def getAdmins():
    url = "https://api.intercom.io/admins/"

    headers = {
        'accept': "application/json",
        'authorization': "Basic MnljbHI5dmg6cm8tMzY2ZWM1ZWYxYTIyY2Q2MWQ4ODJkMzliY2E2MWEwY2NiOTBhZjYxMQ==",
        'cache-control': "no-cache",
    }

    response = requests.request("GET", url, headers=headers)

    return response.json()


def assignConversation(conversation_id, assignee_id):
    url = "https://api.intercom.io/conversations/" + conversation_id + "reply"

    headers = {
        'accept': "application/json",
        'authorization': "Basic MnljbHI5dmg6cm8tMzY2ZWM1ZWYxYTIyY2Q2MWQ4ODJkMzliY2E2MWEwY2NiOTBhZjYxMQ==",
        'cache-control': "no-cache",
    }
    
    data = {
      "type": "admin",
      "message_type": "assignment",
      "admin_id": BRADY,
      "assignee_id": assignee_id
    }
    
    data = json.dumps(data)

    response = requests.request("POST", url, headers=headers, data=data)

    return response.json()


def makeNote(conversation_id, body):
    url = "https://api.intercom.io/conversations/" + conversation_id + "reply"

    headers = {
        'accept': "application/json",
        'authorization': "Basic MnljbHI5dmg6cm8tMzY2ZWM1ZWYxYTIyY2Q2MWQ4ODJkMzliY2E2MWEwY2NiOTBhZjYxMQ==",
        'cache-control': "no-cache",
        'content-type': 'application/json'
    }
    
    data = {
        "type": "admin",
        "admin_id": BRADY,
        "message_type": "note",
        "body": body
    }
    
    data = json.dumps(data)

    response = requests.request("POST", url, headers=headers, data=data)

    return response.json()


def tagUsers(tag, users):
    # Users can be tagged by supplying a users array. The array contains objects identifying users by their id, email or user_id fields.
    headers = {
        'accept': "application/json",
        'content-type': 'application/json',
        'authorization': "Basic MnljbHI5dmg6cm8tMzY2ZWM1ZWYxYTIyY2Q2MWQ4ODJkMzliY2E2MWEwY2NiOTBhZjYxMQ==",
        'cache-control': "no-cache",
    }
    
    data = {
      "name": tag,
      "users": users
    }
    
    response = requests.post('https://api.intercom.io/tags', headers=headers, data=data)
    return response.json()

