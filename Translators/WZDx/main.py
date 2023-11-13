import functions_framework
import json
import requests
import copy
import logging
import os
from request_wrapper import get_sdw_request, get_rsu_request
from tim_generator import generate_tim
from flask import request, Flask
from snmp_operations import clear_index

app = Flask(__name__)

log_level = os.environ.get('LOGGING_LEVEL', 'INFO')
logging.basicConfig(format='%(levelname)s:%(message)s', level=log_level)


def update_sat_region_name(request, tim_body):
    new_tim = copy.deepcopy(tim_body)
    region_name = new_tim['dataframes'][0]['regions'][0]['name']
    region_name = region_name.replace(
        'IDENTIFIER', f"SAT_{request['sdw']['recordId']}")
    new_tim['dataframes'][0]['regions'][0]['name'] = region_name
    return new_tim


def update_rsu_region_name(request, tim_body):
    new_tim = copy.deepcopy(tim_body)
    region_name = new_tim['dataframes'][0]['regions'][0]['name']
    region_name = region_name.replace(
        'IDENTIFIER', f"RSU_{request['rsus'][0]['rsuTarget']}")
    new_tim['dataframes'][0]['regions'][0]['name'] = region_name
    return new_tim


def translate(wzdx_geojson):
    tims = []
    duration = os.getenv("DURATION_TIME", 1800)
    # if no RSUs found, drop that one
    for feature in wzdx_geojson["features"]:
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


@functions_framework.http
def translateWzdxTIM(request):
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

    tims = translate(request.get_json())
    return (json.dumps(tims), 200, headers)

def entry(request):
    logging.info('TIM Translator Timer Called...')
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

    # Scrape the CDOT endpoint to get current list of WZDX features
    geoJSON =  json.loads(requests.get(f'https://{os.getenv("WZDX_ENDPOINT")}/api/v1/wzdx?apiKey={os.getenv("WZDX_API_KEY")}').content.decode('utf-8'))
    
    tim_list = translate(geoJSON)

    logging.info('Pushing TIMs to ODE...')

    # Clear index for each RSU before pushing to ODE
    for tim in tim_list:
        if tim["request"].get("rsus") is not None:
            rsus = tim["request"].get("rsus")
            for rsu in rsus:
                clear_index(rsu)

    errNo = 0
    for tim in tim_list:
        return_value = requests.post(f'{os.getenv("ODE_ENDPOINT")}/tim', json=tim)
        if return_value.status_code != 200:
            errNo += 1
            logging.info(f'Error pushing TIM to ODE: {return_value.content.decode("utf-8")}')
    if errNo > 1:
        logging.info(f'Failed to push {errNo} TIMs to ODE')
    logging.info(f'Successfully pushed {len(tim_list) - errNo} TIMs to ODE')

    return (f'Successfully pushed {len(tim_list) - errNo} TIMs to ODE', 200, headers)