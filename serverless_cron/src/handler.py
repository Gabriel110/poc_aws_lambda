import json
import boto3
from boto3.dynamodb.conditions import Key
import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def handler(event, context):
    urlDynamon = "http://localhost:4566"
    dynamodb = boto3.resource('dynamodb', endpoint_url=urlDynamon)

    table = dynamodb.Table('my_table')
    reponse = table.get_item(Key={'id': '1'})
    LOGGER.info("Reponse: %s", reponse)
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": {"version": 0.1}
    }

    return response
