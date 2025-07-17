import json
import os
import boto3
import decimal
from boto3.dynamodb.conditions import Key
from auth.auth_utils import verify_token

dynamodb = boto3.resource('dynamodb')
goals_table = dynamodb.Table(os.environ['GOALS_TABLE'])

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def handler(event, context):
    try:
        auth_header = event["headers"].get("Authorization", "")
        user_info = verify_token(auth_header)
        user_id = user_info["name"]
        body = json.loads(event['body'])

        if not user_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing user_id parameter"})
            }

        try:
            response = goals_table.query(
                KeyConditionExpression=Key('user_id').eq(user_id)
            )
            return {
                "statusCode": 200,
                "body": json.dumps({"goals": response.get("Items", [])}, cls=DecimalEncoder)
            }
        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": str(e)})
            }
    except Exception as e:
        return {
            "statusCode": 401,
            "body": json.dumps({"error": str(e)})
        }