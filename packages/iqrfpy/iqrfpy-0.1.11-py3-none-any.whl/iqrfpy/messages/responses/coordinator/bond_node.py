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

__all__ = ['BondNodeResponse']


@typechecked
class BondNodeResponse(IResponseGetterMixin):
    __slots__ = '_bond_addr', '_dev_nr'

    def __init__(self, hwpid: int = DpaConstants.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 msgid: Optional[str] = None, result: Optional[dict] = None):
        super().__init__(
            nadr=DpaConstants.COORDINATOR_NADR,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorResponseCommands.BOND_NODE,
            m_type=CoordinatorMessages.BOND_NODE,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            result=result
        )
        if rcode == ResponseCodes.OK:
            self._bond_addr = result['bondAddr']
            self._dev_nr = result['devNr']

    def get_bond_addr(self) -> int:
        return self._bond_addr

    def get_dev_nr(self) -> int:
        return self._dev_nr

    @staticmethod
    def from_dpa(dpa: bytes) -> BondNodeResponse:
        IResponse.validate_dpa_response(dpa)
        hwpid = Common.hwpid_from_dpa(dpa[ResponsePacketMembers.HWPID_HI], dpa[ResponsePacketMembers.HWPID_LO])
        rcode = dpa[ResponsePacketMembers.RCODE]
        result = None
        if rcode == ResponseCodes.OK:
            if len(dpa) != 10:
                raise DpaResponsePacketLengthError('Invalid DPA response packet length.')
            result = {'bondAddr': dpa[8], 'devNr': dpa[9]}
        return BondNodeResponse(hwpid=hwpid, rcode=rcode, dpa_value=dpa[ResponsePacketMembers.DPA_VALUE], result=result)

    @staticmethod
    def from_json(json: dict) -> BondNodeResponse:
        msgid = Common.msgid_from_json(json)
        hwpid = Common.hwpid_from_json(json)
        dpa_value = Common.dpa_value_from_json(json)
        rcode = Common.rcode_from_json(json)
        result = Common.result_from_json(json) if rcode == ResponseCodes.OK else None
        return BondNodeResponse(msgid=msgid, hwpid=hwpid, dpa_value=dpa_value, rcode=rcode, result=result)
