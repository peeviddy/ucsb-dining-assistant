# intent_functions.py
from init_firebase_app import init_firebase_app
from firebase_admin.firestore import firestore

def manage_allergies(req_body, res_body):
    db = init_firebase_app('firebase-auth.json')
    current_user_id = req_body.get('originalDetectIntentRequest').get('payload').get('user').get('userId')

    user_ref = db.collection('users').document(current_user_id)
    if user_ref.get().exists:
        user_data = user_ref.get().to_dict() # get snapshot
        try:
            current_user_allergies = user_data['allergies']
        except KeyError:
            current_user_allergies = []

    message_allergy_items = req_body.get('queryResult').get('parameters')['user-allergy-items']

    final_user_allergies = list(set(current_user_allergies) ^ set(message_allergy_items)) # symmetric difference
    deleted_allergies = list(set(current_user_allergies) & set(message_allergy_items)) # set intersection

    if len(final_user_allergies) > 0:
        user_ref.set({'allergies': final_user_allergies}, merge=True)
        final_user_allergies_str = ", ".join(str(allergy) for allergy in final_user_allergies)
        dialog_response = "Okay, I'll remember that you're allergic to " + final_user_allergies_str
        if len(deleted_allergies) > 0:
            deleted_allergies_str = ", ".join(str(allergy) for allergy in deleted_allergies)
            dialog_response += ", but not to " + deleted_allergies_str
    else:
        user_ref.update({'allergies': firestore.DELETE_FIELD})
        dialog_response = "Okay, I'll remember you aren't allergic to anything"

    res_body['fulfillmentText'] = dialog_response

def manage_food_prefs(req_body, res_body):
    db = init_firebase_app('firebase-auth.json')
    current_user_id = req_body.get('originalDetectIntentRequest').get('payload').get('user').get('userId')

    message_content = req_body.get('queryResult').get('parameters') # dictionary
    meal_items_str = ", ".join(str(meal) for meal in message_content['meal-items']) # if this raises keyerror then dialogflow is wrong

    user_ref = db.collection('users').document(current_user_id)

    if user_ref.get().exists:
        user_data = user_ref.get().to_dict() # get snapshot
        try:
            current_user_dislikes = user_data['dislikes']
        except KeyError:
            current_user_dislikes = []
        try:
            current_user_likes = user_data['likes']
        except KeyError:
            current_user_likes = []
        print('stored dislikes: ' + str(current_user_dislikes))
        print('stored likes: ' + str(current_user_likes))

    if 'user-sentiment-positive' in message_content.keys():
        final_user_likes = list(set(message_content['meal-items']) | set(current_user_likes)) # set union
        final_user_dislikes = list(set(current_user_dislikes) - set(message_content['meal-items']))
        dialog_response = "Okay, I'll remember that you like " + meal_items_str
    elif 'user-sentiment-negative' in message_content.keys():
        final_user_likes = list(set(current_user_likes) - set(message_content['meal-items']))
        final_user_dislikes = list(set(message_content['meal-items']) | set(current_user_dislikes)) # set union
        dialog_response = "Okay, I'll remember that you don't like " + meal_items_str
    else:
        dialog_response = "Please be more specific"

    if len(final_user_likes) > 0:
        user_ref.set({'likes': final_user_likes}, merge=True)
    else:
        user_ref.update({'likes': firestore.DELETE_FIELD})

    if len(final_user_dislikes) > 0:
        user_ref.set({'dislikes': final_user_dislikes}, merge=True)
    else:
        user_ref.update({'dislikes': firestore.DELETE_FIELD})

    res_body['fulfillmentText'] = dialog_response

def manage_philosophy(req_body, res_body):
    db = init_firebase_app('firebase-auth.json')
    current_user_id = req_body.get('originalDetectIntentRequest').get('payload').get('user').get('userId')
    user_philosophy = req_body.get('queryResult').get('parameters').get('user-philosophy')
    user_remove_philosophy = bool(req_body.get('queryResult').get('parameters').get('user-desired-operation') != "")
    user_ref = db.collection('users').document(current_user_id)
    user_data = user_ref.get()
    if user_data.exists:
        if user_remove_philosophy and user_data.to_dict()['philosophy']: # unlikely but maybe catch KeyErrors here
            user_ref.update({'philosophy': firestore.DELETE_FIELD})
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
        dialog_response = "Here's what I remember about you - "
        for key, value in user_data.items():
            print(str(key) + ': ' + str(value) + ', ')
            dialog_response += ''.join(str(key) + ' is ' + str(value) + ', ')
    elif not user_ref.get().to_dict()['saveMyData']:
        dialog_response = "You told me not to save any information about you!"
    else:
        dialog_response = "Sorry, I'm having trouble recognizing you, try again?"
    res_body['fulfillmentText'] = dialog_response
