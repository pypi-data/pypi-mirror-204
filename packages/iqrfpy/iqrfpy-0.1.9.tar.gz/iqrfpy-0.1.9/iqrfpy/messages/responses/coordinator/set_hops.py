from __future__ import annotations
from typeguard import typechecked
from typing import Optional
from iqrfpy.messages.responses.iresponse import IResponse, IResponseGetterMixin
from iqrfpy.enums.commands import CoordinatorResponseCommands
from iqrfpy.enums.message_types import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import DpaResponsePacketLengthError
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as DpaConstants
from iqrfpy.utils.dpa import ResponseCodes, ResponsePacketMembers

__all__ = ['SetHopsResponse']


@typechecked
class SetHopsResponse(IResponseGetterMixin):
    __slots__ = '_request_hops', '_response_hops'

    def __init__(self, hwpid: int = DpaConstants.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 msgid: Optional[str] = None, result: Optional[dict] = None):
        super().__init__(
            nadr=DpaConstants.COORDINATOR_NADR,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorResponseCommands.SET_HOPS,
            m_type=CoordinatorMessages.SET_HOPS,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            result=result
        )
        if rcode == ResponseCodes.OK:
            self._request_hops = result['requestHops']
            self._response_hops = result['responseHops']

    def get_request_hops(self) -> int:
        return self._request_hops

    def get_response_hops(self) -> int:
        return self._response_hops

    @staticmethod
    def from_dpa(dpa: bytes) -> SetHopsResponse:
        IResponse.validate_dpa_response(dpa)
        hwpid = Common.hwpid_from_dpa(dpa[ResponsePacketMembers.HWPID_HI], dpa[ResponsePacketMembers.HWPID_LO])
        rcode = dpa[ResponsePacketMembers.RCODE]
        result = None
        if rcode == ResponseCodes.OK:
            if len(dpa) != 10:
                raise DpaResponsePacketLengthError('Invalid DPA response packet length.')
            result = {'requestHops': dpa[8], 'responseHops': dpa[9]}
        return SetHopsResponse(hwpid=hwpid, rcode=rcode, dpa_value=dpa[ResponsePacketMembers.DPA_VALUE], result=result)

    @staticmethod
    def from_json(json: dict) -> SetHopsResponse:
        msgid = Common.msgid_from_json(json)
        hwpid = Common.hwpid_from_json(json)
        dpa_value = Common.dpa_value_from_json(json)
        rcode = Common.rcode_from_json(json)
        result = Common.result_from_json(json) if rcode == ResponseCodes.OK else None
        return SetHopsResponse(msgid=msgid, hwpid=hwpid, dpa_value=dpa_value, rcode=rcode, result=result)
