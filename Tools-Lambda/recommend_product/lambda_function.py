import json
import boto3

#1 Connect to Bedrock Agent Runtime client
client = boto3.client("bedrock-agent-runtime")

def lambda_handler(event, context):
    #2 Get the user prompt from the incoming event
    prompt = event.get("prompt")

    #3 Query the Knowledge Base using RetrieveAndGenerate API
    response = client.retrieve_and_generate(
        input={"text": prompt},
        retrieveAndGenerateConfiguration={
           "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": "<KNOWLEDGE_BASE_ID>",  # Update with your Bedrock Knowledge Base ID
                "modelArn": "arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-pro-v1:0"
                # Model ARN Format - arn:aws:bedrock:region::foundation-model/amazon.nova-pro-v1:0

            }
        }
    )

    #4 Return the generated response
    return {
        "answer": response["output"]["text"]
    }