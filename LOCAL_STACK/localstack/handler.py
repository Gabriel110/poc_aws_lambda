import logging
import boto3
import json
import os

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

def handler(event, context):

  teste()

  LOGGER.info('CHAMANDO')
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
  client = boto3.client('sns',
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1"
  )
  arn = "arn:aws:sns:us-east-1:000000000000:test2-sns"
  response = client.publish(
      TargetArn=arn,
      Message=json.dumps(message),
      Subject='a short subject for your message',
      MessageStructure='json'
  )
  LOGGER.info(response)

def teste2():
  message = {"foo": "bar"}
  sqs_client = boto3.client('sqs',
    aws_access_key_id="iti",
    aws_secret_access_key="iti",
    region_name="us-east-1",
    endpoint_url="http://localhost:4566"
  )
  response = sqs_client.send_message(
    QueueUrl = "http://localhost:4566/000000000000/gabriel",
    MessageBody=json.dumps(message)
  )

  LOGGER.info(response)
