import json
import os
import boto3
import decimal
from datetime import datetime
from auth.auth_utils import verify_token

dynamodb = boto3.resource('dynamodb')
goals_table = dynamodb.Table(os.environ['GOALS_TABLE'])

def handler(event, context):
    try:
        auth_header = event["headers"].get("Authorization", "")
        user_info = verify_token(auth_header)
        user_id = user_info["name"]
        body = json.loads(event['body'])

        goal_name = body.get('goal_name')
        target_amount = body.get('target_amount')
        progress = body.get('progress', 0)
        amount_saved = body.get('amount_saved', 0)

        if not user_id or not goal_name or target_amount is None:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing required fields"})
            }

        try:
            # Ensure all numerics are Decimal
            target_amount = decimal.Decimal(str(target_amount))
            progress = decimal.Decimal(str(progress))
            amount_saved = decimal.Decimal(str(amount_saved))

            item = {
                'user_id': user_id,
                'goal_name': goal_name,
                'target_amount': target_amount,
                'progress': progress,
                'amount_saved': amount_saved,
                'created_at': datetime.utcnow().isoformat()
            }

            goals_table.put_item(Item=item)

            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Goal created successfully"})
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
