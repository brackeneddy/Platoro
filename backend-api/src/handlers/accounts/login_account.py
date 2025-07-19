import json
import boto3
import os

cognito_client = boto3.client('cognito-idp')

CLIENT_ID = os.getenv("COGNITO_APP_CLIENT_ID")

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
                "PASSWORD": password
            }
        )
        return {
            "statusCode": 200,
            "body": json.dumps({"token": response["AuthenticationResult"]["IdToken"]})
        }

    except cognito_client.exceptions.NotAuthorizedException:
        return {"statusCode": 401, "body": json.dumps({"error": "Incorrect username or password"})}
