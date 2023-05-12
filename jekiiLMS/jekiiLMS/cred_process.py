from cryptography.fernet import Fernet
import base64
import os


ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')


#encrypt secret
def encrypt_secret(secret):
    f = Fernet(ENCRYPTION_KEY.encode('utf-8')) #utf-8 encode encryption key
    encrypted_secret = f.encrypt(secret.encode('utf-8')) #encrypt secret
    encrypted_secret_str = base64.b64encode(encrypted_secret).decode('utf-8') #encode to base64 and decode utf-8
    return encrypted_secret_str
# -- ends

# decrypt secret
def decrypt_secret(encrypted_secret_str):
    f = Fernet(ENCRYPTION_KEY.encode('utf-8'))
    encrypted_secret = base64.b64decode(encrypted_secret_str.encode('utf-8'))
    decrypted_secret = f.decrypt(encrypted_secret).decode('utf-8')
    print(decrypted_secret)
    return decrypted_secret
# -- ends
