import dataclasses
import json


@dataclasses.dataclass
class PushContextVariables:
    key: str
    value: str

    def __int__(self, key, value):
        self.key = key,
        self.value = value


@dataclasses.dataclass
class PushNotificationEvent:
    clientId: str
    eventId: str
    key: str
    value: str

    def __int__(self, clientId, eventId, key, value):
        self.clientId = clientId
        self.eventId = eventId
        self.key = key
        self.value = value

    def toJson(self):
        return {
            "key": "chargebackid",
            "value": self.value
        }


@dataclasses.dataclass
class SqsEvent:
    orgId: str
    tenantId: str
    productId: str
    domain: str
    eventType: str
    schema: str
    timestamp: str
    sendTimestamp: str
    eventId: str
    clientId: str
    notificationId: str
    key: str
    value: str

    def __int__(self, orgId, tenantId, productId, domain, eventType, schema, timestamp, sendTimestamp, eventId,
                clientId, notificationId, key, value):
        self.orgId = orgId
        self.tenantId = tenantId
        self.productId = productId
        self.domain = domain
        self.eventType = eventType
        self.schema = schema
        self.timestamp = timestamp
        self.sendTimestamp = sendTimestamp
        self.eventId = eventId
        self.notification = PushNotificationEvent(
            self.clientId,
            self.notificationId,
            self.key,
            self.value
        )

    pass

    def toString(self):
        if isinstance(self, SqsEvent):
            return {
                "org_id": self.orgId,
                "tenant_id": self.tenantId,
                "product_id": self.productId,
                "domain": self.domain,
                "event_type": self.eventType,
                "schema": self.schema,
                "timestamp": self.timestamp,
                "send_timestamp": self.sendTimestamp,
                "event_id": self.eventId,
                "data": {
                    "client_id": self.clientId,
                    "notification_id": self.notificationId,
                    "push_context_variables": [
                        {
                            "key": self.key,
                            "value": self.value
                        }
                    ]
                }

            }
        raise TypeError(f'Object {self} is not type SqsEvent')


def handler():
    ps1 = PushContextVariables("ps1", "ps1")
    sqs = SqsEvent(
        "gs1",
        "3545cf5b-ada3-47d3-a514-91e9c48a6f71",
        "3545cf5b-ada3-47d3-a514-91e9c48a6f71",
        "gabriel",
        "cancellation_failure",
        "1.0",
        "656565656.9005",
        "656565656.9005",
        "3545cf5b-ada3-47d3-a514-91e9c48a6f71",
        "3545cf5b-ada3-47d3-a514-91e9c48agabriel",
        "notificationId",
        "zz",
        "!"
    )
    tetes = sqs.toString()
    print(tetes)  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    handler()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
