import json
import boto3

#1 Connect to DynamoDB using client
client = boto3.client("dynamodb")


def lambda_handler(event, context):
    #2 Get order_id from the incoming event
    order_id = event.get("order_id")

    #3 Fetch the order from DynamoDB using order_id as partition key
    response = client.get_item(
        TableName="orders",
        Key={"order_id": {"S": order_id}}
    )

    #4 Retrieve data from dictionary
    item = response["Item"]
    print(item)
    order = {
        "order_id": item["order_id"]["S"],
        "status": item["status"]["S"],
        "quantity": int(item["quantity"]["N"])
    }
    print(order)

    #5 Return order details to the calling agent
    return order
