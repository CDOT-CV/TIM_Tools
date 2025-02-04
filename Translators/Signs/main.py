import json
import requests
import copy
import logging
import os
from flask import request, Flask
from vsl_tim_translator import translate

app = Flask(__name__)

log_level = os.environ.get('LOGGING_LEVEL', 'INFO')
logging.basicConfig(format='%(levelname)s:%(message)s', level=log_level)

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

    result = VSL_tim_translator()
    logging.info(result)

    return (result, 200, headers)

def VSL_tim_translator():
    logging.info('Signs TIM Translator Timer Called...')

    # Scrape the CDOT endpoint to get current list of signs features
    geoJSON =  json.loads(requests.get(f'https://{os.getenv("CDOT_FEED_ENDPOINT")}/api/v1/signs?apiKey={os.getenv("CDOT_FEED_API_KEY")}').content.decode('utf-8'))

    tim_list = translate(geoJSON)

    logging.info('Pushing TIMs to TIM Manager...')

    print(tim_list)

    return_value = requests.post(f'{os.getenv("TIM_MANAGER_ENDPOINT")}/vsl-tim', json=tim_list)
    if (return_value.status_code == 200):
        return f'Successfully pushed {len(tim_list["timVslList"])} VSL TIMs to TIM Manager'

    return f'Error pushing TIMs to TIM Manager: {return_value.content}'

# Run via flask app if running locally else just run translator directly
if (os.getenv("RUN_LOCAL") == "true"):
    if __name__ == '__main__':
        app.run()
else:
    res_str = VSL_tim_translator()
    logging.info(res_str)