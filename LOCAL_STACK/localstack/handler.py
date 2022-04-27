import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

def handler(event, context):
  for record in event['Records']:
    LOGGER.info(record['dynamodb'])
    LOGGER.info(record['eventName'])
    LOGGER.info(record['dynamodb']['NewImage'])
    LOGGER.info(record['dynamodb']['OldImage'])
    LOGGER.info('CHAMANDO')

    if(record['dynamodb']['NewImage']['Nome'] != record['dynamodb']['OldImage']['Nome'] ):
      LOGGER.info("DIFERENTE")
    else:
      LOGGER.info("IGUAL")
  return event
