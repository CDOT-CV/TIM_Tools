import json
import requests
import logging
import os
from pgquery import query_db
from tim_translator import translate_old, translate
from flask import request, Flask
from datetime import datetime

app = Flask(__name__)

log_level = os.environ.get('LOGGING_LEVEL', 'INFO')
logging.basicConfig(format='%(levelname)s:%(message)s', level=log_level)

def record_active(feature):
    startDate = datetime.strptime(feature["properties"]["start_date"], "%Y-%m-%dT%H:%M:%SZ")
    endDate = datetime.strptime(feature["properties"]["end_date"], "%Y-%m-%dT%H:%M:%SZ")
    if (datetime.utcnow().replace(tzinfo=None) - startDate.replace(tzinfo=None)).total_seconds() >= -1800 and datetime.utcnow() < endDate:
        return True
    else:
        return False

def delete_tims(feature_list):
    # delete all active TIMs that are not in the current WZDx feed
    active_tims = query_db("SELECT client_id FROM active_tim WHERE tim_type_id = (SELECT tim_type_id FROM tim_type WHERE type = 'RW') AND marked_for_deletion = false")
    active_tims = [tim["client_id"] for tim in active_tims]
    for tim in feature_list["timRwList"]:
        if tim["id"] in active_tims:
            active_tims.remove(tim["id"])
    for tim in active_tims:
        return_value = requests.delete(f'{os.getenv("TIM_MANAGER_ENDPOINT")}/rw-tim/{tim}', headers={"Accept": "application/json"})
        if (return_value.status_code != 200):
            logging.error(f'Error deleting TIM {tim["id"]}: {return_value.content}')

@app.route('/translate', methods=['POST'])
def translateWzdxTIM():
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    Note:
        For more information on how Flask integrates with Cloud
        Functions, see the `Writing HTTP functions` page.
        <https://cloud.google.com/functions/docs/writing/http#http_frameworks>
    """
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }

    tims = translate_old(request.get_json()["features"])
    return (json.dumps(tims), 200, headers)

@app.route('/', methods=['POST'])
def entry():
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    result = WZDx_tim_translator()
    logging.info(result)

    return (result, 200, headers)


def WZDx_tim_translator():
    logging.info('TIM Translator Timer Called...')

    # Scrape the CDOT endpoint to get current list of WZDX features
    geoJSON =  json.loads(requests.get(f'https://{os.getenv("WZDX_ENDPOINT")}/api/v1/wzdx?apiKey={os.getenv("WZDX_API_KEY")}').content.decode('utf-8'))

    # Filter out future records
    geoJSON = [feature for feature in geoJSON["features"] if record_active(feature) == True]

    tim_list = translate(geoJSON)

    delete_tims(tim_list)

    logging.info('Pushing TIMs to the TIM Manager...')

    return_value = requests.post(f'{os.getenv("TIM_MANAGER_ENDPOINT")}/rw-tim', json=tim_list)
    if (return_value.status_code == 200):
        return f'Successfully pushed {len(tim_list["timRwList"])} TIMs to the TIM Manager'

    return f'Error pushing TIMs to the TIM Manager: {return_value.content}'


# Run via flask app if running locally else just run translator directly
if (os.getenv("RUN_LOCAL") == "true"):
    if __name__ == '__main__':
        app.run()
else:
    res_str = WZDx_tim_translator()
    logging.info(res_str)