import json
import requests
import copy
import logging
import os
from pgquery import query_db
from tim_generator import get_geometry, get_itis_codes
from flask import request, Flask
from datetime import datetime

app = Flask(__name__)

log_level = os.environ.get('LOGGING_LEVEL', 'INFO')
logging.basicConfig(format='%(levelname)s:%(message)s', level=log_level)

def calculate_direction(coordinates):
    try:
        long_dif = coordinates[-1][0] - coordinates[0][0]
        lat_dif = coordinates[-1][1] - coordinates[0][1]
    except ValueError as e:
        return "unknown"
    except IndexError as e:
        return "unknown"

    if abs(long_dif) > abs(lat_dif):
        if long_dif > 0:
            # eastbound
            direction = "I"
        else:
            # westbound
            direction = "D"
    elif lat_dif > 0:
        # northbound
        direction = "I"
    else:
        # southbound
        direction = "D"
    return direction

def translate(rc_geojson):
    tims = {"timRcList": []}

    for feature in rc_geojson["features"]:
        if (len(feature["geometry"]["coordinates"]) <= 2):
            continue
        tim_body = {}
        tim_body["clientId"] = feature["properties"]["nameId"].replace("_", "-").replace("/", "-")
        tim_body["direction"] = calculate_direction(feature['geometry']['coordinates'])
        tim_body["segment"] = feature["properties"]["routeSegmentIndex"]
        tim_body["route"] = feature["properties"]["routeName"].replace("_", "-")
        tim_body["roadCode"] = feature["properties"]["nameId"].replace("_", "-")
        tim_body["itisCodes"] = get_itis_codes(feature)
        tim_body["geometry"] = get_geometry(feature["geometry"]["coordinates"])
        tim_body["advisory"] = ["3"]
        active_tim_record = active_tim(feature, tim_body)
        if active_tim_record:
            logging.info(f"TIM already active for record: {tim_body['clientId']}")
            continue
        tims["timRcList"].append(tim_body)
    return tims

def active_tim(feature, tim_body):
    tim_id = tim_body["clientId"]
    # if TIM has an active TIM holding record that is current & info is the same as the current TIM record, then do not update
    active_tim_holding = query_db(f"SELECT * FROM active_tim_holding WHERE client_id LIKE '%{tim_id}%'")
    if len(active_tim_holding) > 0:
        active_tim_holding = active_tim_holding[0]
        return (active_tim_holding["direction"] == tim_body["direction"] and 
            f"{active_tim_holding['start_latitude']:.8f}" == f"{tim_body['geometry'][0]['latitude']:.8f}" and 
            f"{active_tim_holding['start_longitude']:.8f}" == f"{tim_body['geometry'][0]['longitude']:.8f}" and 
            f"{active_tim_holding['end_latitude']:.8f}" == f"{tim_body['geometry'][-1]['latitude']:.8f}" and 
            f"{active_tim_holding['end_longitude']:.8f}" == f"{tim_body['geometry'][-1]['longitude']:.8f}")

    # if TIM has an active TIM record that is current & info is the same as the current TIM record, then do not update
    active_tim = query_db(f"SELECT * FROM active_tim WHERE client_id LIKE '%{tim_id}%' AND tim_type_id = (SELECT tim_type_id FROM tim_type WHERE type = 'RC') AND marked_for_deletion = false")
    if len(active_tim) > 0:
        active_tim = active_tim[0]
        return (active_tim["direction"] == tim_body["direction"] and
            f"{active_tim['start_latitude']:.8f}" == f"{tim_body['geometry'][0]['latitude']:.8f}" and
            f"{active_tim['start_longitude']:.8f}" == f"{tim_body['geometry'][0]['longitude']:.8f}" and
            f"{active_tim['end_latitude']:.8f}" == f"{tim_body['geometry'][-1]['latitude']:.8f}" and
            f"{active_tim['end_longitude']:.8f}" == f"{tim_body['geometry'][-1]['longitude']:.8f}")


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

    result = RC_tim_translator()
    logging.info(result)

    return (result, 200, headers)

def RC_tim_translator():
    logging.info('Road Conditions TIM Translator Timer Called...')

    # Scrape the CDOT endpoint to get current list of road condition features
    geoJSON =  json.loads(requests.get(f'https://{os.getenv("CDOT_FEED_ENDPOINT")}/api/v1/roadConditions?apiKey={os.getenv("CDOT_FEED_API_KEY")}').content.decode('utf-8'))

    tim_list = translate(geoJSON)

    logging.info('Pushing TIMs to ODE...')

    tim_list_copy = copy.deepcopy(tim_list)
    tim_all_clear_list = {"timRcList": [tim for tim in tim_list_copy["timRcList"] if len(tim["itisCodes"]) == 0]}
    tim_list["timRcList"] = [tim for tim in tim_list["timRcList"] if len(tim["itisCodes"]) > 0]

    errNo = 0
    return_value = requests.put(f'{os.getenv("ODE_ENDPOINT")}/submit-rc-ac', json=tim_all_clear_list)
    if (return_value.status_code == 200):
        logging.info(f'Successfully submitted {len(tim_list["timRcList"])} All Clear TIMs to ODE')

    errNo = 0
    return_value = requests.post(f'{os.getenv("ODE_ENDPOINT")}/create-update-rc-tim', json=tim_list)
    if (return_value.status_code == 200):
        return f'Successfully pushed {len(tim_list["timRcList"])} TIMs to ODE'

    return f'Error pushing TIMs to ODE: {return_value.content}'

# Run via flask app if running locally else just run translator directly
if (os.getenv("RUN_LOCAL") == "true"):
    if __name__ == '__main__':
        app.run()
else:
    res_str = RC_tim_translator()
    logging.info(res_str)