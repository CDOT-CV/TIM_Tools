import subprocess
import logging

def clear_index(rsu):
    '''Clears the specific RSU index'''
    cmd = ''
    index = rsu["rsuIndex"]
    if rsu["snmpProtocol"] == "NTCIP1218":
        cmd = f'snmpset -v 3 -u {rsu["rsuUsername"]} -a SHA -A {rsu["rsuPassword"]} -x AES -X {rsu["rsuPassword"]} -l authpriv {rsu["rsuTarget"]} 1.3.6.1.4.1.1206.4.2.18.3.2.1.9.{index} i 6'
    else:
        cmd = f'snmpset -v 3 -u {rsu["rsuUsername"]} -a SHA -A {rsu["rsuPassword"]} -x AES -X {rsu["rsuPassword"]} -l authpriv {rsu["rsuTarget"]} 1.0.15628.4.1.4.1.11.{index} i 6'
    output = ''
    try:
        output = subprocess.run(cmd, shell=True, capture_output=True, check=True)
        output = output.stdout.decode("utf-8").split('\n')[:-1]
        print(f'index {index} cleared for RSU {rsu["rsuTarget"]}')
    except subprocess.CalledProcessError as e:
        output = e.stderr.decode("utf-8").split('\n')[:-1]
        logging.error(f'Encountered error while running snmpset: {output[:-1]}')