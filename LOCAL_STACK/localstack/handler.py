import logging
import boto3
import json
import os

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

def handler(event, context):

  teste()

  # for record in event['Records']:
  #   LOGGER.info(record['dynamodb'])
  #   LOGGER.info(record['eventName'])
  #   LOGGER.info(record['dynamodb']['NewImage'])
  #   LOGGER.info(record['dynamodb']['OldImage'])
  #   LOGGER.info('CHAMANDO')

  #   if(record['dynamodb']['NewImage']['Nome'] != record['dynamodb']['OldImage']['Nome'] ):
  #     LOGGER.info("DIFERENTE")
  #   else:
  #     LOGGER.info("IGUAL")
  # return event

def teste():
  message = {"foo": "bar"}
  sns_url = 'http://%s:4566' % os.environ['LOCALSTACK_HOSTNAME']
  client = boto3.client('sns',
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1",
    endpoint_url=sns_url
  )
  arn = "arn:aws:sns:us-east-1:000000000000:test-sns"
  response = client.publish(
      TargetArn=arn,
      Message=json.dumps(message),
      Subject='a short subject for your message',
      MessageStructure='json'
  )
  LOGGER.info('ENVIANDO ...')
  LOGGER.info(response)
  LOGGER.info('ENVIADO!')