import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

def handler(event, context):
  for record in event['Records']:
    LOGGER.info(record['dynamodb'])
    LOGGER.info(record['eventName'])
  return event
