# welcome.py
from init_firebase_app import init_firebase_app

def welcome_old_user(req_body, res_body):
    db = init_firebase_app('firebase-auth.json')
    current_user_id = req_body.get('originalDetectIntentRequest').get('payload').get('user').get('userId')
    user_ref = db.collection('users').document(current_user_id)
    user_data = user_ref.get()
    if user_data.exists:
        try:
            dialog_response = "How can I help you today, " + user_data.get('name') + "?"
        except KeyError:
            dialog_response = "How can I help you today?" # id exists, but name field doesn't
    else:
        dialog_response = "Wait a second, this current user ID doesn't exist!"

    res_body['fulfillmentText'] = dialog_response

def welcome_default(req_body, res_body):
    db = init_firebase_app('firebase-auth.json')
    current_user_id = req_body.get('originalDetectIntentRequest').get('payload').get('user').get('userId')
    # if you trigger events in a fulfillment, you can't do anything else
    if db.collection('users').document(current_user_id).get().exists:
        res_body['followupEventInput'] = {'name': 'foundOldUserEvent'}
    else:
        res_body['followupEventInput'] = {'name': 'foundNewUserEvent'}
