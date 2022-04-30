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
    array: []

    def __int__(self, clientId, eventId, array):
        self.clientId = clientId
        self.eventId = eventId
        self.array = array

    def toString(self):
        return {
            "clientId": self.clientId,
            "eventId": self.eventId,
        }

    def xx(self):
        return self.array




def handler():
    ps1 = PushContextVariables("xx", "yy")
    ps2 = PushContextVariables("xx2", "yy2")
    aa = [ps1, ps2]
    p = PushNotificationEvent(clientId="xx2", eventId="x2", array=aa)
    print(p.xx())


if __name__ == '__main__':
    handler()
