import json
import boto3
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

cognito_client = boto3.client("cognito-idp")
CLIENT_ID = os.getenv("COGNITO_APP_CLIENT_ID")

def handler(event, context):
    body = json.loads(event["body"])
    email = body.get("email")

    try:
        cognito_client.forgot_password(
            ClientId=CLIENT_ID,
            Username=email
        )
        logger.info(f"Password reset code sent to: {email}")
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Password reset code sent"})
        }

    except cognito_client.exceptions.UserNotFoundException:
        logger.warning(f"Password reset requested for non-existent user: {email}")
        return {"statusCode": 404, "body": json.dumps({"error": "User not found"})}
    except Exception as e:
        logger.error(f"Password reset request failed for {email}: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"error": "Internal server error"})}
