from __future__ import annotations
from typeguard import typechecked
from uuid import uuid4
from typing import Union
from iqrfpy.enums.commands import LEDRequestCommands
from iqrfpy.enums.message_types import LEDRMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
import iqrfpy.utils.dpa as DpaConstants
from iqrfpy.messages.requests.irequest import IRequest

__all__ = ['PulseRequest']


@typechecked
class PulseRequest(IRequest):

    def __init__(self, nadr: int, hwpid: int = DpaConstants.HWPID_MAX, msgid: str = str(uuid4())):
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.LEDR,
            pcmd=LEDRequestCommands.PULSE,
            m_type=LEDRMessages.PULSE,
            hwpid=hwpid,
            msgid=msgid
        )

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        return super().to_json()
