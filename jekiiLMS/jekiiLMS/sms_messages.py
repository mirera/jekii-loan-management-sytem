import requests
import json
from django.conf import settings

def send_sms(phone_no, message):
    url = 'https://sms.erranium.com/api/v3/sms/send'
    headers = {
        'Authorization': f'Bearer {settings.ERRANIUM_API_KEY}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    data = {
        'recipient': phone_no,
        'sender_id': 'JEKII_CPTL',
        'type': 'plain',
        'message': message
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response)
    # check the status code of the response
    if response.status_code == 200:
        # parse the JSON data from the response
        json_data = response.json()
        
        # check the status field in the JSON data
        if json_data['status'] == 'success':
            print(json_data['data'])
            return True, json_data['data']
        else:
            error_msg = json_data['message']
            print(error_msg)
            return False, error_msg
    else:
        response_data = response.json()
        message = response_data['message']
        error_msg = f"Request failed with status code {response.status_code} and this message {message} "
        print(error_msg)
        print(message)
        return False, error_msg