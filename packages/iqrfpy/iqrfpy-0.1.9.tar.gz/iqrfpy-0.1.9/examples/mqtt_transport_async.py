from datetime import datetime
from threading import Thread
import time

from iqrfpy.messages.requests.ledr.pulse import PulseRequest
from iqrfpy.messages.responses.iresponse import IResponse
from iqrfpy.transports.mqtt_transport import MqttTransportParams, MqttTransport


def handler(response: IResponse) -> None:
    print('received response', datetime.now())
    print(response.get_mtype())
    print(response.get_msgid())


params = MqttTransportParams(
        host='localhost',
        port=1883,
        client_id='python-lib-test',
        request_topic='Iqrf/DpaRequest',
        response_topic='Iqrf/DpaResponse',
        qos=1,
        keepalive=25
    )
transport = MqttTransport(params=params, callback=handler)


def subscribe():
    transport.initialize()


def publish():
    while True:
        time.sleep(5)
        print('sending request', datetime.now())
        transport.send(PulseRequest(nadr=0))


sub = Thread(target=subscribe)
pub = Thread(target=publish)

sub.start()
pub.start()
