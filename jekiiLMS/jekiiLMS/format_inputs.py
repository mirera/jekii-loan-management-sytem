import pycountry

#format phone number to 254706384073
def format_phone_number(phone_no, phone_code):
    # Remove any non-digit characters from the phone number
    phone_no = ''.join(filter(str.isdigit, phone_no))

    # Check if the phone number starts with a leading zero
    if phone_no.startswith('0'):
        # Remove the leading zero and prepend '254'phone_code
        #phone_no = '254' + phone_no[1:]
        phone_no = phone_code + phone_no[1:]
    else:
        # Otherwise, just prepend '254'
        phone_no = phone_code + phone_no

    return phone_no  

#get country phone code
def get_country_phone_code(country):
    try:
        country = pycountry.countries.get(alpha_2=country)
        return country.name
    except:
        return ''