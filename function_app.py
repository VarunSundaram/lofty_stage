import logging
import azure.functions as func
import requests
import time
import datetime

app = func.FunctionApp()

#@app.schedule(schedule="* 0/14 * * * 1-5", arg_name="myTimer", run_on_startup=True,
@app.schedule(schedule="* 0/5 * * * 1-5", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def lofty_staging(myTimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    hour = datetime.datetime.utcnow().hour
    if hour >= 3 and hour <= 24:
        stage_my_lofty()
    
def stage_my_lofty():
    token = get_access_token()
    
    if "none" in token:
        time.sleep(180)
        return
    
    api = "https://management.azure.com/subscriptions/cf74786c-6831-4d2b-84c7-9a4e95d202dc/resourceGroups/bollingerposition/providers/Microsoft.Web/sites/lofty-az/functions/loftypts/properties/state?api-version=2022-09-01"

    head_data ={
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IjlHbW55RlBraGMzaE91UjIybXZTdmduTG83WSIsImtpZCI6IjlHbW55RlBraGMzaE91UjIybXZTdmduTG83WSJ9.eyJhdWQiOiJodHRwczovL21hbmFnZW1lbnQuY29yZS53aW5kb3dzLm5ldCIsImlzcyI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0LzUzNjM5MWNkLTYwNmMtNDYwYy1iOWM4LWIzOTRkODliN2E2My8iLCJpYXQiOjE2OTkzMzk0MDksIm5iZiI6MTY5OTMzOTQwOSwiZXhwIjoxNjk5MzQzODAyLCJhY3IiOiIxIiwiYWlvIjoiQVlRQWUvOFZBQUFBd0NoVkI5d3VyT3RZYnkwcnFkNUVGbGs3dk9IN2JTejZQSnBNT0dBd0ZmWGlDKzNHS05kRVYvMHBvYTdoa1lEYTZnUE1RTkZlcVpEcjlMb3ZGY01yOVEwNDkrZ3pMVHE4MDFUUzdKaXVxVk9pMnR4aTNsZ1REQmxuOG0yMDZjTXQ3ejZBbXBOVWg4dVE4bkdiSWw4RlppU0VzTUxmdHkvcmsvRENhTm5kMjQwPSIsImFsdHNlY2lkIjoiMTpsaXZlLmNvbTowMDAzMDAwMEIxNDc1NzQyIiwiYW1yIjpbInB3ZCIsIm1mYSJdLCJhcHBpZCI6IjE4ZmJjYTE2LTIyMjQtNDVmNi04NWIwLWY3YmYyYjM5YjNmMyIsImFwcGlkYWNyIjoiMCIsImVtYWlsIjoidmFydW5zdW5kYXJhbUBvdXRsb29rLmNvbSIsImZhbWlseV9uYW1lIjoiU3VuZGFyYW0iLCJnaXZlbl9uYW1lIjoiVmFydW4ga3VtYXIiLCJncm91cHMiOlsiOWNhMTQwOTgtZGY3NC00MmE0LWFjZDYtMmMzMTg2ZGJlMGNjIl0sImlkcCI6ImxpdmUuY29tIiwiaWR0eXAiOiJ1c2VyIiwiaXBhZGRyIjoiMTYzLjExNi4yMTMuNDEiLCJuYW1lIjoiVmFydW4ga3VtYXIgU3VuZGFyYW0iLCJvaWQiOiIwNDA1MTQwOC02MjU5LTQxODgtOTQwNS0yOTYyMGE3N2FlNWQiLCJwdWlkIjoiMTAwMzIwMDJFRUMwRjQyNiIsInJoIjoiMC5BVDBBelpGalUyeGdERWE1eUxPVTJKdDZZMFpJZjNrQXV0ZFB1a1Bhd2ZqMk1CT2hBR1UuIiwic2NwIjoidXNlcl9pbXBlcnNvbmF0aW9uIiwic3ViIjoidmdWbDNWVzlsSG5YR1hVNGxPTE9aS1NoVjAyWlFKekZDaTRQMG8tTHF3SSIsInRpZCI6IjUzNjM5MWNkLTYwNmMtNDYwYy1iOWM4LWIzOTRkODliN2E2MyIsInVuaXF1ZV9uYW1lIjoibGl2ZS5jb20jdmFydW5zdW5kYXJhbUBvdXRsb29rLmNvbSIsInV0aSI6IkxNWFF6cmNGUmsyTmZzUDBteHUxQUEiLCJ2ZXIiOiIxLjAiLCJ3aWRzIjpbIjYyZTkwMzk0LTY5ZjUtNDIzNy05MTkwLTAxMjE3NzE0NWUxMCIsImI3OWZiZjRkLTNlZjktNDY4OS04MTQzLTc2YjE5NGU4NTUwOSJdLCJ4bXNfY2FlIjoiMSIsInhtc190Y2R0IjoxNjk0MzI2MTE2fQ.lfQpWBGxpzTNj2OpnIIR5zWV0qVPJjDDYTBAwS_QFXQwjcMxheoJTmCnBA8IjktNBrleAnt7cRwzYjo6SusXJnTdFp4X1WerP29fze2NvnhBHOv-kamGHX6AzblwZfTiNTJMq8xsnhRNst0HW3s9D_O8aJUv3aDOMvBznl422RQLx5brXLwpGeacCJVlD4-VIEASCi3-Si6r_lNzEq0_vSfkBE9Y2l4v4x6UXc0iX7cT6p0YHdQ2UD5OjqgReRYFLLTvyERxmxf7MAUDCNSMKQrNo7gFMlhloRDAU6V-gzFxpRRVs57QnJIASJ5KkOZLbpYt0HzcEXIPOaX1wG9mwg",
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
    
    time.sleep(270)
    return

def get_access_token():
    # Tenant ID for your Azure Subscription
    TENANT_ID = '536391cd-606c-460c-b9c8-b394d89b7a63'

    # Your Service Principal App ID
    CLIENT = '4d296fdd-a8eb-4f9c-8d71-06dc86c4c319'

    # Your Service Principal Password
    KEY = 'b19d9a53-723d-4c64-a97f-2bf29148e908'

    auth_server_url = "https://login.microsoftonline.com/{TENANT_ID}/"

    token_req_payload = {'grant_type': 'client_credentials'}

    token_response = requests.post(auth_server_url,
        data=token_req_payload, verify=False, allow_redirects=False,
        auth=(CLIENT, KEY))
        
    if token_response.status_code !=200:
        logging.info ("Failed to obtain token from the OAuth 2.0 server")
        logging.info (token_response.text)
        logging.info (token_response)
        logging.info (token_response.status_code)
        return "none"

    logging.info ("Successfuly obtained a new token")
    logging.info (token_response.text)
    return token_response["access_token"]
 


#if __name__ == "__main__":
#    stage_my_lofty()
