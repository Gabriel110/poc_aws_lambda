import logging
import boto3
import json
import os
import uuid
import datetime

from botocore.exceptions import ClientError

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

# sns_url = 'http://%s:4566' % os.environ['LOCALSTACK_HOSTNAME']
# LOGGER.info("Url: %s.", sns_url)
#
# client = boto3.client('sns',
#                       aws_access_key_id="test",
#                       aws_secret_access_key="test",
#                       region_name="us-east-1",
#                       endpoint_url=sns_url
#                       )
client = boto3.client('sns')
arn = "arn:aws:sns:us-east-1:000000000000:test-sns"
tenantId = "b507498202dc4051bbd4ffd363223707"
productId = "b507498202dc4051bbd4ffd363223707"


def handler(event, context):
    for record in event['Records']:
        LOGGER.info(event)
        eventInsert = record['eventName'] == 'INSERT'
        eventModify = record['eventName'] == 'MODIFY'
        eventRemove = record['eventName'] == 'REMOVE'

        if not eventRemove:
            idCliente = record['dynamodb']['NewImage']['client_id']['S']
            chargebackId = record['dynamodb']['NewImage']['chargeback_id']['S']
            internalNewProcess = record['dynamodb']['NewImage']['internal_process_status_code']['N']

            if eventInsert and internalNewProcess == '0':
                LOGGER.info('Starting process push notification event: evtPUSH-ITI-ContestacaoNova')
                send_push(idCliente, "evtPUSH-ITI-ContestacaoNova", chargebackId)
                LOGGER.info('Process push notification successfully finished event: evtPUSH-ITI-ContestacaoNova')
            elif eventModify:
                internalOldProcess = record['dynamodb']['OldImage']['internal_process_status_code']['N']
                internalOldDefense = record['dynamodb']['OldImage']['internal_actual_defense_document_status_code']['N']
                internalNewDefense = record['dynamodb']['NewImage']['internal_actual_defense_document_status_code']['N']
                internalProcessEqual = internalOldProcess == internalNewProcess
                internalDefenseEqual = internalNewDefense == internalOldDefense

                if not internalProcessEqual:
                    if internalNewProcess == '10':
                        LOGGER.info('Starting process push notification event: evtPUSH-ITI-ContestacaoComprovada')
                        send_push(idCliente, "evtPUSH-ITI-ContestacaoComprovada", chargebackId)
                        LOGGER.info('Process push notification successfully finished event: evtPUSH-ITI-ContestacaoComprovada')
                    elif internalNewProcess == '20':
                        LOGGER.info('Starting process push notification event: evtPUSH-ITI-ContestacaoNaoComprovada')
                        send_push(idCliente, "evtPUSH-ITI-ContestacaoNaoComprovada", chargebackId)
                        LOGGER.info('Process push notification successfully finished event: evtPUSH-ITI-ContestacaoNaoComprovada')
                    elif internalNewProcess == '30':
                        LOGGER.info('Starting process push notification event: evtPUSH-ITI-ContestacaoEncerrada')
                        send_push(idCliente, "evtPUSH-ITI-ContestacaoEncerrada", chargebackId)
                        LOGGER.info(
                            'Process push notification successfully finished event: evtPUSH-ITI-ContestacaoEncerrada')
                    else:
                        LOGGER.info("No situation found for triggering the push: Process status")
                else:
                    LOGGER.info("No situation found for triggering the push: Process status")

                if not internalDefenseEqual and internalNewDefense == '13':
                    LOGGER.info('Starting process push notification event: evtPUSH-ITI-ContestacaoDocumentoRecusado')
                    send_push(idCliente, "evtPUSH-ITI-ContestacaoDocumentoRecusado", chargebackId)
                    LOGGER.info('Process push notification successfully finished event: evtPUSH-ITI-ContestacaoDocumentoRecusado')
                else:
                    LOGGER.info("No situation found for triggering the push: Defense document status")

        else:
            LOGGER.info("No situation found the push")


def class_to_json(sqs):
    if isinstance(sqs, SnsEvent):
        return {
            'org_id': sqs.orgId,
            'tenant_id': sqs.tenantId,
            'product_id': sqs.productId,
            "domain": sqs.domain,
            'event_type': sqs.eventType,
            'schema': sqs.schema,
            'schema_version': sqs.schemaVersion,
            'timestamp': sqs.timestamp,
            'send_timestamp': sqs.sendTimestamp,
            'event_id': sqs.eventId,
            'data': {
                'id_cliente': sqs.idCliente,
                'id_event': sqs.idEvent,
                'variaveis_contexto': sqs.contextVariable.toString()
            }
        }
    raise TypeError(f'Object not valid')


class PushContextVariables:
    def __init__(self, chave, valor):
        self.chave = chave
        self.valor = valor

    def toString(self):
        return {
            "chave": self.chave,
            "valor": self.valor
        }


class SnsEvent:
    def __init__(self, tenantId, productId, idCliente, idEvent, contextVariable):
        self.orgId = "gsb"
        self.tenantId = tenantId
        self.productId = productId
        self.domain = "gabriel"
        self.eventType = "success"
        self.schema = "/gabriel/success/1.0"
        self.schemaVersion = "1.0"
        self.timestamp = datetime.datetime.now()
        self.sendTimestamp = datetime.datetime.now()
        self.eventId = uuid.uuid4().hex
        self.idCliente = idCliente
        self.idEvent = idEvent
        self.contextVariable = contextVariable


def send_push(idCliente, idEvent, value):
    sns_message = generate_sns_message(idCliente, idEvent, value)
    publish_message(sns_message)


def generate_sns_message(idCliente, idEvent, value):
    contextVariable = PushContextVariables('chargebackid', value)
    snsMessage = SnsEvent(tenantId, productId, idCliente, idEvent, contextVariable)
    return snsMessage


def publish_message(message):
    try:
        LOGGER.info('Sending push notification SNS')
        LOGGER.info(json.dumps(message, default=class_to_json))
        response = client.publish(
            TargetArn=arn,
            Message=json.dumps(message, default=class_to_json)
        )
        message_id = response['MessageId']
        LOGGER.info("Id da menssgaem %s.", message_id)
        LOGGER.info('Push notification sended sucess')
    except ClientError:
        LOGGER.exception("Couldn't publish message to topic %s.", client.arn)
        raise
    else:
        return message_id