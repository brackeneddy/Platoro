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
    code = body.get("code")
    new_password = body.get("new_password")

    try:
        cognito_client.confirm_forgot_password(
            ClientId=CLIENT_ID,
            Username=email,
            ConfirmationCode=code,
            Password=new_password
        )
        logger.info(f"Password reset confirmed for: {email}")
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Password reset successful"})
        }

    except cognito_client.exceptions.CodeMismatchException:
        logger.warning(f"Password reset confirmation failed - invalid code for: {email}")
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid confirmation code"})}
    except cognito_client.exceptions.ExpiredCodeException:
        logger.warning(f"Password reset confirmation failed - code expired for: {email}")
        return {"statusCode": 400, "body": json.dumps({"error": "Code expired"})}
    except Exception as e:
        logger.error(f"Password reset confirmation failed for {email}: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"error": "Internal server error"})}
