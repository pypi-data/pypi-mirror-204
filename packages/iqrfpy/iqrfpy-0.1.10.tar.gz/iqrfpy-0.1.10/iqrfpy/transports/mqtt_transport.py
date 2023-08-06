from dataclasses import dataclass
import json
import random
import string
import threading

from typing import Callable, Optional
from typeguard import typechecked
from paho.mqtt.client import Client
from iqrfpy.exceptions import TransportNotConnectedError, MessageNotReceivedError
from iqrfpy.messages.requests.irequest import IRequest
from iqrfpy.messages.responses.confirmation import Confirmation
from iqrfpy.messages.responses.iresponse import IResponse
from iqrfpy.messages.response_factory import ResponseFactory
from iqrfpy.transports.itransport import ITransport

__all__ = (
    'MqttTransportParams'
    'MqttTransport'
)


@dataclass
@typechecked
class MqttTransportParams:
    host: str = 'localhost'
    port: int = 1883
    client_id: str = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(16))
    user: str = None
    password: str = None
    request_topic: str = None
    response_topic: str = None
    qos: int = 1
    keepalive: int = 60

    def __post_init__(self):
        if not (1024 <= self.port <= 65535):
            raise MqttParamsError('Port value should be between 1024 and 65535.')
        if (self.user is not None and self.password is None) or (self.user is None and self.password is not None):
            raise MqttParamsError('Both user and password parameters need to be specified, or neither of them.')
        if not (0 <= self.qos <= 2):
            raise MqttParamsError('QoS value should be between 0 and 2.')


class MqttTransport(ITransport):

    __slots__ = '_client', '_params', '_callback', '_timeout', '_cv'

    def __init__(self, params: MqttTransportParams, callback: Optional[Callable] = None,
                 auto_init: bool = False, timeout: Optional[int] = 5):
        self._client: Optional[Client] = None
        self._params: MqttTransportParams = params
        self._callback: Optional[Callable] = callback
        self._timeout: int = timeout
        self._msg_id: Optional[str] = None
        self._cv: threading.Condition = threading.Condition()
        self._response: Optional[IResponse] = None
        if auto_init:
            self.initialize()

    def initialize(self) -> None:
        self._client = Client(self._params.client_id)
        self._client.on_connect = self._connect_callback
        self._client.on_message = self._message_callback
        if self._params.user is not None and self._params.password is not None:
            self._client.username_pw_set(self._params.user, self._params.password)
        self._client.connect(self._params.host, self._params.port)
        self._client.loop_start()

    def _connect_callback(self, client, userdata, flags, rc):
        # pylint: disable=W0613
        if rc == 0:
            self._client.subscribe(self._params.response_topic, self._params.qos)

    def _message_callback(self, client, userdata, message):
        # pylint: disable=W0613
        payload = json.loads(message.payload.decode('utf-8'))
        response = ResponseFactory.get_response_from_json(payload)
        if self._callback is not None:
            self._callback(response)
        if response.get_msgid() == self._msg_id:
            self._response = response
            with self._cv:
                self._cv.notify()

    def send(self, request: IRequest) -> None:
        self._response = None
        self._msg_id = None
        if not self._client.is_connected():
            raise TransportNotConnectedError(f'MQTT client {self._params.client_id} not connected to broker.')
        self._client.publish(
            topic=self._params.request_topic,
            payload=json.dumps(request.to_json()),
            qos=self._params.qos
        )
        self._msg_id = request.get_msg_id()

    def send_and_receive(self, request: IRequest, timeout: Optional[int] = None) -> IResponse:
        self.send(request)
        return self.receive(timeout)

    def receive(self, timeout: Optional[int] = None) -> IResponse:
        timeout_to_use = timeout if timeout is not None else self._timeout
        with self._cv:
            self._cv.wait(timeout=timeout_to_use)
        if self._response is None:
            raise MessageNotReceivedError(f'Response message to request with ID {self._msg_id} not received within the'
                                          f' specified time of {timeout_to_use} seconds.')
        return self._response

    def confirmation(self) -> Confirmation:
        raise NotImplementedError('Method not implemented.')

    def set_receive_callback(self, callback: Callable[[IResponse], None]) -> None:
        self._callback = callback


class MqttParamsError(Exception):
    pass
