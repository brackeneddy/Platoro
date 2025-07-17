import boto3

table = boto3.resource("dynamodb").Table("transactions")

def save_transaction(transaction):
    table.put_item(Item=transaction)
