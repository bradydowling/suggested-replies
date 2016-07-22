from chalice import Chalice
from chalice import BadRequestError

import json


from chalice import NotFoundError

import requests

app = Chalice(app_name='helloworld')
app.debug = True

CITIES_TO_STATE = {
    'seattle': 'WA',
    'portland': 'OR',
}

@app.route('/')
def index():
    return {'hello': 'world'}
    
@app.route('/cities/{city}')
def state_of_city(name):
    try:
        return {'state': CITIES_TO_STATE[name]}
    except KeyError:
        raise BadRequestError("Unknown city '%s', valid choices are: %s" % (
            name, ', '.join(CITIES_TO_STATE.keys())))

@app.route('/resource/{value}', methods=['PUT'])
def put_test(value):
    return {"value": value}

@app.route('/introspect')
def introspect():
    return app.current_request.to_dict()



@app.route('/get_convo/')
def getIntercomConversation():
    conversation_id = "5422245921"
    url = "https://api.intercom.io/conversations/" + conversation_id

    headers = {
        'accept': "application/json",
        'authorization': "Basic MnljbHI5dmg6cm8tMzY2ZWM1ZWYxYTIyY2Q2MWQ4ODJkMzliY2E2MWEwY2NiOTBhZjYxMQ==",
        'cache-control': "no-cache",
    }

    response = requests.request("GET", url, headers=headers)

    return response
