from secrets import UCSB_API_KEY
import requests

ENDPOINT = {
    'menu': 'https://api.ucsb.edu/dining/menu/v1/',
    'commons': 'https://api.ucsb.edu/dining/commons/v1'
}

HEADERS = {
    'accept': 'application/json',
    'ucsb-api-key': UCSB_API_KEY
}

def ask_UCSB(paramString):
    return requests.get(ENDPOINT['menu'] + paramString, HEADERS)
