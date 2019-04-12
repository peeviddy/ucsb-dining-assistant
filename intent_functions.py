# intent_functions.py
from ucsb import ask_UCSB
from datetime import datetime
from init_firebase_app import init_firebase_app

def manage_user_allergies(req_body, res_body):
    db = init_firebase_app('firebase-auth.json')
    current_user_id = req_body.get('originalDetectIntentRequest').get('payload').get('user').get('userId')
    res_body['fulfillmentText'] = 'managing user allergies'

def manage_user_prefs(req_body, res_body):
    db = init_firebase_app('firebase-auth.json')
    current_user_id = req_body.get('originalDetectIntentRequest').get('payload').get('user').get('userId')
    res_body['fulfillmentText'] = "managing user preferences"

def manage_user_philosophy(req_body, res_body):
    db = init_firebase_app('firebase-auth.json')
    current_user_id = req_body.get('originalDetectIntentRequest').get('payload').get('user').get('userId')

    user_philosophy = req_body.get('queryResult').get('parameters').get('user-philosophy')
    user_remove_philosophy = bool(req_body.get('queryResult').get('parameters').get('user-desired-operation') != "")

    user_ref = db.collection('users').document(current_user_id)
    user_data = user_ref.get()
    if user_data.exists:
        print('user_remove_philosophy: ' + str(user_remove_philosophy))
        # print(user_data.to_dict()['philosophy'])
        if user_remove_philosophy and user_data.to_dict()['philosophy']:
            from firebase_admin.firestore import firestore
            user_ref.update({'philosophy': firestore.DELETE_FIELD })
            dialog_response = "Okay, I'll forget that you're " + str(user_data.to_dict()['philosophy'])
        else:
            user_ref.set({'philosophy': user_philosophy, 'saveMyData': True}, merge=True)
            dialog_response = "Okay, I'll remember that you're " + str(user_philosophy)
    else:
        dialog_response = "Sorry, I'm having trouble recognizing you, try again?"

    res_body['fulfillmentText'] = dialog_response

def manage_user_name(req_body, res_body):
    db = init_firebase_app('firebase-auth.json')

    current_user_id = req_body.get('originalDetectIntentRequest').get('payload').get('user').get('userId')
    # this is safe since intent won't trigger unless the parameter is populated
    new_name = req_body.get('queryResult').get('parameters').get('given-name')

    user_ref = db.collection('users').document(current_user_id)
    user_data = user_ref.get()
    if user_data.exists:
        dialog_response = "Okay, I'll remember you as " + str(new_name) + " from now on"
    else:
        dialog_response = "Okay, I'll remember you, " + str(new_name)
    user_ref.set({'name': new_name, 'saveMyData': True}, merge=True)
    res_body['fulfillmentText'] = dialog_response

def read_user_data(req_body, res_body):
    db = init_firebase_app('firebase-auth.json')

    current_user_id = req_body.get('originalDetectIntentRequest').get('payload').get('user').get('userId')
    user_ref = db.collection('users').document(current_user_id)

    if user_ref.get().exists:
        user_data = user_ref.get().to_dict() # dict snapshot of current user document
        dialog_response = 'I can do that! '
        for key, value in user_data.items():
            print(str(key) + ': ' + str(value) + ', ')
            dialog_response += ''.join(str(key) + ' is ' + str(value) + ', ')
    elif not user_ref.get().to_dict()['saveMyData']:
        dialog_response = 'You told me not to save any information about you!'
    else:
        dialog_response = 'sorry, I didn\'t recognize your voice there, please try again'

    res_body['fulfillmentText'] = dialog_response

def return_availability(req_body, res_body):
    if req_body.get('queryResult').get('parameters').get('date-time') == "":
        print("no datetime provided, sending " + datetime.now().isoformat())
        open_commons = ask_UCSB( datetime.now().isoformat() )
    else:
        print("provided datetime: " + str(req_body.get('queryResult').get('parameters').get('date-time')))
        open_commons = ask_UCSB( req_body.get('queryResult').get('parameters').get('date-time') )

    if open_commons.status_code == 404:
        res_body['fulfillmentText'] = 'Sorry, the dining commons are closed that day'

    elif open_commons.status_code == 200:
        dialog_response = 'You can eat at '
        for i in range( len(open_commons.json())-1 ):
            dialog_response += ''.join( open_commons.json()[i].get('name') + ', ' )
        dialog_response += ''.join( 'and ' + open_commons.json()[len(open_commons.json())-1].get('name') )
        res_body['fulfillmentText'] = dialog_response


def welcome_old_user(req_body, res_body):
    db = init_firebase_app('firebase-auth.json')

    current_user_id = req_body.get('originalDetectIntentRequest').get('payload').get('user').get('userId')
    user_ref = db.collection('users').document(current_user_id)

    user_data = user_ref.get()
    if user_data.exists:
        try:
            dialog_response = 'How can I help you today, ' + user_data.get('name') + '?'
        except KeyError:
            dialog_response = 'How can I help you today?'
    else:
        dialog_response = 'Wait a second, this current user ID doesn\'t exist!'

    res_body['fulfillmentText'] = dialog_response

def welcome_default(req_body, res_body):
    db = init_firebase_app('firebase-auth.json')
    current_user_id = req_body.get('originalDetectIntentRequest').get('payload').get('user').get('userId')
    # basically if you trigger events in a fulfillment, you can't do anything else
    if db.collection('users').document(current_user_id).get().exists:
        res_body['followupEventInput'] = {'name': 'foundOldUserEvent'}
    else:
        res_body['followupEventInput'] = {'name': 'foundNewUserEvent'}

intent_map = {
    'Welcome Default': welcome_default,
    'Welcome Old User': welcome_old_user,

    'Manage User Name': manage_user_name,
    'Manage User Allergies': manage_user_allergies,
    'Manage User Preferences': manage_user_prefs,
    'Manage User Philosophy': manage_user_philosophy,

    'Read User Data': read_user_data,
    # 'Read Menu': read_menu,
    'Return Availability': return_availability
}
