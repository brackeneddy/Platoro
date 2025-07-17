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
        return super().default(obj)

def handler(event, context):
    try:
        auth_header = event["headers"].get("Authorization", "")
        user_info = verify_token(auth_header)
        user_id = user_info["name"]
        body = json.loads(event['body'])

        goal_name = body.get('goal_name')
        amount = body.get('amount')

        if not user_id or not goal_name or amount is None:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing required fields"})
            }

        try:
            # Get current goal to retrieve target_amount and amount_saved
            existing = goals_table.get_item(Key={
                'user_id': user_id,
                'goal_name': goal_name
            }).get('Item')

            if not existing:
                return {
                    "statusCode": 404,
                    "body": json.dumps({"error": "Goal not found"})
                }

            new_amount_saved = decimal.Decimal(str(existing.get('amount_saved', 0))) + decimal.Decimal(str(amount))
            target_amount = decimal.Decimal(str(existing.get('target_amount', 0)))
            new_progress = new_amount_saved / target_amount if target_amount > 0 else 0

            # Update both fields
            response = goals_table.update_item(
                Key={
                    'user_id': user_id,
                    'goal_name': goal_name
                },
                UpdateExpression="SET amount_saved = :val, progress = :prog",
                ExpressionAttributeValues={
                    ":val": new_amount_saved,
                    ":prog": new_progress
                },
                ReturnValues="UPDATED_NEW"
            )

            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Goal progress updated",
                    "updated": response.get("Attributes")
                }, cls=DecimalEncoder)
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