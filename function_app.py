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
TENANT_ID = 'XXXXXXXXXXXXXXXX'

# Your Service Principal Sectret Password
KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXX'

# Your Client ID or App Id
APP_ID = "XXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Resource Name
RESOURCE_GROUP = "bollingerposition"

# app name
APP_NAME = "lofty-az"

# Subscription
SUBSCRIPTION = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

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
    #token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
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

    request_payload = {"username": "XXXXXXXXXXXXXXXXXXX@XXXXXXXXXX",
                       "password": "XXXXXXXXXXXX",
                       "scope": ".admin", #".default",
                       "grant_type": "client_credentials",
                       "client_id": APP_ID,
                       "client_secret": KEY}

    return requests.post(url=TOKEN_URL, data=request_payload)
    

#if __name__ == "__main__":
#    stage_my_lofty()
