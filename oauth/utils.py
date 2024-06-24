from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from django.conf import settings
import requests


# https://developer.intuit.com/app/developer/qbo/docs/develop/authentication-and-authorization/oauth-2.0

CLIENT_ID = "AB3DAs4bWdhMaW8dy6FjlzCRCaPWjfLxQ5n5s69CJmJaOABddJ"
CLIENT_SECRET = "1YyVtnnqj9i4aStP006JKvkLPk2eE1z9ueNgB4Lo"
SCOPE = ["com.intuit.quickbooks.accounting"]
REDIRECT_URI = "http://localhost:8000/quickbooks/callback/"
ENVIRONMENT = "sandbox"

auth_client = AuthClient(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    environment=ENVIRONMENT,
    redirect_uri=REDIRECT_URI,
)

def get_authorization_url():
    return auth_client.get_authorization_url([Scopes.ACCOUNTING,])


def fetch_token(auth_code):
    auth_client.get_bearer_token(auth_code)
    return auth_client


def make_quickbooks_request(endpoint, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    response = requests.get(endpoint, headers=headers)
    return response
