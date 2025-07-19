import json
import boto3
import os

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
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Password reset successful"})
        }

    except cognito_client.exceptions.CodeMismatchException:
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid confirmation code"})}
    except cognito_client.exceptions.ExpiredCodeException:
        return {"statusCode": 400, "body": json.dumps({"error": "Code expired"})}
