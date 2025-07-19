import json
import boto3
import os

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
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Password reset code sent"})
        }

    except cognito_client.exceptions.UserNotFoundException:
        return {"statusCode": 404, "body": json.dumps({"error": "User not found"})}
