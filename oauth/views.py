from django.shortcuts import redirect, render
from django.http import HttpResponse
from .utils import get_authorization_url, fetch_token, make_quickbooks_request
import json


def quickbooks_index(request):
    return HttpResponse("Hi :)")


def quickbooks_login(request):
    authorization_url = get_authorization_url()
    print(authorization_url)
    return redirect(authorization_url)


def quickbooks_callback(request):
    auth_code = request.GET.get('code')
    auth_state = request.GET.get('state')
    auth_realmId = request.GET.get("realmId")
    print ("auth_code:",auth_code)
    print("auth_state:",auth_state)
    print("auth_realmId:",auth_realmId)

    auth_client = fetch_token(auth_code)
    
    # Saving token in JSON file
    oauth_data = {
        "oauth_access_token": auth_client.access_token,
        "oauth_refresh_token": auth_client.refresh_token,
        "oauth_realmId": auth_realmId
    }

    # Saving data in JSON file
    with open('quickbooks_app/oauth_data.json', 'w') as file:
        json.dump(oauth_data, file)

    return HttpResponse(json.dumps(oauth_data))


def quickbooks_home(request):
    access_token = request.session.get('oauth_access_token')
    realmId = request.session.get('oauth_realmId')
    if not access_token:
        return redirect('quickbooks_login')

    endpoint = f'https://sandbox-quickbooks.api.intuit.com/v3/company/{realmId}/companyinfo/{realmId}'
    response = make_quickbooks_request(endpoint, access_token)
    return HttpResponse(response)