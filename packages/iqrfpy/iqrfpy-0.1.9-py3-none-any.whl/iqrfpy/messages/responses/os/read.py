from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from iqrfpy.messages.responses.iresponse import IResponse, IResponseGetterMixin
from iqrfpy.enums.commands import OSResponseCommands
from iqrfpy.enums.message_types import OSMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import DpaResponsePacketLengthError
from iqrfpy.utils.common import Common
from iqrfpy.utils.dpa import ResponsePacketMembers

__all__ = ['ReadResponse', 'OsReadData']


@dataclass
class PeripheralEnumerationData:

    __slots__ = 'dpa_version', 'user_per_nr', 'embedded_pers', 'hwpid', 'hwpid_ver', 'flags', 'user_per'

    def __init__(self, result: dict):
        self.dpa_version = result['dpaVer']
        self.user_per_nr = result['perNr']
        self.embedded_pers = result['embeddedPers']
        self.hwpid = result['hwpid']
        self.hwpid_ver = result['hwpidVer']
        self.flags = result['flagsEnum']
        self.user_per = result['userPer']


@dataclass
class OsReadData:

    __slots__ = 'mid', 'os_version', 'mcu_type', 'os_build', 'rssi', 'supply_voltage', 'flags', 'slot_limits', 'ibk',\
        'per_enum'

    def __init__(self, result: dict):
        self.mid = result['mid']
        self.os_version = result['osVersion']
        self.mcu_type = result['trMcuType']
        self.os_build = result['osBuild']
        self.rssi = result['rssi']
        self.supply_voltage = result['supplyVoltage']
        self.flags = result['flags']
        self.slot_limits = result['slotLimits']
        self.ibk = result['ibk']
        self.per_enum = PeripheralEnumerationData(result)


class ReadResponse(IResponseGetterMixin):

    __slots__ = '_os_response'

    def __init__(self, nadr: int, hwpid: Common.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 msgid: Optional[str] = None, result: Optional[dict] = None):
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.OS,
            pcmd=OSResponseCommands.READ,
            m_type=OSMessages.READ,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            result=result
        )
        if rcode == 0:
            self._os_response = OsReadData(result=result)

    def get_os_read_data(self) -> OsReadData:
        return self._os_response

    @staticmethod
    def from_dpa(dpa: bytes) -> ReadResponse:
        IResponse.validate_dpa_response(dpa)
        nadr = dpa[ResponsePacketMembers.NADR]
        hwpid = Common.hwpid_from_dpa(dpa[ResponsePacketMembers.HWPID_HI], dpa[ResponsePacketMembers.HWPID_LO])
        rcode = dpa[ResponsePacketMembers.RCODE]
        dpa_value = dpa[ResponsePacketMembers.DPA_VALUE]
        result = None
        if rcode == 0:
            if len(dpa) < 48:
                raise DpaResponsePacketLengthError('Invalid DPA response packet length.')
            result = {
                'mid': (dpa[11] << 24) + (dpa[10] << 16) + (dpa[9] << 8) + dpa[8],
                'osVersion': dpa[12],
                'trMcuType': dpa[13],
                'osBuild': (dpa[15] << 8) + dpa[14],
                'rssi': dpa[16],
                'supplyVoltage': 261.12 / (127 - dpa[17]),
                'flags': dpa[18],
                'slotLimits': dpa[19],
                'ibk': list(dpa[20:36]),
                'dpaVer': (dpa[37] << 8) + dpa[36],
                'perNr': dpa[38],
                'hwpid': (dpa[44] << 8) + dpa[43],
                'hwpidVer': (dpa[46] << 8) + dpa[45],
                'flagsEnum': dpa[47],
                'userPer': [],
            }
            embed_pers_data = list(dpa[39:43])
            embedded_pers = []
            for i in range(0, len(embed_pers_data * 8)):
                if embed_pers_data[int(i / 8)] & (1 << (i % 8)) and EmbedPeripherals.has_value(i):
                    embedded_pers.append(i)
            result['embeddedPers'] = embedded_pers
            if result['perNr'] > 0:
                user_per_data = list(dpa[48:])
                user_pers = []
                for i in range(0, len(user_per_data * 8)):
                    if user_per_data[int(i / 8)] & (1 << (i % 8)):
                        user_pers.append(i + 0x20)
                result['userPer'] = user_pers
        return ReadResponse(nadr=nadr, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, result=result)

    @staticmethod
    def from_json(json: dict) -> ReadResponse:
        nadr = Common.nadr_from_json(json)
        msgid = Common.msgid_from_json(json)
        hwpid = Common.hwpid_from_json(json)
        dpa_value = Common.dpa_value_from_json(json)
        rcode = Common.rcode_from_json(json)
        status = Common.status_from_json(json)
        result = Common.result_from_json(json) if status == 0 else None
        return ReadResponse(nadr=nadr, msgid=msgid, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, result=result)
