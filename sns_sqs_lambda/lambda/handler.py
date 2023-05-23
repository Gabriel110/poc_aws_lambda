import logging
from sns import Sns
import json

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

def handler(event, context):
  for record in event['Records']:
    LOGGER.info(record['body'])
    response = json.loads('{"nome":"xxx"}')
    request = json.loads(record['body'])
    message = Sns.json_merge(request, response)
    LOGGER.info("MESSAGE {}".format(message))
    Sns.send_message(message)
  return event