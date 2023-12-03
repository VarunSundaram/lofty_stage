import logging
import azure.functions as func
import requests
from requests import post
import time
import datetime
from os import getenv
import json
from msal import PublicClientApplication
import msal


app = func.FunctionApp()

# Tenant ID for your Azure Subscription
TENANT_ID = '536391cd-606c-460c-b9c8-b394d89b7a63'

# Your Service Principal Sectret Password
KEY = 'F4c8Q~mgmy33EZT.waROdQeoMBdIUdVPjjgwtbal'

# Your Client ID or App Id
APP_ID = "4e19fbe7-2e9a-402a-aebf-3b7b54a97aa6"

# Resource Name
RESOURCE_GROUP = "bollingerposition"

# app name
APP_NAME = "lofty-az"

# Subscription
SUBSCRIPTION = "cf74786c-6831-4d2b-84c7-9a4e95d202dc"

@app.schedule(schedule="* 0/30 * * * *", arg_name="myTimer", run_on_startup=True,
#@app.schedule(schedule="* 0/5 * * * 1-5", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def lofty_staging(myTimer: func.TimerRequest) -> None:
    try:
        utc_timestamp = datetime.datetime.utcnow().replace(
            tzinfo=datetime.timezone.utc).isoformat()
        if myTimer.past_due:
            logging.info('The timer is past due!')

        logging.info('Python timer trigger function ran at %s', utc_timestamp)
        hour = datetime.datetime.utcnow().hour
        if hour >= 3 and hour < 24:
            stage_my_lofty()
    except Exception as e:
        time.sleep(60)
        raise Exception(e)
    
def stage_my_lofty():
    #token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IlQxU3QtZExUdnlXUmd4Ql82NzZ1OGtyWFMtSSIsImtpZCI6IlQxU3QtZExUdnlXUmd4Ql82NzZ1OGtyWFMtSSJ9.eyJhdWQiOiJodHRwczovL21hbmFnZW1lbnQuY29yZS53aW5kb3dzLm5ldCIsImlzcyI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0LzUzNjM5MWNkLTYwNmMtNDYwYy1iOWM4LWIzOTRkODliN2E2My8iLCJpYXQiOjE3MDA1ODc0MTgsIm5iZiI6MTcwMDU4NzQxOCwiZXhwIjoxNzAwNTkxNjA5LCJhY3IiOiIxIiwiYWlvIjoiQVlRQWUvOFZBQUFBNTVJc216R080ZGpnbkI4ci9WaHZRVW1ta3pZbEJCdXRKOEpEbitjblFuMys3RUdwQmVlUDJ4QWdwUVpaYXR5dVU3VDJtNkpNbnBJbWZnU1Foa1JrRWFtRklnVUM1My8vL1NYS1JUZ1dOSW0xaTdZZEdwTCtrUUpSTVpsVGxab1RUK2NjY2M4bStZSURqU1FQTXV0N2k2MGl4d2ZORHN1SjY0WkNONzA1U2U4PSIsImFsdHNlY2lkIjoiMTpsaXZlLmNvbTowMDAzMDAwMEIxNDc1NzQyIiwiYW1yIjpbInB3ZCIsIm1mYSJdLCJhcHBpZCI6IjE4ZmJjYTE2LTIyMjQtNDVmNi04NWIwLWY3YmYyYjM5YjNmMyIsImFwcGlkYWNyIjoiMCIsImVtYWlsIjoidmFydW5zdW5kYXJhbUBvdXRsb29rLmNvbSIsImZhbWlseV9uYW1lIjoiU3VuZGFyYW0iLCJnaXZlbl9uYW1lIjoiVmFydW4ga3VtYXIiLCJncm91cHMiOlsiOWNhMTQwOTgtZGY3NC00MmE0LWFjZDYtMmMzMTg2ZGJlMGNjIl0sImlkcCI6ImxpdmUuY29tIiwiaWR0eXAiOiJ1c2VyIiwiaXBhZGRyIjoiMTYzLjExNi4yMTQuNjQiLCJuYW1lIjoiVmFydW4ga3VtYXIgU3VuZGFyYW0iLCJvaWQiOiIwNDA1MTQwOC02MjU5LTQxODgtOTQwNS0yOTYyMGE3N2FlNWQiLCJwdWlkIjoiMTAwMzIwMDJFRUMwRjQyNiIsInJoIjoiMC5BVDBBelpGalUyeGdERWE1eUxPVTJKdDZZMFpJZjNrQXV0ZFB1a1Bhd2ZqMk1CT2hBR1UuIiwic2NwIjoidXNlcl9pbXBlcnNvbmF0aW9uIiwic3ViIjoidmdWbDNWVzlsSG5YR1hVNGxPTE9aS1NoVjAyWlFKekZDaTRQMG8tTHF3SSIsInRpZCI6IjUzNjM5MWNkLTYwNmMtNDYwYy1iOWM4LWIzOTRkODliN2E2MyIsInVuaXF1ZV9uYW1lIjoibGl2ZS5jb20jdmFydW5zdW5kYXJhbUBvdXRsb29rLmNvbSIsInV0aSI6IjVQU3VrdHRQcDB5RmhtMmR0Zmp3QUEiLCJ2ZXIiOiIxLjAiLCJ3aWRzIjpbIjYyZTkwMzk0LTY5ZjUtNDIzNy05MTkwLTAxMjE3NzE0NWUxMCIsImI3OWZiZjRkLTNlZjktNDY4OS04MTQzLTc2YjE5NGU4NTUwOSJdLCJ4bXNfY2FlIjoiMSIsInhtc190Y2R0IjoxNjk0MzI2MTE2fQ.RVHZ3mk7kztgeV8GAcDvhshlQQ4hbMT5Qcf8r5Rii_G_YeNZR65oNNNbigMqbiQw0pzDLiAPneYzBa3ptPyZarfBOwE3RUtZX9inlfGz0knFRPD4NY4_ZffsmCxDzkAse9HQe_ZS7D5IqoLmgfcTbc9kAoyHhRmGaGUC2xIW-r4fs0ScVx5GzReAqnBKH9xraz9EuIAG24HEgp78FfAqjIC2Zab5kgjkNDHvx280DYrVk-BbcmpnEq6_ggrrz_VNN6YzPrsqN2jDiXfgud3nd6vCYYJBv7DlLv1mnkKy2woyxEaZ2jL_4SCJpGWTOVFEFoq_UAb2Nhnab1b66vB3iQ"
    token = get_access_token()
        
    if "none" in token:
        time.sleep(60)
        return
    
    api = f"https://management.azure.com/subscriptions/{SUBSCRIPTION}/resourceGroups/{RESOURCE_GROUP}/providers/Microsoft.Web/sites/{APP_NAME}/config/appsettings?api-version=2022-03-01"

    head_data ={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8"
        }

    data = {
        "properties":"disabled"
        }
    
    response = requests.put(f"{api}", headers=head_data, json=data)
    if response.status_code == 200:
        logging.info ('the lofty application is disabled for the comfort')
        logging.info (response.text)
    else:
        logging.info ('the lofty application is not disabled and this is worriesome')
        logging.info (response.status_code)
        logging.info (response.text)
        time.sleep(270)
        return
    
    time.sleep(30)
    
    data = {
        "properties":"enabled"
        }
    
    response = requests.put(f"{api}", headers=head_data, json=data)
    if response.status_code == 200:
        logging.info('the lofty application is enabled for the comfort')
    else:
        logging.info('the lofty application is not enabled and this is worriesome')
    logging.info (response.status_code)
    logging.info (response.text)
    
    time.sleep(120)
    return

def get_from_msal():
    
    TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    #TOKEN_URL = "https://lofty-az.azurewebsites.net/.auth/login/aad/callback"

    APP_URI = "https://lofty-az.azurewebsites.net/.auth/"

    global_token_cache = msal.TokenCache()
    
    app = PublicClientApplication(APP_ID,
                    authority=f"https://login.microsoftonline.com/{TENANT_ID}") 
    
    result = app.acquire_token_by_username_password("varunsundaram@outlook.com", "Juliet#1", scopes=["User.ReadWrite.All"])
    logging.info (result)
    if "access_token" in result:
        logging.info ("Successfuly obtained a new token")
        logging.info (result["access_token"])  # Yay!
    else:
        logging.info ("Failed to obtained a new token by MSAL")
        logging.info (result.get("error"))
        logging.info (result.get("error_description"))
        logging.info (result.get("correlation_id"))
    return result

def get_access_token():
    auth_server_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    
    appuri = "https://lofty-az.azurewebsites.net"
    APP_URI = "https://lofty-az.azurewebsites.net/.auth/"
    # secret = getenv(<name-of-secret-stored-in-env-variable>)

    ### 1ST STEP - getting auth token with App registration secret  
    auth_response = get_from_msal()
    
    if "access_token" not in auth_response:
        logging.info ("1 Failed to obtain token from MSAL")
        auth_response = authenticate()
        if auth_response.status_code !=200:
            logging.info ("2 Failed to obtain token from the OAuth 2.0 server")
            logging.info (auth_response.text)
            logging.info (auth_response)
            logging.info (auth_response.status_code)

            token_req_payload = {'grant_type': 'client_credentials'}
        
            auth_response = requests.post(auth_server_url,
                data=token_req_payload, verify=False, allow_redirects=False,
                auth=(APP_ID, KEY))
            
            if auth_response.status_code !=200:
                logging.info ("3 Failed to obtain token from the OAuth 2.0 server")
                logging.info (auth_response.text)
                logging.info (auth_response)
                logging.info (auth_response.status_code)
            
                auth_body = {}  
                auth_body['client_id'] = APP_ID
                auth_body['client_secret'] = KEY  
                auth_body['grant_type'] = 'client_credentials'  

                auth_response = post(auth_server_url, data=auth_body)
                if auth_response.status_code !=200:
                    logging.info ("4 Failed to obtain token from the OAuth 2.0 server")
                    logging.info (auth_response.text)
                    logging.info (auth_response)
                    logging.info (auth_response.status_code)
                    return "none"

    logging.info ("Successfuly obtained a new token")
    logging.info (auth_response.text)
    logging.info (auth_response)
    logging.info (auth_response.status_code)
    return auth_response.json()["access_token"]
 
def authenticate():
    TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"

    request_payload = {"username": "varunsundaram@outlook.com",
                       "password": "Juliet#1",
                       "scope": ".admin", #".default",
                       "grant_type": "client_credentials",
                       "client_id": APP_ID,
                       "client_secret": KEY}

    return requests.post(url=TOKEN_URL, data=request_payload)
    

if __name__ == "__main__":
    stage_my_lofty()
