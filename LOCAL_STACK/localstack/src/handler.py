import logging
import boto3
import json
from botocore.exceptions import ClientError
import os
import uuid
import datetime

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


class PushContextVariables:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def toString(self):
        return {
            "key": self.key,
            "value": self.value
        }


class PushNotificationEvent:
    def __init__(self, clientId, eventId, pushContextVar):
        self.clientId = clientId
        self.eventId = eventId
        self.pushContextVar = pushContextVar

    def arrayToJson(self):
        ctxVar = []
        for i in self.pushContextVar:
            ctxVar.append({"key": i.key, "value": i.value})
        return ctxVar

    def toString(self):
        return {
            "client_id": self.clientId,
            "event_id": self.eventId,
            "context_variables": self.arrayToJson()
        }


class SnsEvent:
    def __init__(self, tenantId, productId, pushNotificationEvent):
        self.orgId = "gs1"
        self.tenantId = tenantId
        self.productId = productId
        self.eventType = "cancellation_failure"
        self.schema = "1.0"
        self.timestamp = datetime.datetime.now().timestamp()
        self.sendTimestamp = datetime.datetime.now().timestamp()
        self.eventId = uuid.uuid4().hex
        self.data = pushNotificationEvent

    def toString(self):
        return {
            "org_id": self.orgId,
            "tenant_id": self.tenantId,
            "product_id": self.productId,
            "event_type": self.eventType,
            "schema": self.schema,
            "timestamp": self.timestamp,
            "send_timestamp": self.sendTimestamp,
            "event_id": self.eventId,
            "data": self.data.toString()
        }


def class_to_json(sqs):
    if isinstance(sqs, SnsEvent):
        return {
            'org_id': sqs.orgId,
            'tenant_id': sqs.tenantId,
            'product_id': sqs.productId,
            'event_type': sqs.eventType,
            'schema': sqs.schema,
            'timestamp': sqs.timestamp,
            'send_timestamp': sqs.sendTimestamp,
            'event_id': sqs.eventId,
            'data': {
                'client_id': sqs.data.clientId,
                'event_id': sqs.data.eventId,
                'context_variables': sqs.data.toString()
            }
        }
    raise TypeError(f'Object not valid')


def handler(event, context):
    sns_url = 'http://%s:4566' % os.environ['LOCALSTACK_HOSTNAME']
    LOGGER.info("Url: %s.", sns_url)

    client = boto3.client('sns',
                          aws_access_key_id="test",
                          aws_secret_access_key="test",
                          region_name="us-east-1",
                          endpoint_url=sns_url
                          )
    arn = "arn:aws:sns:us-east-1:000000000000:test-sns"
    for record in event['Records']:

        eventInsert = record['eventName'] == 'INSERT'
        eventModify = record['eventName'] == 'MODIFY'
        internalNewProcess = record['dynamodb']['NewImage']['internal_process_status_code']['N']
        LOGGER.info('Event  %s', record['eventName'])
        LOGGER.info('Evento insert %s', eventInsert)
        LOGGER.info('Evento modify  %s', eventModify)
        LOGGER.info('Novo dados  %s', internalNewProcess)

        if eventInsert and internalNewProcess == '0':
            LOGGER.info('Push notification internal process status code 0')
            sns_message = generate_sns_message("xx0", "yy0", record['dynamodb']['NewImage']['client_id']['S'],
                                               "evtPUSH-ITI-ContestacaoNova",
                                               record['dynamodb']['NewImage']['chargeback_id']['S'])
            publish_message(client, sns_message, arn)
        elif eventModify:
            internalOldProcess = record['dynamodb']['OldImage']['internal_process_status_code']['N']
            internalProcessEqual = internalOldProcess == internalNewProcess
            internalOldDefense = record['dynamodb']['OldImage']['internal_actual_defense_document_status_code']['N']
            internalNewDefense = record['dynamodb']['NewImage']['internal_actual_defense_document_status_code']['N']
            internalDefenseEqual = internalNewDefense == internalOldDefense
            if not internalProcessEqual:
                if internalNewProcess == '10':
                    LOGGER.info('Push notification internal process status code 10')
                    sns_message = generate_sns_message("xx10", "yy10", record['dynamodb']['NewImage']['client_id']['S'],
                                                       "evtPUSH-ITI-10",
                                                       record['dynamodb']['NewImage']['chargeback_id']['S'])
                    publish_message(client, sns_message, arn)
                elif internalNewProcess == '20':
                    LOGGER.info('Push notification internal process status code 20')
                    sns_message = generate_sns_message("xx20", "yy20", record['dynamodb']['NewImage']['client_id']['S'],
                                                       "evtPUSH-ITI-20",
                                                       record['dynamodb']['NewImage']['chargeback_id']['S'])
                    publish_message(client, sns_message, arn)
                elif internalNewProcess == '30':
                    LOGGER.info('Push notification internal process status code 30')
                    sns_message = generate_sns_message("xx30", "yy30", record['dynamodb']['NewImage']['client_id']['S'],
                                                       "evtPUSH-ITI-Contestacao30",
                                                       record['dynamodb']['NewImage']['chargeback_id']['S'])
                    publish_message(client, sns_message, arn)
                else:
                    LOGGER.info("No situation found for triggering the push")
                if internalOldDefense != internalNewDefense and internalNewDefense == '13':
                    LOGGER.info('Push notification internal actual defense document status code 13')
                    sns_message = generate_sns_message("xx13", "yy13", record['dynamodb']['NewImage']['client_id']['S'],
                                                       "evtPUSH-ITI-Contestacao13",
                                                       record['dynamodb']['NewImage']['chargeback_id']['S'])
                    publish_message(client, sns_message, arn)
        else:
            LOGGER.info("No situation found the push")
    LOGGER.info(event)


def generate_sns_message(tenantId, productId, clientId, eventId, value):
    pushContextVar = PushContextVariables('chargebackid', value)
    pushNotificationEvent = PushNotificationEvent(clientId, eventId, [pushContextVar])
    snsMessage = SnsEvent(tenantId, productId, pushNotificationEvent)
    return snsMessage


def publish_message(client, message, arn):
    try:
        response = client.publish(
            TargetArn=arn,
            Message=json.dumps({'default': json.dumps(message, default=class_to_json)}),
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
