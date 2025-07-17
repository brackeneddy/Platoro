import boto3
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("accounts")

def save_account(user_id, item_id, access_token):
    table.put_item(Item={
        "user_id": user_id,
        "item_id": item_id,
        "access_token": access_token,
        "linked_at": datetime.utcnow().isoformat()
    })
