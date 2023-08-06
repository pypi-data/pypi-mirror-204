from __future__ import annotations
from typeguard import typechecked
from uuid import uuid4
from typing import Union
from iqrfpy.enums.commands import CoordinatorRequestCommands
from iqrfpy.enums.message_types import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as DpaConstants
from iqrfpy.messages.requests.irequest import IRequest

__all__ = ['SetHopsRequest']

REQUEST_HOPS_DRM = 0
REQUEST_HOPS_DOM = 0xFF
RESPONSE_HOPS_DOM = 0xFF


@typechecked
class SetHopsRequest(IRequest):
    __slots__ = '_request_hops', '_response_hops'

    def __init__(self, request_hops: int, response_hops: int, hwpid: int = DpaConstants.HWPID_MAX,
                 msgid: str = str(uuid4())):
        super().__init__(
            nadr=DpaConstants.COORDINATOR_NADR,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorRequestCommands.SET_HOPS,
            m_type=CoordinatorMessages.SET_HOPS,
            hwpid=hwpid,
            msgid=msgid
        )
        self._request_hops = request_hops
        self._response_hops = response_hops
        self._validate()

    def _validate(self) -> None:
        if (self._request_hops < REQUEST_HOPS_DRM or self._request_hops > DpaConstants.NODE_NADR_MAX) \
                and self._request_hops != REQUEST_HOPS_DOM:
            raise RequestParameterInvalidValueError('Request hops value should be between 0 and 239, or 255.')
        if (self._response_hops < DpaConstants.NODE_NADR_MIN or self._response_hops > DpaConstants.NODE_NADR_MAX) \
                and self._response_hops != RESPONSE_HOPS_DOM:
            raise RequestParameterInvalidValueError('Response hops value should be between 1 and 239, or 255.')

    def set_request_hops(self, request_hops: int) -> None:
        self._request_hops = request_hops

    def set_response_hops(self, response_hops: int) -> None:
        self._response_hops = response_hops

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        self._validate()
        self._pdata = [self._request_hops, self._response_hops]
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._validate()
        self._params = {'requestHops': self._request_hops, 'responseHops': self._response_hops}
        return super().to_json()
