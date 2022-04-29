import logging
import boto3
import json
from botocore.exceptions import ClientError
import os
import uuid
import datetime

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def sns_event(clienteId, chargebackId):
    ts = datetime.datetime.now().timestamp()
    uuids =  uuid.uuid4().__str__()
    return {
        "SnsEvent": {
            "orgId": "gs1",
            "tenantId": "3545cf5b-ada3-47d3-a514-91e9c48a6f71",
            "productId": "3545cf5b-ada3-47d3-a514-91e9c48a6f71",
            "domain": "gabriel",
            "eventType": "cancellation_failure",
            "schema": "1.0",
            "timestamp": ts,
            "sendTimestamp": ts,
            "eventId": uuids,
            "data": "PushNotificationEvent"
        },
        "PushNotificationEvent": {
            "clientId": clienteId,
            "eventId": "enum.evtPUSH-ITI-ContestacaoNova",
            "contextVariables": "PushContextVariables"
        },
        "PushContextVariables": [
            {
                "key": "chargebackid",
                "value": chargebackId
            }
        ]
    }


def handler(event, context):
    sns_url = 'http://%s:4566' % os.environ['LOCALSTACK_HOSTNAME']
    LOGGER.info("Url: %s.", sns_url)

    sns_message = sns_event("cc", "xxx")
    client = boto3.client('sns',
                          aws_access_key_id="test",
                          aws_secret_access_key="test",
                          region_name="us-east-1",
                          endpoint_url=sns_url
                          )
    arn = "arn:aws:sns:us-east-1:000000000000:test-sns"

    publish_message(client, sns_message, arn)
    LOGGER.info(event)

    # for record in event['Records']:
    #   LOGGER.info(record['dynamodb'])
    #   LOGGER.info(record['eventName'])
    #   LOGGER.info(record['dynamodb']['NewImage'])
    #   LOGGER.info(record['dynamodb']['OldImage'])
    # return event


def publish_message(client, message, arn):
    try:
        response = client.publish(
            TargetArn=arn,
            Message=json.dumps({'default': json.dumps(message)}),
            MessageStructure='json'
        )
        message_id = response['MessageId']
        LOGGER.info('ENVIANDO ...')
        LOGGER.info("Id da menssgaem %s.", message_id)
        LOGGER.info('ENVIADO!')
    except ClientError:
        LOGGER.exception("Couldn't publish message to topic %s.", client.arn)
        raise
    else:
        return message_id
