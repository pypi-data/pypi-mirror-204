import time
from datetime import datetime
from iqrfpy.messages.requests.ledr.pulse import PulseRequest
from iqrfpy.messages.requests.os.read import ReadRequest
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
transport = MqttTransport(params=params, synchronous=True, auto_init=True)

time.sleep(10)

print('sending request', datetime.now())
rsp = transport.send_and_receive(PulseRequest(nadr=0, msgid='pulseTest'), timeout=2)
handler(rsp)

print('sending request', datetime.now())
rsp = transport.send_and_receive(ReadRequest(nadr=0, msgid='osTest1'), timeout=1)
handler(rsp)

print('sending request', datetime.now())
rsp = transport.send_and_receive(ReadRequest(nadr=2, msgid='osTest2'), timeout=1)
handler(rsp)


