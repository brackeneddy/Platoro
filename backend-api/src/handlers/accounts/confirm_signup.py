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
    code = body.get("code")

    try:
        cognito_client.confirm_sign_up(
            ClientId=CLIENT_ID,
            SecretHash=get_secret_hash(email),
            Username=email,
            ConfirmationCode=code
        )
        logger.info(f"Signup confirmed for: {email}")
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Signup confirmed"})
        }
    except cognito_client.exceptions.CodeMismatchException:
        logger.warning(f"Signup confirmation failed - invalid code for: {email}")
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid confirmation code"})}
    except cognito_client.exceptions.ExpiredCodeException:
        logger.warning(f"Signup confirmation failed - code expired for: {email}")
        return {"statusCode": 400, "body": json.dumps({"error": "Code expired"})}
    except cognito_client.exceptions.UserNotFoundException:
        logger.warning(f"Signup confirmation failed - user not found: {email}")
        return {"statusCode": 404, "body": json.dumps({"error": "User not found"})}
    except Exception as e:
        logger.error(f"Signup confirmation failed for {email}: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"error": "Internal server error"})} 