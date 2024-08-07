import requests
import time
import datetime
import random

SERVICE_NAME = 'Servicio1'
LOG_LEVELS = ['INFO', 'ERROR', 'DEBUG']
SERVER_URL = 'http://127.0.0.1:5000/logs'
TOKEN = 'abcd1234efgh5678ijkl'

def generate_log():
    log = {
        'timestamp': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S'),
        'service_name': SERVICE_NAME,
        'level': random.choice(LOG_LEVELS),
        'message': f'This is a log message from {SERVICE_NAME}'
    }
    return log

def send_log(log):
    headers = {'Authorization': 'Bearer ' + TOKEN}
    try:
        response = requests.post(SERVER_URL, json=log, headers=headers)
        response.raise_for_status()
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error sending log: {e}")

if __name__ == '__main__':
    while True:
        log = generate_log()
        send_log(log)
        time.sleep(5)
