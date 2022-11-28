import functions_framework
import json
import copy
from Translators.WZDx.request_wrapper import getRsuRequest, getSdwRequest
from Translators.WZDx.tim_generator import generateTim


def updateSatRegionName(request, tim_body):
    new_tim = copy.deepcopy(tim_body)
    region_name = new_tim['dataframes'][0]['regions'][0]['name']
    region_name = region_name.replace(
        'IDENTIFIER', f"SAT_{request['sdw']['recordId']}")
    new_tim['dataframes'][0]['regions'][0]['name'] = region_name
    return new_tim


def updateRsuRegionName(request, tim_body):
    new_tim = copy.deepcopy(tim_body)
    region_name = new_tim['dataframes'][0]['regions'][0]['name']
    region_name = region_name.replace(
        'IDENTIFIER', f"RSU_{request['rsus'][0]['rsuTarget']}")
    new_tim['dataframes'][0]['regions'][0]['name'] = region_name
    return new_tim


def translate(wzdx_geojson):
    tims = []
    # TODO: generate two messages, one for sdx and one for rsu
    # if no RSUs found, drop that one
    for feature in wzdx_geojson["features"]:
        tim_body = generateTim(feature)
        if tim_body is not None:
            sdx_request = getSdwRequest(feature["geometry"])
            sdx_tim = {
                "request": sdx_request,
                "tim": updateSatRegionName(sdx_request, tim_body)
            }
            tims.append(sdx_tim)

            rsu_request = getRsuRequest(feature)
            if rsu_request is not None:
                rsu_tim = {
                    "request": rsu_request,
                    "tim": updateRsuRegionName(rsu_request, tim_body)
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
