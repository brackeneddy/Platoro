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

USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
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
    name = body.get("name")

    try:
        response = cognito_client.sign_up(
            ClientId=CLIENT_ID,
            SecretHash=get_secret_hash(email),
            Username=email,
            Password=password,
            UserAttributes=[{"Name": "email", "Value": email},{"Name": "name", "Value": name}],
        )
        logger.info(f"User signup successful: {email}")
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "User created", "userSub": response["UserSub"]})
        }

    except cognito_client.exceptions.UsernameExistsException:
        logger.warning(f"Signup failed - user already exists: {email}")
        return {"statusCode": 400, "body": json.dumps({"error": "User already exists"})}
    except Exception as e:
        logger.error(f"Signup failed for {email}: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"error": "Internal server error"})}
