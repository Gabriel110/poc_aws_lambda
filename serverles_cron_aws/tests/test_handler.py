import unittest
from unittest.mock import Mock, MagicMock
from src import handler
from moto import mock_dynamodb2, mock_sns
import boto3
import os



intens = [{
  "id": {
    "S": "1"
  },
  "internal_process_status_code": {
    "N": "0"
  },
  "client_id": {
    "S": "001"
  },
  "chargeback_id": {
    "S": "d88c1fe5-f314-4dae-ac3c-9fde8604caa5"
  },
  "internal_actual_defense_document_status_code": {
    "N": "0"
  },
  "attendance_period_end_data": {
    "S": "2022-05-04"
  }
}]


class MyTestCase(unittest.TestCase):

    def setUp(self):
        handler.client = Mock()
        handler.dynamodb_client = Mock()
        handler.table = Mock()
        handler.data = intens
        handler.table.scan = MagicMock()[intens]
        boto3.setup_default_session()
        client = boto3.client('sns', "us-east-1")
        dynamodb_client = boto3.resource('dynamodb')


    @mock_dynamodb2
    @mock_sns
    def test_handler(self):
        handler.hello(None, None)
        self.assertIsNotNone(handler.table)
        self.assertIsNotNone(handler.client)
        self.assertIsNotNone(handler.dynamodb_client)

if __name__ == '__main__':
    unittest.main()
