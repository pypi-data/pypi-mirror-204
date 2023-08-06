from __future__ import annotations
from typeguard import typechecked
from uuid import uuid4
from typing import Union
from iqrfpy.enums.commands import NodeRequestCommands
from iqrfpy.enums.message_types import NodeMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
import iqrfpy.utils.dpa as DpaConstants
from iqrfpy.messages.requests.irequest import IRequest

__all__ = ['ReadRequest']


@typechecked
class ReadRequest(IRequest):

    def __init__(self, nadr: int, hwpid: int = DpaConstants.HWPID_MAX, msgid: str = str(uuid4())):
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.NODE,
            pcmd=NodeRequestCommands.READ,
            m_type=NodeMessages.READ,
            hwpid=hwpid,
            msgid=msgid
        )

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        return super().to_json()
