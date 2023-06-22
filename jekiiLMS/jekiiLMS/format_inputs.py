import pytz

#format phone number to 254706384073
def format_phone_number(phone_no, phone_code):
    # Remove any non-digit characters from the phone number
    if phone_no != None:
        phone_no = ''.join(filter(str.isdigit, phone_no))
        #remove plus sign from phone_code
        phone_code = phone_code[1:]
        # Check if the phone number starts with a leading zero
        if phone_no.startswith('0'):
            # Remove the leading zero and prepend phone_code
            phone_no = phone_code + phone_no[1:] 
        else:
            # Otherwise, just prepend phone_code
            phone_no = phone_code + phone_no

        return phone_no  

#deformat the number
def deformat_phone_no(phone_no, phone_code):
    phone_code_length = len(phone_code[1:]) #remove plus sign 
    if phone_no:
        deheaded_phone = phone_no[phone_code_length:] #remove code 700000200
        return deheaded_phone

def user_local_time(user_timezone, datetime_value): 
    # Convert the datetime to the user's timezone
    user_timezone = pytz.timezone(user_timezone)
    user_datetime = datetime_value.astimezone(user_timezone)
    return user_datetime

def to_utc(user_timezone, datetime_value):
    user_timezone = pytz.timezone(user_timezone)
    datetime_local = user_timezone.localize(datetime_value)
    datetime_utc = datetime_local.astimezone(pytz.utc)
    return datetime_utc

