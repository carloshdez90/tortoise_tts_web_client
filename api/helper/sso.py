import os
import requests
from dotenv import load_dotenv

load_dotenv()

SSO_URL=os.getenv('sso_url')
SSO_REALM=os.getenv('sso_realm')
SSO_KEY=os.getenv('sso_key')

def validate_token(token):
    url =  f'{SSO_URL}auth/realms/{SSO_REALM}/protocol/openid-connect/token/introspect'
    payload = {
        'token_type_hint': 'requesting_party_token',
        'token': token
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": f"Basic {SSO_KEY}"}

    response = requests.post(url, headers=headers, data=payload)
    return response