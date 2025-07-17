import json
import os
import boto3
from boto3.dynamodb.conditions import Key
from auth.auth_utils import verify_token

dynamodb = boto3.resource('dynamodb')
GOALS_TABLE = os.environ['GOALS_TABLE']
table = dynamodb.Table(GOALS_TABLE)

def handler(event, context):
    try:
        auth_header = event["headers"].get("Authorization", "")
        user_info = verify_token(auth_header)
        user_id = user_info["name"]
        body = json.loads(event['body'])
        
        try:
            goal_name = body['goal_name']

            table.delete_item(
                Key={
                    'user_id': user_id,
                    'goal_name': goal_name
                }
            )

            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Goal deleted successfully'})
            }

        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }

    except Exception as e:
        return {
            "statusCode": 401,
            "body": json.dumps({"error": str(e)})
        }