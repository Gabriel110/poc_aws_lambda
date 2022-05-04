import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import logging
import os
import uuid
from datetime import datetime

from botocore.exceptions import ClientError

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

URL_LOCLA = 'http://%s:4566' % os.environ['LOCALSTACK_HOSTNAME']
LOGGER.info("Url: %s.", URL_LOCLA)
dynamodb_client = boto3.resource('dynamodb', endpoint_url=URL_LOCLA)
table = dynamodb_client.Table('my_table')

client = boto3.client('sns', endpoint_url=URL_LOCLA)

arn = "arn:aws:sns:us-east-1:000000000000:test-sns"
tenantId = "b507498202dc4051bbd4ffd363223707"
productId = "b507498202dc4051bbd4ffd363223707"


def hello(event, context):
    response = table.scan()
    data = response['Items']

    for i in data:
        dif_date = diff_days(i['attendance_period_end_data'])
        isZeroOrNineNIne = i['internal_process_status_code'] == 0 or i['internal_process_status_code'] == 99
        LOGGER.info("Diferença entre duas datas %s", dif_date)
        LOGGER.info("E 99 ou 0 %s", isZeroOrNineNIne)
        if dif_date == 2 and isZeroOrNineNIne:
            contextVariable = [{"chave": 'chargebackid', "valor": i['chargeback_id']}]
            send_push(i['client_id'], "xxx", contextVariable)
            LOGGER.info("Data %s, context %s", i['attendance_period_end_data'], contextVariable)

    response = {
        "statusCode": 200,
        "body": response
    }

    return response


def diff_days(date):
    today = datetime.now()
    d2 = datetime.strptime(date, "%Y-%m-%d")
    return abs((today - d2).days)


def send_push(idCliente, idEvent, contextVariable):
    snsData = SnsEventData(idCliente, idEvent, contextVariable)
    snsEvent = SnsEvent(tenantId, productId, snsData)
    publish_message(snsEvent)


def publish_message(message):
    try:
        LOGGER.info('Sending push notification SNS')
        LOGGER.info(json.dumps(message, default=class_to_json))
        response = client.publish(
            TargetArn=arn,
            Message=json.dumps(message, default=class_to_json)
        )
        messageId = response['MessageId']
        LOGGER.info("Id da menssgaem %s.", messageId)
        LOGGER.info('Push notification sended sucess')
    except ClientError:
        LOGGER.exception("Couldn't publish message to topic %s.", client.arn)
        raise
    else:
        return messageId


class SnsEvent:
    def __init__(self, tenantId, productId, snsData):
        self.orgId = "bs1"
        self.tenantId = tenantId
        self.productId = productId
        self.domain = "chargeback"
        self.eventType = "success"
        self.schema = "/chargeback/success/1.0"
        self.schemaVersion = "1.0"
        self.timestamp = datetime.now().timestamp()
        self.sendTimestamp = datetime.now().timestamp()
        self.eventId = uuid.uuid4().hex
        self.data = snsData


class SnsEventData:
    def __init__(self, idCliente, idEvent, contextVariable):
        self.idCliente = idCliente
        self.idEvent = idEvent
        self.contextVariable = contextVariable


def class_to_json(snsEvent):
    if isinstance(snsEvent, SnsEvent):
        return {
            'org_id': snsEvent.orgId,
            'tenant_id': snsEvent.tenantId,
            'product_id': snsEvent.productId,
            "domain": snsEvent.domain,
            'event_type': snsEvent.eventType,
            'schema': snsEvent.schema,
            'schema_version': snsEvent.schemaVersion,
            'timestamp': snsEvent.timestamp,
            'send_timestamp': snsEvent.sendTimestamp,
            'event_id': snsEvent.eventId,
            'data': {
                'id_cliente': snsEvent.data.idCliente,
                'id_event': snsEvent.data.idEvent,
                'variaveis_contexto': json.dumps(snsEvent.data.contextVariable)
            }
        }
    raise TypeError(f'Object not valid')