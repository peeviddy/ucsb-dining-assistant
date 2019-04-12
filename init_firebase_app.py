import os.path
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def init_firebase_app(firebase_auth_file):
    if os.path.isfile(firebase_auth_file):
        # testing locally, already authenticated
        pass
    else:
        # environment is GCP, can use default app credentials
        try:
            firebase_admin.initialize_app(credentials.ApplicationDefault(), {
                'projectId': 'dining-common-assistant'
            })
            print('initializing dining-common-assistant')
        except ValueError:
            print('dining-common-assistant already initialized')

    return firestore.client()
