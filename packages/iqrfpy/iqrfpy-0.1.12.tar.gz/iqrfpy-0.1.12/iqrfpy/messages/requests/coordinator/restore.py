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

__all__ = ['RestoreRequest']


@typechecked
class RestoreRequest(IRequest):
    __slots__ = '_network_data'

    def __init__(self, network_data: List[int], hwpid: int = DpaConstants.HWPID_MAX, msgid: str = str(uuid4())):
        super().__init__(
            nadr=DpaConstants.COORDINATOR_NADR,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorRequestCommands.RESTORE,
            m_type=CoordinatorMessages.RESTORE,
            hwpid=hwpid,
            msgid=msgid
        )
        self._network_data = network_data
        self._validate()

    def _validate(self) -> None:
        if not Common.values_in_byte_range(self._network_data):
            raise RequestParameterInvalidValueError('Network data block values should be between 0 and 255.')
        if len(self._network_data) != DpaConstants.BACKUP_DATA_LEN:
            raise RequestParameterInvalidValueError('Network data should be 49 blocks long.')

    def set_network_data(self, network_data: List[int]) -> None:
        self._network_data = network_data

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        self._validate()
        self._pdata = self._network_data
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._validate()
        self._params = {'networkData': self._network_data}
        return super().to_json()
