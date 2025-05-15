import requests
import sys
import json
import pandas as pd


# Variables d'environnements

API_URL = "https://api.sewan.fr/sophia/SophiaFramework/jsongateway"
USER_AGENT = 'NCO SERVICES API'
TOKEN_API = '01b1b2952c0a7c55119f6964e03761ccdbcc68f1543e4788c0023e409ff7884d'

PERSON_ID = 95848

CUSTOMMER_ID = 902143

BILL_ID = 25013101

SEARCH_ID =2

headers = {
    'Authorization': f'bearer {TOKEN_API}',
    'User-Agent': USER_AGENT,
    'Accept-Language': 'fr_FR'
}
