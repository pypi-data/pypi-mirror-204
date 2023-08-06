from __future__ import annotations
from typeguard import typechecked
from uuid import uuid4
from typing import List, Union
from iqrfpy.enums.commands import CoordinatorRequestCommands
from iqrfpy.enums.message_types import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as DpaConstants
from iqrfpy.messages.requests.irequest import IRequest

__all__ = ['SmartConnectRequest']


@typechecked
class SmartConnectRequest(IRequest):
    __slots__ = '_req_addr', '_bonding_test_retries', '_ibk', '_mid', '_virtual_device_address'

    def __init__(self, req_addr: int, bonding_test_retries: int, ibk: Union[str, List[int]], mid: int,
                 virtual_device_address: int = 0xFF, hwpid: int = DpaConstants.HWPID_MAX, msgid: str = str(uuid4())):
        super().__init__(
            nadr=DpaConstants.COORDINATOR_NADR,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorRequestCommands.SMART_CONNECT,
            m_type=CoordinatorMessages.SMART_CONNECT,
            hwpid=hwpid,
            msgid=msgid
        )
        self._req_addr = req_addr
        self._bonding_test_retries = bonding_test_retries
        self._ibk = ibk
        self._mid = mid
        self._virtual_device_address = virtual_device_address
        self._validate()

    def _validate(self) -> None:
        if self._req_addr == DpaConstants.IQMESH_TEMP_ADDR:
            if self._bonding_test_retries != DpaConstants.BYTE_MIN:
                raise RequestParameterInvalidValueError('Bonding test value must be zero if requested address \
                set to 254.')
            if len(self._ibk) != DpaConstants.IBK_LEN:
                raise RequestParameterInvalidValueError('IBK should be a string of 32 hex characters.')
            # if set(self._ibk) - set('0'):
            #    raise RequestParameterInvalidValueError('IBK values must be zero if requested address is set to 254.')
            if self._mid != DpaConstants.MID_MIN:
                raise RequestParameterInvalidValueError('MID value must be zero if requested address is set to 254.')
            if self._virtual_device_address != DpaConstants.NADR_MIN:
                raise RequestParameterInvalidValueError('VRN value must be zero if requested address is set to 254.')
            return
        if self._req_addr < DpaConstants.NODE_NADR_MIN or self._req_addr > DpaConstants.NODE_NADR_MAX:
            raise RequestParameterInvalidValueError('Requested address value should be between 1 and 239, or 254.')
        if self._bonding_test_retries < DpaConstants.BYTE_MIN or self._bonding_test_retries > DpaConstants.BYTE_MAX:
            raise RequestParameterInvalidValueError('Bonding test retries value should be between 0 and 255.')
        if len(self._ibk) != DpaConstants.IBK_LEN:
            raise RequestParameterInvalidValueError('IBK should be a string of 32 hex characters.')
        if not Common.is_hex_string(self._ibk):
            raise RequestParameterInvalidValueError('IBK string should only contain hexadecimal characters.')
        if self._mid < DpaConstants.MID_MIN or self._mid > DpaConstants.MID_MAX:
            raise RequestParameterInvalidValueError('MID value should be an unsigned 32bit integer.')
        if (self._virtual_device_address < DpaConstants.NODE_NADR_MIN
            or self._virtual_device_address > DpaConstants.NODE_NADR_MAX) \
                and self._virtual_device_address != DpaConstants.VDA_UNUSED:
            raise RequestParameterInvalidValueError('VRN value should be between 1 and 239, or 255.')

    def set_req_addr(self, req_addr: int) -> None:
        self._req_addr = req_addr

    def set_bonding_test_retries(self, bonding_test_retries: int) -> None:
        self._bonding_test_retries = bonding_test_retries

    def set_ibk(self, ibk: str) -> None:
        self._ibk = ibk

    def set_mid(self, mid: int) -> None:
        self._mid = mid

    def set_virtual_device_address(self, virtual_device_address: int) -> None:
        self._virtual_device_address = virtual_device_address

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        self._validate()
        self._pdata = [self._req_addr, self._bonding_test_retries].extend(
            Common.hex_string_to_list(self._ibk)
        )
        params = [self._req_addr, self._bonding_test_retries]
        params.extend(Common.hex_string_to_list(self._ibk))
        params.extend([
            self._mid & 0xFF,
            (self._mid >> 8) & 0xFF,
            (self._mid >> 16) & 0xFF,
            (self._mid >> 24) & 0xFF,
            0,
            self._virtual_device_address,
        ])
        params.extend([0] * 14)
        self._pdata = params
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._validate()
        self._params = {
            'reqAddr': self._req_addr,
            'bondingTestRetries': self._bonding_test_retries,
            'ibk': Common.hex_string_to_list(self._ibk),
            'mid': self._mid,
            'virtualDeviceAddress': self._virtual_device_address,
            'userData': [0, 0, 0, 0]
        }
        return super().to_json()
