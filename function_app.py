import logging
import azure.functions as func
import requests
import time
import datetime

app = func.FunctionApp()

@app.schedule(schedule="* 0/14 * * * 1-5", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def lofty_staging(myTimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    hour = datetime.datetime.utcnow().hour
    if hour >= 3 and hour <= 20:
        stage_my_lofty()
    
def stage_my_lofty():
    api = "https://management.azure.com/subscriptions/cf74786c-6831-4d2b-84c7-9a4e95d202dc/resourceGroups/bollingerposition/providers/Microsoft.Web/sites/lofty-az/functions/loftypts/properties/state?api-version=2022-09-01"

    head_data ={
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IjlHbW55RlBraGMzaE91UjIybXZTdmduTG83WSIsImtpZCI6IjlHbW55RlBraGMzaE91UjIybXZTdmduTG83WSJ9.eyJhdWQiOiJodHRwczovL21hbmFnZW1lbnQuY29yZS53aW5kb3dzLm5ldCIsImlzcyI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0LzUzNjM5MWNkLTYwNmMtNDYwYy1iOWM4LWIzOTRkODliN2E2My8iLCJpYXQiOjE2OTkzMzM4ODcsIm5iZiI6MTY5OTMzMzg4NywiZXhwIjoxNjk5MzM4MDI1LCJhY3IiOiIxIiwiYWlvIjoiQVlRQWUvOFZBQUFBc3lEb0tibTFhYlVtUTcrZ2dIY0VxVDJFeUNEOU9LQUZDTmhrdXQxUXVuei81RVI5N0hKRnYvT2dCMGhTU2NhT0ZKZHdjeXdWYTZzbXZpNm0vaEh4V0I3R3E0aFF5V0hKRVQ4NzIwVVZwMnRNazM0QW5KZEpEKzZHRlhqbzFNN202MWo2SFlLRFlXQzAwYU1OeGE2OVB4bm9NZXZRZmVHakN1NWdBNlBCc1BnPSIsImFsdHNlY2lkIjoiMTpsaXZlLmNvbTowMDAzMDAwMEIxNDc1NzQyIiwiYW1yIjpbInB3ZCIsIm1mYSJdLCJhcHBpZCI6IjE4ZmJjYTE2LTIyMjQtNDVmNi04NWIwLWY3YmYyYjM5YjNmMyIsImFwcGlkYWNyIjoiMCIsImVtYWlsIjoidmFydW5zdW5kYXJhbUBvdXRsb29rLmNvbSIsImZhbWlseV9uYW1lIjoiU3VuZGFyYW0iLCJnaXZlbl9uYW1lIjoiVmFydW4ga3VtYXIiLCJncm91cHMiOlsiOWNhMTQwOTgtZGY3NC00MmE0LWFjZDYtMmMzMTg2ZGJlMGNjIl0sImlkcCI6ImxpdmUuY29tIiwiaWR0eXAiOiJ1c2VyIiwiaXBhZGRyIjoiMTYzLjExNi4yMTMuNDEiLCJuYW1lIjoiVmFydW4ga3VtYXIgU3VuZGFyYW0iLCJvaWQiOiIwNDA1MTQwOC02MjU5LTQxODgtOTQwNS0yOTYyMGE3N2FlNWQiLCJwdWlkIjoiMTAwMzIwMDJFRUMwRjQyNiIsInJoIjoiMC5BVDBBelpGalUyeGdERWE1eUxPVTJKdDZZMFpJZjNrQXV0ZFB1a1Bhd2ZqMk1CT2hBR1UuIiwic2NwIjoidXNlcl9pbXBlcnNvbmF0aW9uIiwic3ViIjoidmdWbDNWVzlsSG5YR1hVNGxPTE9aS1NoVjAyWlFKekZDaTRQMG8tTHF3SSIsInRpZCI6IjUzNjM5MWNkLTYwNmMtNDYwYy1iOWM4LWIzOTRkODliN2E2MyIsInVuaXF1ZV9uYW1lIjoibGl2ZS5jb20jdmFydW5zdW5kYXJhbUBvdXRsb29rLmNvbSIsInV0aSI6InNhd2pvWmFTZDBhWkxjNEVuVjdYQUEiLCJ2ZXIiOiIxLjAiLCJ3aWRzIjpbIjYyZTkwMzk0LTY5ZjUtNDIzNy05MTkwLTAxMjE3NzE0NWUxMCIsImI3OWZiZjRkLTNlZjktNDY4OS04MTQzLTc2YjE5NGU4NTUwOSJdLCJ4bXNfY2FlIjoiMSIsInhtc190Y2R0IjoxNjk0MzI2MTE2fQ.i9QGqtx0CYfFHpuriAJedhXYh9wgCOz3wxD6ZmkRdtH51VTfNFj9j9niK0dZmWwpw_Zkbxam6nTVGMy-M5_6C0OQEKYqpBitJy8_Ho3JmUWA1vm6TcZzs_IdvrXB-uGIzTQkzsACWikf33ybmMW4Kw0kEcjKge-2jGAjiHBxvL82gfJ-AOrrCeTAEDsbjHwgKxr136Oowv5lXreUrBoiOi1mGzePbEgtLYbKInW4stpicPzWcSruiqfhk3dgnuhOwff-cMM2dY4USpPYEpBE5grPVlfWqvCCjppLd-K1Z8HLI8aOkedqmjh0cxfTTjwMTzUv1Mj8cAIsHyBMREtSjA",
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
    return

#if __name__ == "__main__":
#    stage_my_lofty()
