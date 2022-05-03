import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import logging
import os

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


URL_DYNAMODB = 'http://%s:4566' % os.environ['LOCALSTACK_HOSTNAME']
LOGGER.info("Url: %s.", URL_DYNAMODB)
dynamodb_client = boto3.resource('dynamodb', endpoint_url=URL_DYNAMODB)


def hello(event, context):
    table = dynamodb_client.Table('my_table')

    response = table.query(
        IndexName="status_code",
        KeyConditionExpression=Key('internal_process_status_code').eq(0)
    )

    LOGGER.info("REPONSE %s", response)
    response = {
        "statusCode": 200,
        "body": {"Version": "v0.0.1"}
    }

    return response

