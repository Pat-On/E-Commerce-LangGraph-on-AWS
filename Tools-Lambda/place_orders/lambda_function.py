import json
import boto3
import uuid

#1 Connect to DynamoDB using low-level client
client = boto3.client("dynamodb")

def lambda_handler(event, context):
    #2 Get product_id and quantity from the incoming event
    product_id = event.get("product_id")
    quantity = event.get("quantity", 1)

    #3 Generate a unique order_id
    order_id = str(uuid.uuid4())

    #4 Write the order to DynamoDB orders table
    response = client.put_item(
        TableName="orders",
        Item={
            "order_id": {"S": order_id},
            "product_id": {"S": product_id},
            "quantity": {"N": str(quantity)},
            "status": {"S": "Pending"}
        }
    )

    #5 Return order_id to the calling agent
    return {"order_id": order_id}
