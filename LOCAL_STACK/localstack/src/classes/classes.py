import uuid
import datetime


class PushContextVariables:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def toString(self):
        return {
            "key": self.key,
            "value": self.value
        }


class PushNotificationEvent:
    def __init__(self, clientId, eventId, pushContextVar):
        self.clientId = clientId
        self.eventId = eventId
        self.pushContextVar = pushContextVar

    def arrayToJson(self):
        ctxVar = []
        for i in self.pushContextVar:
            ctxVar.append({"key": i.key, "value": i.value})
        return ctxVar

    def toString(self):
        return {
            "client_id": self.clientId,
            "event_id": self.eventId,
            "context_variables": self.arrayToJson()
        }


class SnsEvent:
    def __init__(self, tenantId, productId, pushNotificationEvent):
        self.orgId = "gs1"
        self.tenantId = tenantId
        self.productId = productId
        self.eventType = "cancellation_failure"
        self.schema = "1.0"
        self.timestamp = datetime.datetime.now().timestamp()
        self.sendTimestamp = datetime.datetime.now().timestamp()
        self.eventId = uuid.uuid4().hex
        self.data = pushNotificationEvent

    def toString(self):
        return {
            "org_id": self.orgId,
            "tenant_id": self.tenantId,
            "product_id": self.productId,
            "event_type": self.eventType,
            "schema": self.schema,
            "timestamp": self.timestamp,
            "send_timestamp": self.sendTimestamp,
            "event_id": self.eventId,
            "data": self.data.toString()
        }
