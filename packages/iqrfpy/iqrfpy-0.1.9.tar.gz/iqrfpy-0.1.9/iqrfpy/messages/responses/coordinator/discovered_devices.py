from __future__ import annotations
from typeguard import typechecked
from typing import List, Optional
from iqrfpy.enums.commands import CoordinatorResponseCommands
from iqrfpy.enums.message_types import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import DpaResponsePacketLengthError
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as DpaConstants
from iqrfpy.utils.dpa import ResponseCodes, ResponsePacketMembers
from iqrfpy.messages.responses.iresponse import IResponse, IResponseGetterMixin

__all__ = ['DiscoveredDevicesResponse']


@typechecked
class DiscoveredDevicesResponse(IResponseGetterMixin):
    __slots__ = '_discovered'

    def __init__(self, hwpid: int = DpaConstants.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 msgid: Optional[str] = None, result: Optional[dict] = None):
        super().__init__(
            nadr=DpaConstants.COORDINATOR_NADR,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorResponseCommands.DISCOVERED_DEVICES,
            m_type=CoordinatorMessages.DISCOVERED_DEVICES,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            result=result
        )
        if rcode == ResponseCodes.OK:
            self._discovered = result['discoveredDevices']

    def get_discovered(self) -> List[int]:
        return self._discovered

    @staticmethod
    def from_dpa(dpa: bytes) -> DiscoveredDevicesResponse:
        IResponse.validate_dpa_response(dpa)
        hwpid = Common.hwpid_from_dpa(dpa[ResponsePacketMembers.HWPID_HI], dpa[ResponsePacketMembers.HWPID_LO])
        rcode = dpa[ResponsePacketMembers.RCODE]
        result = None
        if rcode == ResponseCodes.OK:
            if len(dpa) != 40:
                raise DpaResponsePacketLengthError('Invalid DPA response packet length.')
            result = {'discoveredDevices': Common.bitmap_to_nodes(list(dpa[8:]))}
        return DiscoveredDevicesResponse(hwpid=hwpid, rcode=rcode, dpa_value=dpa[ResponsePacketMembers.DPA_VALUE],
                                         result=result)

    @staticmethod
    def from_json(json: dict) -> DiscoveredDevicesResponse:
        msgid = Common.msgid_from_json(json)
        hwpid = Common.hwpid_from_json(json)
        dpa_value = Common.dpa_value_from_json(json)
        rcode = Common.rcode_from_json(json)
        result = Common.result_from_json(json) if rcode == ResponseCodes.OK else None
        return DiscoveredDevicesResponse(msgid=msgid, hwpid=hwpid, dpa_value=dpa_value, rcode=rcode, result=result)
