import time
from datetime import datetime
from iqrfpy.exceptions import MessageNotReceivedError
from iqrfpy.messages.requests.ledr.pulse import PulseRequest
from iqrfpy.messages.requests.os.read import ReadRequest
from iqrfpy.messages.responses.iresponse import IResponse
from iqrfpy.transports.mqtt_transport import MqttTransportParams, MqttTransport


def handler(response: IResponse) -> None:
    print(f'received response at {datetime.now()}')
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
transport = MqttTransport(params=params, auto_init=True)

time.sleep(10)

print(f'sending request at {datetime.now()}')
rsp = transport.send_and_receive(PulseRequest(nadr=0, msgid='pulseTest'), timeout=2)
handler(rsp)

print(f'sending request at {datetime.now()}')
rsp = transport.send_and_receive(ReadRequest(nadr=0, msgid='osTest1'), timeout=1)
handler(rsp)

print(f'sending request at {datetime.now()}')
transport.send(ReadRequest(nadr=0, msgid='osTest2'))
rsp = transport.receive(timeout=1)
handler(rsp)

print(f'sending request at {datetime.now()}')
try:
    rsp = transport.send_and_receive(ReadRequest(nadr=2, msgid='osTest3'), timeout=1)
    handler(rsp)
except MessageNotReceivedError as e:
    print('Message not received: ', str(e))
