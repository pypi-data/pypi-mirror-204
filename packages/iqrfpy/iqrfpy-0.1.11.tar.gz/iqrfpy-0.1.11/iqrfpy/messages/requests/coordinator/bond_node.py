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

__all__ = ['BondNodeRequest']


@typechecked
class BondNodeRequest(IRequest):
    __slots__ = '_req_addr', '_bonding_test_retries'

    def __init__(self, req_addr: int, bonding_test_retries: int, hwpid: int = DpaConstants.HWPID_MAX,
                 msgid: str = str(uuid4())) -> None:
        super().__init__(
            nadr=DpaConstants.COORDINATOR_NADR,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorRequestCommands.BOND_NODE,
            m_type=CoordinatorMessages.BOND_NODE,
            hwpid=hwpid,
            msgid=msgid
        )
        self._req_addr = req_addr
        self._bonding_test_retries = bonding_test_retries
        self._validate()

    def _validate(self) -> None:
        if self._req_addr == DpaConstants.IQUIP_NADR and self._bonding_test_retries == 0:
            return
        if self._req_addr < DpaConstants.NADR_MIN or self._req_addr > DpaConstants.NADR_MAX:
            raise RequestParameterInvalidValueError('Address value should be between 0 and 239. Value 240 is allowed \
            combination with bonding test retries value 0.')
        if self._bonding_test_retries < DpaConstants.BYTE_MIN or self._bonding_test_retries > DpaConstants.BYTE_MAX:
            raise RequestParameterInvalidValueError('Bonding test retries value should be between 0 and 255.')

    def set_req_addr(self, req_addr: int) -> None:
        self._req_addr = req_addr

    def set_bonding_test_retries(self, bonding_test_retries: int) -> None:
        self._bonding_test_retries = bonding_test_retries

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        self._validate()
        self._pdata = [self._req_addr, self._bonding_test_retries]
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._validate()
        self._params = {'reqAddr': self._req_addr, 'bondingMask': self._bonding_test_retries}
        return super().to_json()
