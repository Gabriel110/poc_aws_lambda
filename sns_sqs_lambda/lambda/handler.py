import logging
from sns import Sns
from myhttp import Feign

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

def handler(event, context):
  for record in event['Records']:
    LOGGER.info(record['body'])
    response = Feign.getName()
    message = Sns.enrich_message(record['body'], response)
    Sns.send_message(message)
  return event