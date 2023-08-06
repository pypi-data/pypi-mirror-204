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

__all__ = ['BackupRequest']


@typechecked
class BackupRequest(IRequest):
    __slots__ = '_index'

    def __init__(self, index: int = 0, hwpid: int = DpaConstants.HWPID_MAX, msgid: str = str(uuid4())):
        super().__init__(
            nadr=DpaConstants.COORDINATOR_NADR,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorRequestCommands.BACKUP,
            m_type=CoordinatorMessages.BACKUP,
            hwpid=hwpid,
            msgid=msgid
        )
        self._index = index
        self._validate()

    def _validate(self) -> None:
        if self._index < DpaConstants.BYTE_MIN or self._index > DpaConstants.BYTE_MAX:
            raise RequestParameterInvalidValueError('Index value should be between 0 and 255.')

    def set_index(self, index: int) -> None:
        self._index = index

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        self._validate()
        self._pdata = [self._index]
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._validate()
        self._params = {'index': self._index}
        return super().to_json()
