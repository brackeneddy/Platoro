import json
import boto3
import os

cognito_client = boto3.client('cognito-idp')

USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
CLIENT_ID = os.getenv("COGNITO_APP_CLIENT_ID")
print("DEBUG: CLIENT_ID =", CLIENT_ID)

def handler(event, context):
    body = json.loads(event["body"])

    email = body.get("email")
    password = body.get("password")

    try:
        response = cognito_client.sign_up(
            ClientId=CLIENT_ID,
            Username=email,
            Password=password,
            UserAttributes=[{"Name": "email", "Value": email}],
        )
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "User created", "userSub": response["UserSub"]})
        }

    except cognito_client.exceptions.UsernameExistsException:
        return {"statusCode": 400, "body": json.dumps({"error": "User already exists"})}
