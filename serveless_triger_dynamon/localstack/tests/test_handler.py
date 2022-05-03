import unittest
from unittest import mock

import localstack.src.handler
from localstack.src.handler import handler, send_push

event1 = {
    "Records": [
        {
            "eventVersion": "1.1",
            "dynamodb": {
                "ApproximateCreationDateTime": 1651578891,
                "SizeBytes": 188,
                "Keys": {
                    "id": {
                        "S": "4"
                    }
                },
                "NewImage": {
                    "id": {
                        "S": "4"
                    },
                    "internal_process_status_code": {
                        "N": "0"
                    },
                    "client_id": {
                        "S": "sss123"
                    },
                    "chargeback_id": {
                        "S": "54566567"
                    },
                    "internal_actual_defense_document_status_code": {
                        "N": "0"
                    }
                },
                "StreamViewType": "NEW_AND_OLD_IMAGES",
                "OldImage": {
                    "internal_process_status_code": {
                        "N": "0"
                    },
                    "id": {
                        "S": "4"
                    },
                    "internal_actual_defense_document_status_code": {
                        "N": "0"
                    },
                    "client_id": {
                        "S": "sss123"
                    },
                    "chargeback_id": {
                        "S": "54566567"
                    }
                },
                "SequenceNumber": "9"
            },
            "awsRegion": "us-east-1",
            "eventSource": "aws:dynamodb",
            "eventName": "MODIFY",
            "eventSourceARN": "arn:aws:dynamodb:us-east-1:000000000000:table/my_table"
        }
    ]
}


class MyTestCase(unittest.TestCase):
    def test_handler(self):
        handler(event1, None)


if __name__ == '__main__':
    unittest.main()
