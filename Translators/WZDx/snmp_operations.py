import re
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
        return True
    else:
        err = response.content.decode("utf-8")
        if (re.search(r'Invalid index', err) is not None):
            return False
        if (re.search(r'Timeout', err) is not None):
            return False
        print(f'Failed to clear index {rsu["rsuIndex"]} for RSU {rsu["rsuTarget"]}: {err}')
        return True