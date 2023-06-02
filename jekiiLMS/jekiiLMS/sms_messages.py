import requests
import json
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from jekiiLMS.cred_process import decrypt_secret

#sms
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
#-- end

#emails
def send_email(context, template_path, from_name, from_email, subject, recipient_email, replyto_email):
    from_name_email = f'{from_name} <{from_email}>'
    template = render_to_string(template_path, context)
    e_mail = EmailMessage(
        subject,
        template,
        from_name_email, #'John Doe <john.doe@example.com>'
        [recipient_email],
        reply_to=[replyto_email,from_email],
    )
    e_mail.send(fail_silently=False)
#--end
