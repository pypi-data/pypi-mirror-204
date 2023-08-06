from __future__ import annotations
from typeguard import typechecked
from typing import Optional
from iqrfpy.enums.peripherals import Peripheral
from iqrfpy.enums.commands import Command
from iqrfpy.enums.message_types import GenericMessages
from .iresponse import IResponse, IResponseGetterMixin
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as DpaConstants
from iqrfpy.utils.dpa import ResponsePacketMembers

__all__ = ['AsyncResponse']


@typechecked
class AsyncResponse(IResponseGetterMixin):

    def __init__(self, nadr: int, pnum: Peripheral, pcmd: Command, hwpid: int = DpaConstants.HWPID_MAX,
                 rcode: int = 0x80, dpa_value: int = 0, pdata: Optional[bytes] = None, msgid: Optional[str] = None,
                 result: Optional[dict] = None):
        super().__init__(
            nadr=nadr,
            pnum=pnum,
            pcmd=pcmd,
            m_type=GenericMessages.RAW,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            pdata=pdata,
            msgid=msgid,
            result=result
        )

    @staticmethod
    def from_dpa(dpa: bytes) -> AsyncResponse:
        IResponse.validate_dpa_response(dpa)
        hwpid = Common.hwpid_from_dpa(dpa[ResponsePacketMembers.HWPID_HI], dpa[ResponsePacketMembers.HWPID_LO])
        pnum = Common.pnum_from_dpa(dpa[ResponsePacketMembers.PNUM])
        pcmd = Common.request_pcmd_from_dpa(pnum, dpa[ResponsePacketMembers.PCMD])
        rcode = dpa[ResponsePacketMembers.RCODE]
        result = None
        if rcode == DpaConstants.ASYNC_RESPONSE_CODE:
            if len(dpa) > 8:
                result = {'rData': list(dpa)}
        return AsyncResponse(nadr=dpa[ResponsePacketMembers.NADR], pnum=pnum, pcmd=pcmd, hwpid=hwpid, rcode=rcode,
                             dpa_value=dpa[ResponsePacketMembers.DPA_VALUE], pdata=dpa, result=result)

    @staticmethod
    def from_json(json: dict) -> AsyncResponse:
        msgid = Common.msgid_from_json(json)
        result = json['data']['rsp']
        packet = result['rData'].replace('.', '')
        pdata = bytes.fromhex(packet)
        ldata = Common.hex_string_to_list(packet)
        hwpid = Common.hwpid_from_dpa(ldata[ResponsePacketMembers.HWPID_HI], ldata[ResponsePacketMembers.HWPID_LO])
        pnum = Common.pnum_from_dpa(ldata[ResponsePacketMembers.PNUM])
        pcmd = Common.request_pcmd_from_dpa(pnum, ldata[ResponsePacketMembers.PCMD])
        return AsyncResponse(nadr=ldata[ResponsePacketMembers.NADR], pnum=pnum, pcmd=pcmd, hwpid=hwpid,
                             rcode=ldata[ResponsePacketMembers.RCODE], dpa_value=ldata[ResponsePacketMembers.DPA_VALUE],
                             pdata=pdata, msgid=msgid, result=result)
