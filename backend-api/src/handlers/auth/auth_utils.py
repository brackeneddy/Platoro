import os
import json
import jwt
import requests

COGNITO_POOL_ID = os.environ['COGNITO_USER_POOL_ID']
COGNITO_REGION = os.environ['AWS_REGION']
COGNITO_APP_CLIENT_ID = os.environ['COGNITO_APP_CLIENT_ID']
JWKS_URL = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_POOL_ID}/.well-known/openid-configuration"

def verify_token(auth_header):
    if not auth_header or not auth_header.startswith("Bearer "):
        raise Exception("Unauthorized: Missing or malformed token")

    token = auth_header.split(" ")[1]
    headers = jwt.get_unverified_header(token)
    jwks = requests.get(JWKS_URL).json()
    key = next(k for k in jwks['keys'] if k['kid'] == headers['kid'])
    public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))

    payload = jwt.decode(token, public_key, algorithms=["RS256"], audience=COGNITO_APP_CLIENT_ID)
    return payload
