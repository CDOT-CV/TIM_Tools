import json
import requests
import copy
import logging
import os
from request_wrapper import get_rsu_request, get_sdw_request
from pgquery import query_db
from tim_generator import generate_tim, get_bearing, get_geometry, get_itis_codes
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

def update_sat_region_name(request, tim_body):
    new_tim = copy.deepcopy(tim_body)
    region_name = new_tim['dataframes'][0]['regions'][0]['name']
    region_name = region_name.replace(
        'IDENTIFIER', f"SAT_{request['sdw']['recordId']}")
    if len(region_name) > 63:
        region_name = region_name[:60] + '...'
    new_tim['dataframes'][0]['regions'][0]['name'] = region_name
    return new_tim


def update_rsu_region_name(request, tim_body):
    new_tim = copy.deepcopy(tim_body)
    region_name = new_tim['dataframes'][0]['regions'][0]['name']
    region_name = region_name.replace(
        'IDENTIFIER', f"RSU_{request['rsus'][0]['rsuTarget']}")
    if len(region_name) > 63:
        region_name = region_name[:60] + '...'
    new_tim['dataframes'][0]['regions'][0]['name'] = region_name
    return new_tim

def translate_old(wzdx_geojson):
    tims = []
    duration = os.getenv("DURATION_TIME", 30)
    # if no RSUs found, drop that one
    for feature in wzdx_geojson:
        tim_body = generate_tim(feature)
        if tim_body is not None:
            for msg in tim_body["dataframes"]:
                # update start date to include milliseconds if missing
                if msg["startDateTime"][-5] != ".":
                    msg["startDateTime"] = msg["startDateTime"][:-1] + ".000Z"
                # set duration time
                msg["durationTime"] = duration

            sdx_request = get_sdw_request(feature["geometry"])
            sdx_tim = {
                "request": sdx_request,
                "tim": update_sat_region_name(sdx_request, tim_body)
            }
            tims.append(sdx_tim)

            rsu_request = get_rsu_request(feature)
            if rsu_request is not None:
                rsu_tim = {
                    "request": rsu_request,
                    "tim": update_rsu_region_name(rsu_request, tim_body)
                }
                tims.append(rsu_tim)
        else:
            logging.info(f'Failed to generate TIM for feature: {feature["id"]}')
    return tims

def translate(wzdx_geojson):
    tims = {"timRwList": []}

    for feature in wzdx_geojson:
        if (len(feature["geometry"]["coordinates"]) <= 2):
            continue
        tim_body = {}
        tim_body["direction"] = "I" if feature["properties"]["core_details"]["direction"].lower() in ["northbound", "eastbound"] else "D"
        tim_body["bearing"] = get_bearing(feature)
        tim_body["geometry"] = get_geometry(feature["geometry"]["coordinates"])
        tim_body["route"] = feature["properties"]["core_details"]["road_names"][0].replace("_", "-")
        tim_body["roadCode"] = feature["properties"]["core_details"]["name"].replace("_", "-")
        tim_body["itisCodes"] = get_itis_codes(feature)
        tim_body["action"] = ""
        tim_body["schedStart"] = datetime.strptime(feature["properties"]["start_date"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
        tim_body["schedEnd"] = datetime.strptime(feature["properties"]["end_date"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
        tim_body["highway"] = feature["properties"]["core_details"]["road_names"][0].replace("_", "-")
        tim_body["id"] = feature["properties"]["core_details"]["name"].replace("_", "-")
        tim_body["projectKey"] = 1
        tim_body["buffers"] = []
        active_tim_record = active_tim(feature, tim_body)
        if active_tim_record:
            logging.info(f"TIM already active for record: {tim_body['id']}")
            continue
        tims["timRwList"].append(tim_body)
    return tims

def active_tim(feature, tim_body):
    tim_id = tim_body["id"]
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
    active_tim = query_db(f"SELECT * FROM active_tim WHERE client_id LIKE '%{tim_id}%' AND tim_type_id = (SELECT tim_type_id FROM tim_type WHERE type = 'RW') AND marked_for_deletion = false")
    if len(active_tim) > 0:
        active_tim = active_tim[0]
        return (active_tim["direction"] == tim_body["direction"] and
            f"{active_tim['start_latitude']:.8f}" == f"{tim_body['geometry'][0]['latitude']:.8f}" and
            f"{active_tim['start_longitude']:.8f}" == f"{tim_body['geometry'][0]['longitude']:.8f}" and
            f"{active_tim['end_latitude']:.8f}" == f"{tim_body['geometry'][-1]['latitude']:.8f}" and
            f"{active_tim['end_longitude']:.8f}" == f"{tim_body['geometry'][-1]['longitude']:.8f}")

def delete_tims(feature_list):
    # delete all active TIMs that are not in the current WZDx feed
    active_tims = query_db("SELECT client_id FROM active_tim WHERE tim_type_id = (SELECT tim_type_id FROM tim_type WHERE type = 'RW') AND marked_for_deletion = false")
    active_tims = [tim["client_id"] for tim in active_tims]
    for tim in feature_list["timRwList"]:
        if tim["id"] in active_tims:
            active_tims.remove(tim["id"])
    for tim in active_tims:
        return_value = requests.delete(f'{os.getenv("ODE_ENDPOINT")}/rw-tim/{tim}', headers={"Accept": "application/json"})
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

    logging.info('Pushing TIMs to ODE...')

    errNo = 0
    return_value = requests.post(f'{os.getenv("ODE_ENDPOINT")}/rw-tim', json=tim_list)
    if (return_value.status_code == 200):
        return f'Successfully pushed {len(tim_list["timRwList"])} TIMs to ODE'

    return f'Error pushing TIMs to ODE: {return_value.content}'


# Run via flask app if running locally else just run translator directly
if (os.getenv("RUN_LOCAL") == "true"):
    if __name__ == '__main__':
        app.run()
else:
    res_str = WZDx_tim_translator()
    logging.info(res_str)