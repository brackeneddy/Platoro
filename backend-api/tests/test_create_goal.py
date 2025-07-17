import json
import boto3
import pytest
from moto import mock_aws
from src.handlers.goals.create_goal import handler

TABLE_NAME = "goals"

@pytest.fixture
def dynamodb_setup():
    with mock_aws():
        # Create mock table
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {"AttributeName": "user_id", "KeyType": "HASH"},
                {"AttributeName": "goal_name", "KeyType": "RANGE"}
            ],
            AttributeDefinitions=[
                {"AttributeName": "user_id", "AttributeType": "S"},
                {"AttributeName": "goal_name", "AttributeType": "S"}
            ],
            BillingMode="PAY_PER_REQUEST"
        )
        yield

def test_create_goal_success(monkeypatch, dynamodb_setup):
    monkeypatch.setenv("GOALS_TABLE", TABLE_NAME)

    event = {
        "body": json.dumps({
            "user_id": "bracken",
            "goal_name": "Bike",
            "target_amount": 1000
        })
    }

    result = handler(event, None)
    body = json.loads(result["body"])

    assert result["statusCode"] == 200
    assert body["message"] == "Goal created successfully"
