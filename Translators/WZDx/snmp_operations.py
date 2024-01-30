import requests
import json
import os

def clear_index(rsu):
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({
        'rsuTarget': rsu['rsuTarget'],
        'rsuRetries': rsu['rsuRetries'],
        'rsuTimeout': rsu['rsuTimeout'],
        'rsuIndex': rsu['rsuIndex'],
        'snmpProtocol': rsu['snmpProtocol'],
        'rsuUsername': rsu['rsuUsername'],
        'rsuPassword': rsu['rsuPassword']
    })
    params = {'index': str(rsu['rsuIndex'])}
    
    response = requests.delete(f'{os.getenv("ODE_ENDPOINT")}/tim', data=payload, headers=headers, params=params)
    
    if response.status_code == 200:
        print(f'Index {rsu["rsuIndex"]} cleared for RSU {rsu["rsuTarget"]}')
    else:
        print(f'Failed to clear index {rsu["rsuIndex"]} for RSU {rsu["rsuTarget"]}: {response.content.decode("utf-8")}')