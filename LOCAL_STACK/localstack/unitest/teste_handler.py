import unittest
from localstack.src.handler import PushContextVariables, PushNotificationEvent, SnsEvent, handler
from localstack.src.handler import generate_sns_message
from unittest import mock, TestCase

pushContextVar = PushContextVariables('chargebackid', 'xxx')

pushNotificationEvent = PushNotificationEvent('019', 't1esww', [pushContextVar])
snsEvet = SnsEvent("gavsg", "ajjsjds", pushNotificationEvent)

event1 = {
  'Records': [
    {
      'eventVersion': '1.1',
      'dynamodb': {
        'ApproximateCreationDateTime': 1651512028,
        'SizeBytes': 190,
        'Keys': {
          'id': {
            'S': '1'
          }
        },
        'NewImage': {
          'id': {
            'S': '1'
          },
          'internal_process_status_code': {
            'N': '0'
          },
          'client_id': {
            'S': 'sss123'
          },
          'chargeback_id': {
            'S': '54566567'
          },
          'internal_actual_defense_document_status_code': {
            'N': '0'
          }
        },
        'StreamViewType': 'NEW_AND_OLD_IMAGES',
        'SequenceNumber': '1'
      },
      'awsRegion': 'us-east-1',
      'eventSource': 'aws:dynamodb',
      'eventName': 'INSERT',
      'eventSourceARN': 'arn:aws:dynamodb:us-east-1:000000000000:table/my_table'
    }
  ]
}

class MyTestCase(TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

    def test_generate_sns_message(self):
        self.assertEqual(snsEvet.toString().get('org_id'),
                         generate_sns_message("gavsg", "ajjsjds", '019', 't1esww', "xxx").toString().get('org_id'))
        self.assertEqual(snsEvet.toString().get('tenant_id'),
                         generate_sns_message("gavsg", "ajjsjds", '019', 't1esww', "xxx").toString().get('tenant_id'))
        self.assertEqual(snsEvet.toString().get('org_id'),
                         generate_sns_message("gavsg", "ajjsjds", '019', 't1esww', "xxx").toString().get('org_id'))
        self.assertEqual(snsEvet.toString().get('product_id'),
                         generate_sns_message("gavsg", "ajjsjds", '019', 't1esww', "xxx").toString().get('product_id'))
        self.assertEqual(snsEvet.toString().get('event_type'),
                         generate_sns_message("gavsg", "ajjsjds", '019', 't1esww', "xxx").toString().get('event_type'))
        self.assertEqual(snsEvet.toString().get('schema'),
                         generate_sns_message("gavsg", "ajjsjds", '019', 't1esww', "xxx").toString().get('schema'))
        self.assertEqual(snsEvet.toString().get('data'),
                         generate_sns_message("gavsg", "ajjsjds", '019', 't1esww', "xxx").toString().get('data'))


if __name__ == '__main__':
    unittest.main()
