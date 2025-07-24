import json
import boto3
import os
import hmac
import hashlib
import base64
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

cognito_client = boto3.client('cognito-idp')

CLIENT_ID = os.getenv("COGNITO_APP_CLIENT_ID")
CLIENT_SECRET = os.getenv("COGNITO_APP_CLIENT_SECRET")

def get_secret_hash(username):
    message = username + CLIENT_ID
    dig = hmac.new(CLIENT_SECRET.encode(), msg=message.encode(), digestmod=hashlib.sha256).digest()
    return base64.b64encode(dig).decode()

def handler(event, context):
    body = json.loads(event["body"])
    email = body.get("email")
    password = body.get("password")

    try:
        response = cognito_client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                "USERNAME": email,
                "PASSWORD": password,
                "SECRET_HASH": get_secret_hash(email)
            }
        )
        logger.info(f"User login successful: {email}")
        return {
            "statusCode": 200,
            "body": json.dumps({"token": response["AuthenticationResult"]["IdToken"]})
        }

    except cognito_client.exceptions.NotAuthorizedException:
        logger.warning(f"Login failed - incorrect credentials: {email}")
        return {"statusCode": 401, "body": json.dumps({"error": "Incorrect username or password"})}
    except Exception as e:
        logger.error(f"Login failed for {email}: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"error": "Internal server error"})}
