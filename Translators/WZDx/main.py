import functions_framework
import json
import copy
import logging
import os
from Translators.WZDx.request_wrapper import get_rsu_request, get_sdw_request
from Translators.WZDx.tim_generator import generate_tim

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
    # if no RSUs found, drop that one
    for feature in wzdx_geojson["features"]:
        tim_body = generate_tim(feature)
        if tim_body is not None:
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
