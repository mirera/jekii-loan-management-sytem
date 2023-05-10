import requests
import base64
from django.http import HttpResponse
import json
from django.conf import settings 

#function to generate access token for API consumptio
def generate_access_token():
    consumer_key = settings.CONSUMER_KEY
    consumer_secret = settings.CONSUMER_SECRET
    api_URL = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
    # Encode the consumer key and secret key in base64
    encoded_keys = base64.b64encode(f'{consumer_key}:{consumer_secret}'.encode()).decode('utf-8')

    # Make a request to the Safaricom OAuth2 API to get an access token
    headers = {
        'Authorization': f'Basic {encoded_keys}',
        'Content-Type': 'application/json'
    }
    #response = requests.get(api_URL, auth=(consumer_key, consumer_secret))
    response = requests.get(api_URL, headers=headers)
    access_token = json.loads(response.text)['access_token']
    return access_token
# -- ends


# -- function to send post request to b2c api
def disburse_loan(loan):
    access_token = generate_access_token()
    api_url = "https://api.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"
    headers = {
        "Authorization": "Bearer %s" % access_token,
        "Content-Type": "application/json"
    }
    phone_no = loan.member.phone_no
    amount = loan.approved_amount
    transaction_reference = f"DISBURSEMENT_{loan.id}"
    command_id = "BusinessPayment"
    short_code = settings.SHORT_CODE
    timeout_url = 'http://127.0.0.1:8000/loan/api/b2c-timeout'
    result_url = 'http://127.0.0.1:8000/loan/api/b2c-result'
    payload = {
        "InitiatorName": "<your initiator name>",
        "SecurityCredential": "<your security credential>",
        "CommandID": command_id,
        "Amount": amount,
        "PartyA": short_code,
        "PartyB": phone_no,
        "Remarks": "Loan Disbursement",
        "QueueTimeOutURL": timeout_url,
        "ResultURL": result_url,
        "Occasion": "Loan Disbursement",
        "OriginatorConversationID": transaction_reference
    }
    response = requests.post(api_url, json=payload, headers=headers)
    response_data = json.loads(response.text)
    return response_data
# -- ends