from datetime import datetime
import secrets
import base64
import pyotp


# Generate a 32-byte encryption key
key_bytes = secrets.token_bytes(32)
# Encode the key in base64 format
key_base64 = base64.b64encode(key_bytes).decode('utf-8')

# Generate a random secret key for otp
otp_secret_key = pyotp.random_base32()
