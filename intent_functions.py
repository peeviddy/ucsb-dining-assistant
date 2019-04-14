# intent_functions.py
from ucsb import ask_UCSB
from datetime import datetime
import welcome, user_fields

def return_availability(req_body, res_body):
    if req_body.get('queryResult').get('parameters').get('date-time') == "":
        print('DEBUG: no datetime provided, sending ' + datetime.now().isoformat())
        open_commons = ask_UCSB( datetime.now().isoformat() )
    else:
        print('DEBUG: provided datetime: ' + str(req_body.get('queryResult').get('parameters').get('date-time')))
        open_commons = ask_UCSB( req_body.get('queryResult').get('parameters').get('date-time') )

    if open_commons.status_code == 404:
        res_body['fulfillmentText'] = "Sorry, the dining commons are closed that day"

    elif open_commons.status_code == 200:
        dialog_response = "You can eat at "
        for i in range( len(open_commons.json())-1 ):
            dialog_response += ''.join( open_commons.json()[i].get('name') + ', ' )
        dialog_response += ''.join( "and " + open_commons.json()[len(open_commons.json())-1].get('name') )
        res_body['fulfillmentText'] = dialog_response

intent_map = {
    'Welcome Default': welcome.welcome_default,
    'Welcome Old User': welcome.welcome_old_user,

    'Manage User Name': user_fields.manage_name,
    'Manage User Allergies': user_fields.manage_allergies,
    'Manage User Likes': user_fields.manage_food_prefs,
    'Manage User Dislikes': user_fields.manage_food_prefs,
    'Manage User Philosophy': user_fields.manage_philosophy,
    'Read User Data': user_fields.read_data,

    'Return Availability': return_availability
}
