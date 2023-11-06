import logging
import azure.functions as func
import requests
import time

app = func.FunctionApp()

@app.schedule(schedule="* 12 0/15 * * 1-5", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def lofty_staging(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')
    stage_my_lofty()
    
def stage_my_lofty():
    api = "https://management.azure.com/subscriptions/cf74786c-6831-4d2b-84c7-9a4e95d202dc/resourceGroups/bollingerposition/providers/Microsoft.Web/sites/lofty-az/functions/loftypts/properties/state?api-version=2022-09-01"

    head_data ={
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IjlHbW55RlBraGMzaE91UjIybXZTdmduTG83WSIsImtpZCI6IjlHbW55RlBraGMzaE91UjIybXZTdmduTG83WSJ9.eyJhdWQiOiJodHRwczovL21hbmFnZW1lbnQuY29yZS53aW5kb3dzLm5ldCIsImlzcyI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0LzUzNjM5MWNkLTYwNmMtNDYwYy1iOWM4LWIzOTRkODliN2E2My8iLCJpYXQiOjE2OTkyOTY1MzAsIm5iZiI6MTY5OTI5NjUzMCwiZXhwIjoxNjk5MzAwNjc2LCJhY3IiOiIxIiwiYWlvIjoiQVlRQWUvOFZBQUFBVmU0SnZoblVHekZkcFJha3M5anQ0ZHlmYm1WV1JKbnVabEdXaklIN3VIajVRQ245R0ZkZVNpRm8vRkVrVlJsL3A3T3A2VHNYOC8vTUcrUGVwVHVHeWNUcVdPNktKNDBwV05RRG5LQ2VmTk1jYzF6eDYySnFrRVM3Sk5EaGdxcTQ5SnNsL0VySFNNTitsTjlJN3lvVEh3QmhiOFhuTkVSTlM1Zlk5OG8zM0hrPSIsImFsdHNlY2lkIjoiMTpsaXZlLmNvbTowMDAzMDAwMEIxNDc1NzQyIiwiYW1yIjpbInB3ZCIsIm1mYSJdLCJhcHBpZCI6IjE4ZmJjYTE2LTIyMjQtNDVmNi04NWIwLWY3YmYyYjM5YjNmMyIsImFwcGlkYWNyIjoiMCIsImVtYWlsIjoidmFydW5zdW5kYXJhbUBvdXRsb29rLmNvbSIsImZhbWlseV9uYW1lIjoiU3VuZGFyYW0iLCJnaXZlbl9uYW1lIjoiVmFydW4ga3VtYXIiLCJncm91cHMiOlsiOWNhMTQwOTgtZGY3NC00MmE0LWFjZDYtMmMzMTg2ZGJlMGNjIl0sImlkcCI6ImxpdmUuY29tIiwiaWR0eXAiOiJ1c2VyIiwiaXBhZGRyIjoiMTYzLjExNi4yMTQuMzQiLCJuYW1lIjoiVmFydW4ga3VtYXIgU3VuZGFyYW0iLCJvaWQiOiIwNDA1MTQwOC02MjU5LTQxODgtOTQwNS0yOTYyMGE3N2FlNWQiLCJwdWlkIjoiMTAwMzIwMDJFRUMwRjQyNiIsInJoIjoiMC5BVDBBelpGalUyeGdERWE1eUxPVTJKdDZZMFpJZjNrQXV0ZFB1a1Bhd2ZqMk1CT2hBR1UuIiwic2NwIjoidXNlcl9pbXBlcnNvbmF0aW9uIiwic3ViIjoidmdWbDNWVzlsSG5YR1hVNGxPTE9aS1NoVjAyWlFKekZDaTRQMG8tTHF3SSIsInRpZCI6IjUzNjM5MWNkLTYwNmMtNDYwYy1iOWM4LWIzOTRkODliN2E2MyIsInVuaXF1ZV9uYW1lIjoibGl2ZS5jb20jdmFydW5zdW5kYXJhbUBvdXRsb29rLmNvbSIsInV0aSI6InM1OEV5N3lTbVVtSUZ4SUx0ZFhHQUEiLCJ2ZXIiOiIxLjAiLCJ3aWRzIjpbIjYyZTkwMzk0LTY5ZjUtNDIzNy05MTkwLTAxMjE3NzE0NWUxMCIsImI3OWZiZjRkLTNlZjktNDY4OS04MTQzLTc2YjE5NGU4NTUwOSJdLCJ4bXNfY2FlIjoiMSIsInhtc190Y2R0IjoxNjk0MzI2MTE2fQ.KZnmaijU7Z3Um8VrYqouuCJZunMRFeL5gpv7Neguv2jThnjld0H9-ZAYOerKaxYMDAXbDtPZcOJSfMO5j5mVHE_gIezqBFCSU0UMztEhilvsF8zpK_zLTzJRviyVadfJ8pQr_yq97QYAKEsmO8c3RyA8RIMlBNGsoGvRbGzv5qt4HgL5MIBUZv1J15hQGea8VQ90bM164vm2P7ASEA0O6FF8dJJGyRWbdnXqkd9Z-t_gv7_rdmQx_VY-wXt94x2zsc3OkuC1FSlJJBjutNMsnoGOJVuNRIOYFdQhqsaFDDF4L3k-6xgOi2RvCEZHMhvKbWkgNpPZ4IUUJm7ga49GnA",
        "Content-Type": "application/json; charset=utf-8"
        }

    data = {
        "properties":"disabled"
        }
    
    response = requests.put(f"{api}", headers=head_data, json=data)
    if response.status_code == 200:
        logging.info('the lofty application is disabled for the comfort')
    else:
        logging.info('the lofty application is not disabled and this is worriesome')
        logging.info(response)
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
    return

#if __name__ == "__main__":
#    stage_my_lofty()
