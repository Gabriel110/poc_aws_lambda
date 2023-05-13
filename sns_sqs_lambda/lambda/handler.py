import logging
from sns import Sns

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

def handler(event, context):
  for record in event['Records']:
    LOGGER.info(record['body'])
    Sns.send_message(record['body'])
  return event