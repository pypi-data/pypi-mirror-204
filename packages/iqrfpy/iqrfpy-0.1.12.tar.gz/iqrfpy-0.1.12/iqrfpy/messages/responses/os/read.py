from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from iqrfpy.messages.responses.iresponse import IResponseGetterMixin
from iqrfpy.enums.commands import OSResponseCommands
from iqrfpy.enums.message_types import OSMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.utils.common import Common
from iqrfpy.utils.dpa import ResponsePacketMembers, ResponseCodes
from iqrfpy.utils.validators import DpaValidator, JsonValidator

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
class OsReadSlotLimits:

    __slots__ = 'shortest_timeslot', 'longest_timeslot'

    def __init__(self, slot_limits):
        self.shortest_timeslot = (slot_limits >> 4) & 0x0F
        self.longest_timeslot = slot_limits & 0x0F


@dataclass
class OsReadFlags:

    __slots__ = 'insufficient_os_version', 'spi_interface_supported', 'uart_interface_supported',\
        'custom_dpa_handler_detected', 'custom_dpa_handler_not_detected_enabled', 'no_interface_supported', \
        'original_os', 'frc_aggregation'

    def __init__(self, flags):
        bits = [int(bit) for bit in f'{flags:08b}']
        self.insufficient_os_version: bool = bool(bits[0])
        self.custom_dpa_handler_detected: bool = bool(bits[2])
        self.custom_dpa_handler_not_detected_enabled: bool = bool(bits[3])
        self.no_interface_supported: bool = bool(bits[4])
        if not self.no_interface_supported:
            self.spi_interface_supported = bits[1] == 0
            self.uart_interface_supported = not self.spi_interface_supported
        else:
            self.spi_interface_supported = self.uart_interface_supported = False
        self.original_os: bool = bool(bits[5])
        self.frc_aggregation: bool = bool(bits[6])


@dataclass
class OsReadData:

    __slots__ = 'mid', 'os_version', 'mcu_type', 'os_build', 'rssi', 'supply_voltage', 'flags', 'slot_limits', 'ibk',\
        'per_enum'

    def __init__(self, result: dict):
        self.mid = [
            result['mid'] & 0xFF,
            (result['mid'] >> 8) & 0xFF,
            (result['mid'] >> 16) & 0xFF,
            (result['mid'] >> 24) & 0xFF
        ]
        self.os_version = result['osVersion']
        self.mcu_type = result['trMcuType']
        self.os_build = result['osBuild']
        self.rssi = result['rssi']
        self.supply_voltage = result['supplyVoltage']
        self.flags = result['flags']
        self.slot_limits = result['slotLimits']
        self.ibk = result['ibk']
        self.per_enum = PeripheralEnumerationData(result)

    def get_mid(self) -> int:
        return (self.mid[3] << 24) + (self.mid[2] << 16) + (self.mid[1] << 8) + self.mid[0]

    def get_os_version(self):
        return self.os_version

    def get_mcu_type(self):
        return self.mcu_type

    def get_os_build(self):
        return self.os_build

    def get_rssi(self):
        return self.rssi

    def get_supply_voltage(self) -> float:
        return self.supply_voltage

    def get_flags(self) -> OsReadFlags:
        return OsReadFlags(self.flags)

    def get_slot_limits(self):
        return OsReadSlotLimits(self.slot_limits)

    def get_ibk(self):
        return Common.list_to_hex_string(self.ibk)


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
        if rcode == ResponseCodes.OK:
            self._os_response = OsReadData(result=result)

    def get_os_read_data(self) -> OsReadData:
        return self._os_response

    @staticmethod
    def from_dpa(dpa: bytes) -> ReadResponse:
        DpaValidator.base_response_length(dpa=dpa)
        nadr = dpa[ResponsePacketMembers.NADR]
        hwpid = Common.hwpid_from_dpa(dpa[ResponsePacketMembers.HWPID_HI], dpa[ResponsePacketMembers.HWPID_LO])
        rcode = dpa[ResponsePacketMembers.RCODE]
        dpa_value = dpa[ResponsePacketMembers.DPA_VALUE]
        result = None
        if rcode == ResponseCodes.OK:
            DpaValidator.response_length(dpa=dpa, expected_len=48)
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
        JsonValidator.response_received(json)
        nadr = Common.nadr_from_json(json)
        msgid = Common.msgid_from_json(json)
        hwpid = Common.hwpid_from_json(json)
        dpa_value = Common.dpa_value_from_json(json)
        rcode = Common.rcode_from_json(json)
        result = Common.result_from_json(json) if rcode == ResponseCodes.OK else None
        return ReadResponse(nadr=nadr, msgid=msgid, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, result=result)
