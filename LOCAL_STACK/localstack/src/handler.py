import json
import logging
import boto3
import os
from classes.classes import PushContextVariables, PushNotificationEvent, SnsEvent
from localstack.src.classes.util import class_to_json, publish_message

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def handler(event, context):
    sns_url = 'http://%s:4566' % os.environ['LOCALSTACK_HOSTNAME']
    LOGGER.info("Url: %s.", sns_url)
    pushContextVar = PushContextVariables('chargebackid', 'xxx')
    pushContextVar1 = PushContextVariables('chargebackid', 'xxx1')
    pushContextVar2 = PushContextVariables('chargebackid', 'xxx2')
    pushNotificationEvent = PushNotificationEvent('019', 't1esww', [pushContextVar, pushContextVar1, pushContextVar2])
    snsEvet = SnsEvent("gavsg", "ajjsjds", pushNotificationEvent)

    sns_message = snsEvet
    client = boto3.client('sns',
                          aws_access_key_id="test",
                          aws_secret_access_key="test",
                          region_name="us-east-1",
                          endpoint_url=sns_url
                          )
    arn = "arn:aws:sns:us-east-1:000000000000:test-sns"

    publish_message(client, sns_message, arn)
    LOGGER.info(sns_message)
    print(json.dumps(sns_message, default=class_to_json))

    # for record in event['Records']:
    #   LOGGER.info(record['dynamodb'])
    #   LOGGER.info(record['eventName'])
    #   LOGGER.info(record['dynamodb']['NewImage'])
    #   LOGGER.info(record['dynamodb']['OldImage'])
    # return event


if __name__ == "__main__":
    handler('', '')

