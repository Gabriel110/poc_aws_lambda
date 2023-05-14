import json
import boto3
import os

sns_url = 'http://%s:4566' % os.environ['LOCALSTACK_HOSTNAME']
sns = boto3.client('sns', aws_access_key_id="test", aws_secret_access_key="test", region_name="us-east-1", endpoint_url=sns_url)
topic_arn = 'arn:aws:sns:us-east-1:000000000000:sns-lambda-dois'

class Sns:

  def send_message(message):
    try:
      response = sns.publish(
        TopicArn=topic_arn,
        Message= message
      )
          
      print('Message published to SNS topic')
      return {
        'statusCode': 200,
        'body': json.dumps(response)
      }
    except Exception as e:
      print('Failed to publish message to SNS topic')
      return {'status': 'error', 'message': str(e)}
  
  def enrich_message(message, enrichment):
    message['nome'] = enrichment
    return message
    
  def json_merge(message, enrichment):
    message.update(enrichment)
    return message