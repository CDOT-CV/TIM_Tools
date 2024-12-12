import json
import requests
import logging
import os
from pgquery import query_db
from tim_generator import get_action, get_effect, get_point, get_itis_codes, calculate_direction
from flask import request, Flask
from datetime import datetime

app = Flask(__name__)

log_level = os.environ.get('LOGGING_LEVEL', 'INFO')
logging.basicConfig(format='%(levelname)s:%(message)s', level=log_level)

def translate(incident_geojson):
    tims = {"timIncidentList": []}

    for feature in incident_geojson["features"]:
        tim_body = {}
        tim_body["clientId"] = feature["properties"]["id"].replace("_", "-")
        tim_body["incidentId"] = feature["properties"]["id"].replace("_", "-")
        if feature["geometry"]["type"] == "Point":
            tim_body["startPoint"] = get_point(feature["geometry"]["coordinates"])
            tim_body["endPoint"] = get_point(feature["geometry"]["coordinates"])
            tim_body["direction"] = "I"
        else:
            tim_body["startPoint"] = get_point(feature["geometry"]["coordinates"][0])
            tim_body["endPoint"] = get_point(feature["geometry"]["coordinates"][-1])
            tim_body["direction"] = calculate_direction(feature['geometry']['coordinates'])
        tim_body["route"] = feature["properties"]["routeName"].replace("_", "-")
        tim_body["highway"] = feature["properties"]["routeName"].replace("_", "-")
        tim_body["problem"] = feature["properties"]["type"]
        if (feature["properties"].get("additionalImpacts") == None):
            feature["properties"]["additionalImpacts"] = []
        tim_body["effect"] = get_effect(feature["properties"]["laneImpacts"], feature["properties"]["additionalImpacts"])
        tim_body["action"] = get_action(tim_body, feature)
        tim_body["itisCodes"] = get_itis_codes(tim_body)
        active_tim_record = active_tim(tim_body)
        if active_tim_record:
            logging.info(f"TIM already active for record: {tim_body['clientId']}")
            continue
        tims["timIncidentList"].append(tim_body)
    return tims

def active_tim(tim_body):
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
    active_tim = query_db(f"SELECT * FROM active_tim WHERE client_id LIKE '%{tim_id}%' AND tim_type_id = (SELECT tim_type_id FROM tim_type WHERE type = 'I') AND marked_for_deletion = false")
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

    result = incident_tim_translator()
    logging.info(result)

    return (result, 200, headers)

def incident_tim_translator():
    logging.info('Incident Feed TIM Translator Timer Called...')

    # Scrape the CDOT endpoint to get current list of incident features
    geoJSON =  json.loads(requests.get(f'https://{os.getenv("CDOT_FEED_ENDPOINT")}/api/v1/incidents?apiKey={os.getenv("CDOT_FEED_API_KEY")}').content.decode('utf-8'))

    tim_list = translate(geoJSON)

    logging.info('Pushing TIMs to Tim Manager...')

    errNo = 0
    return_value = requests.post(f'{os.getenv("ODE_ENDPOINT")}/incident-tim', json=tim_list)
    if (return_value.status_code == 200):
        return f'Successfully pushed {len(tim_list["timIncidentList"])} TIMs to Tim Manager'

    return f'Error pushing TIMs to Tim Manager: {return_value.content}'

# Run via flask app if running locally else just run translator directly
if (os.getenv("RUN_LOCAL") == "true"):
    if __name__ == '__main__':
        app.run()
else:
    res_str = incident_tim_translator()
    logging.info(res_str)