import logging
from sns import Sns
from myhttp import Feign

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

def handler(event, context):
  for record in event['Records']:
    LOGGER.info(record['body'])
    response = Feign.getName()
    message = Sns.json_merge(record['body'], response)
    Sns.send_message(message)
  return event