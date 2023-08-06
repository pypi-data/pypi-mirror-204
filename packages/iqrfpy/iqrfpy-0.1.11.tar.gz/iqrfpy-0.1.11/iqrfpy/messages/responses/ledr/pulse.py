from __future__ import annotations
from typeguard import typechecked
from typing import Optional
from iqrfpy.messages.responses.iresponse import IResponse, IResponseGetterMixin
from iqrfpy.enums.commands import LEDResponseCommands
from iqrfpy.enums.message_types import LEDRMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import DpaResponsePacketLengthError
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as DpaConstants
from iqrfpy.utils.dpa import ResponsePacketMembers


@typechecked
class PulseResponse(IResponseGetterMixin):

    def __init__(self, nadr: int, hwpid: int = DpaConstants.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 msgid: Optional[str] = None, result: Optional[dict] = None):
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.LEDR,
            pcmd=LEDResponseCommands.PULSE,
            m_type=LEDRMessages.PULSE,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            result=result
        )

    @staticmethod
    def from_dpa(dpa: bytes) -> PulseResponse:
        IResponse.validate_dpa_response(dpa)
        nadr = dpa[ResponsePacketMembers.NADR]
        hwpid = Common.hwpid_from_dpa(dpa[ResponsePacketMembers.HWPID_HI], dpa[ResponsePacketMembers.HWPID_LO])
        rcode = dpa[ResponsePacketMembers.RCODE]
        if len(dpa) != 8:
            raise DpaResponsePacketLengthError('Invalid DPA response packet length.')
        return PulseResponse(nadr=nadr, hwpid=hwpid, rcode=rcode, dpa_value=dpa[ResponsePacketMembers.DPA_VALUE],
                             result=None)

    @staticmethod
    def from_json(json: dict) -> PulseResponse:
        msgid = Common.msgid_from_json(json)
        nadr = Common.nadr_from_json(json)
        hwpid = Common.hwpid_from_json(json)
        dpa_value = Common.dpa_value_from_json(json)
        rcode = Common.rcode_from_json(json)
        return PulseResponse(nadr=nadr, msgid=msgid, hwpid=hwpid, dpa_value=dpa_value, rcode=rcode, result=None)
