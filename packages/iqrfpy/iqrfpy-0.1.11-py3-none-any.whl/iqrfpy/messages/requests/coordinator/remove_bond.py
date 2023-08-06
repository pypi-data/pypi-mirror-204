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

__all__ = ['RemoveBondRequest']


@typechecked
class RemoveBondRequest(IRequest):
    __slots__ = '_bond_addr'

    def __init__(self, bond_addr: int, hwpid: int = DpaConstants.HWPID_MAX, msgid: str = str(uuid4())):
        super().__init__(
            nadr=DpaConstants.COORDINATOR_NADR,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorRequestCommands.REMOVE_BOND,
            m_type=CoordinatorMessages.REMOVE_BOND,
            hwpid=hwpid,
            msgid=msgid
        )
        self._bond_addr = bond_addr
        self._validate()

    def _validate(self) -> None:
        if self._bond_addr < DpaConstants.NODE_NADR_MIN or self._bond_addr > DpaConstants.NODE_NADR_MAX:
            raise RequestParameterInvalidValueError('Bond address value should be between 1 and 239.')

    def set_bond_addr(self, bond_addr: int) -> None:
        self._bond_addr = bond_addr

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        self._validate()
        self._pdata = [self._bond_addr]
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._validate()
        self._params = {'bondAddr': self._bond_addr}
        return super().to_json()
