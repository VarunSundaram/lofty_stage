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
    api = "https://management.azure.com/subscriptions/cf74786c-6831-4d2b-84c7-9a4e95d202dc/resourceGroups/bollingerposition/providers/Microsoft.Web/sites/lofty-az/functions/loftypts/properties/state?api-version=2018-11-01"
    
    data = {
        "properties":"disabled"
        }
    
    response = requests.post(f"{api}", json=data)
    if response.status_code == 200:
        logging.info('the lofty application is disabled for the comfort')
    else:
        logging.info('the lofty application is not disabled and this is worriesome')
        return
    time.sleep(30)
    
    data = {
        "properties":"enabled"
        }
    
    response = requests.post(f"{api}", json=data)
    if response.status_code == 200:
        logging.info('the lofty application is enabled for the comfort')
    else:
        logging.info('the lofty application is not enabled and this is worriesome')
    return

#if __name__ == "__main__":
#    stage_my_lofty()
