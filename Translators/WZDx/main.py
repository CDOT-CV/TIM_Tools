import functions_framework
import json
from Translators.WZDx.request_wrapper import getRsuRequest, getSdwRequest
from Translators.WZDx.tim_generator import generateTim


def translate(wzdx_geojson):
    tims = []
    # TODO: generate two messages, one for sdx and one for rsu
    # if no RSUs found, drop that one
    for feature in wzdx_geojson["features"]:
        tim_body = generateTim(feature)
        if tim_body is not None:
            sdx_tim = {
                "request": getSdwRequest(feature["geometry"]),
                "tim": tim_body
            }
            rsu_tim = {
                "request": getRsuRequest(feature),
                "tim": tim_body
            }
            tims.append(sdx_tim)
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
