import boto3
from datetime import datetime

table = boto3.resource("dynamodb").Table("goals")

def create_goal(user_id, name, target_amount):
    table.put_item(Item={
        "user_id": user_id,
        "goal_name": name,
        "target_amount": target_amount,
        "progress": 0,
        "created_at": datetime.utcnow().isoformat()
    })
