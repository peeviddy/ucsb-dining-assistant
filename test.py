from flask import Flask, request
from main import fulfill_agent
import firebase_admin
from firebase_admin import credentials

app = Flask(__name__)

# Use a service account locally
firebase_admin.initialize_app(credentials.Certificate('firebase-auth.json'))

# so u can ```flask run``` this locally and test
@app.route('/', methods=['POST'])
def webhook():
    return fulfill_agent(request)
