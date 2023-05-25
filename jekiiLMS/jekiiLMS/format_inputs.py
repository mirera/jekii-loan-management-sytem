import pycountry

#format phone number to 254706384073
def format_phone_number(phone_no, phone_code):
    # Remove any non-digit characters from the phone number
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

def deformat_phone_no(phone_no, phone_code):
    phone_code_length = len(phone_code[1:]) #remove plus sign
    print(phone_code[1:])
    print(phone_code_length)
    deheaded_phone = phone_no[phone_code_length:]
    print(phone_no)
    print(deheaded_phone)
    return deheaded_phone
