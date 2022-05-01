from classes import SnsEvent
import json
from botocore.exceptions import ClientError
import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


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
