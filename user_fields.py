# intent_functions.py
from init_firebase_app import init_firebase_app

def manage_allergies(req_body, res_body):
    db = init_firebase_app('firebase-auth.json')
    current_user_id = req_body.get('originalDetectIntentRequest').get('payload').get('user').get('userId')
    res_body['fulfillmentText'] = 'managing user allergies'

def manage_prefs(req_body, res_body):
    db = init_firebase_app('firebase-auth.json')
    current_user_id = req_body.get('originalDetectIntentRequest').get('payload').get('user').get('userId')
    res_body['fulfillmentText'] = "managing user preferences"

def manage_philosophy(req_body, res_body):
    db = init_firebase_app('firebase-auth.json')
    current_user_id = req_body.get('originalDetectIntentRequest').get('payload').get('user').get('userId')
    user_philosophy = req_body.get('queryResult').get('parameters').get('user-philosophy')
    user_remove_philosophy = bool(req_body.get('queryResult').get('parameters').get('user-desired-operation') != "")
    user_ref = db.collection('users').document(current_user_id)
    user_data = user_ref.get()
    if user_data.exists:
        if user_remove_philosophy and user_data.to_dict()['philosophy']: # unlikely but maybe catch KeyErrors here
            from firebase_admin.firestore import firestore
            user_ref.update({'philosophy': firestore.DELETE_FIELD })
            dialog_response = "Okay, I'll forget that you're " + str(user_data.to_dict()['philosophy'])
        else:
            user_ref.set({'philosophy': user_philosophy, 'saveMyData': True}, merge=True)
            dialog_response = "Okay, I'll remember that you're " + str(user_philosophy)
    else:
        dialog_response = "Sorry, I'm having trouble recognizing you, try again?"
    res_body['fulfillmentText'] = dialog_response

def manage_name(req_body, res_body):
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

def read_data(req_body, res_body):
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
        dialog_response = "You told me not to save any information about you!"
    else:
        dialog_response = "Sorry, I'm having trouble recognizing you, try again?"
    res_body['fulfillmentText'] = dialog_response
