import requests
import json
from django.conf import settings
from jekiiLMS.cred_process import decrypt_secret

def send_sms(sender_id, token, phone_no, message):

    token_decrypted = decrypt_secret(token)

    url = 'https://sms.erranium.com/api/v3/sms/send'
    headers = {
        'Authorization': f'Bearer {token_decrypted}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    data = {
        'recipient': phone_no,
        'sender_id': sender_id,
        'type': 'plain',
        'message': message
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    # check the status code of the response
    if response.status_code == 200:
        # parse the JSON data from the response
        json_data = response.json()
        
        # check the status field in the JSON data
        if json_data['status'] == 'success':
            return True, json_data['data']
        else:
            error_msg = json_data['message']
            return False, error_msg
    else:
        response_data = response.json()
        message = response_data['message']
        error_msg = f"Request failed with status code {response.status_code} and this message {message} "
        return False, error_msg