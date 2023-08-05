from abc import ABC, abstractmethod
from typing import Union
from ..enums.commands import *
from ..enums.message_types import *
from ..enums.peripherals import *
from .responses.async_response import AsyncResponse
from .responses.confirmation import Confirmation
from .responses.iresponse import IResponse
from .responses.coordinator import *
import iqrfpy.messages.responses.os as OsResponses
import iqrfpy.messages.responses.ledr as LedrResponses
from ..utils.common import Common
from ..utils.dpa import *
from ..exceptions import UnsupportedMessageTypeError, UnsupportedPeripheralError, UnsupportedPeripheralCommandError

__all__ = [
    'ResponseFactory',
    'AsyncResponseFactory',
    'ConfirmationFactory',
    'CoordinatorAddrInfoFactory',
    'CoordinatorAuthorizeBondFactory',
    'CoordinatorBackupFactory',
    'CoordinatorBondedDevicesFactory',
    'CoordinatorBondNodeFactory',
    'CoordinatorClearAllBondsFactory',
    'CoordinatorDiscoveredDevicesFactory',
    'CoordinatorDiscoveryFactory',
    'CoordinatorRemoveBondFactory',
    'CoordinatorRestoreFactory',
    'CoordinatorSetDpaParamsFactory',
    'CoordinatorSetHopsFactory',
    'CoordinatorSetMIDFactory',
    'CoordinatorSmartConnectFactory'
]


class ResponseFactory:

    @staticmethod
    def get_response_from_dpa(dpa: bytes) -> IResponse:
        IResponse.validate_dpa_response(dpa)
        pnum = dpa[ResponsePacketMembers.PNUM]
        pcmd = dpa[ResponsePacketMembers.PCMD]
        rcode = dpa[ResponsePacketMembers.RCODE]
        if rcode == CONFIRMATION_RCODE and len(dpa) == CONFIRMATION_PACKET_LEN:
            factory = ConfirmationFactory()
        elif pcmd <= REQUEST_PCMD_MAX and rcode >= ASYNC_RESPONSE_CODE:
            factory = AsyncResponseFactory()
        else:
            peripheral = Common.pnum_from_dpa(pnum)
            command = Common.response_pcmd_from_dpa(peripheral, pcmd)
            factory = _get_factory_from_dpa(peripheral, command)
        return factory.create_from_dpa(dpa)

    @staticmethod
    def get_response_from_json(json: dict) -> IResponse:
        msgid = Common.msgid_from_json(json)
        mtype = Common.mtype_str_from_json(json)
        if msgid == IResponse.ASYNC_MSGID and \
                GenericMessages.has_value(mtype) and GenericMessages(mtype) == GenericMessages.RAW:
            factory = AsyncResponseFactory()
        else:
            message = Common.string_to_mtype(mtype)
            factory = _get_factory_from_mtype(message)
        return factory.create_from_json(json)


class BaseFactory(ABC):

    @abstractmethod
    def create_from_dpa(self, dpa: bytes) -> IResponse:
        """Returns a response object created from DPA message."""

    @abstractmethod
    def create_from_json(self, json: dict) -> IResponse:
        """Returns a response object created from JSON API message."""

# Coordinator factories


class ConfirmationFactory(BaseFactory):
    def create_from_dpa(self, dpa: bytes) -> Confirmation:
        return Confirmation.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> Confirmation:
        return Confirmation.from_json(json=json)


class AsyncResponseFactory(BaseFactory):
    def create_from_dpa(self, dpa: bytes) -> IResponse:
        return AsyncResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> IResponse:
        return AsyncResponse.from_json(json=json)


class CoordinatorAddrInfoFactory(BaseFactory):

    def create_from_dpa(self, dpa: bytes) -> AddrInfoResponse:
        return AddrInfoResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> AddrInfoResponse:
        return AddrInfoResponse.from_json(json=json)


class CoordinatorAuthorizeBondFactory(BaseFactory):

    def create_from_dpa(self, dpa: bytes) -> AuthorizeBondResponse:
        return AuthorizeBondResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> AuthorizeBondResponse:
        return AuthorizeBondResponse.from_json(json=json)


class CoordinatorBackupFactory(BaseFactory):

    def create_from_dpa(self, dpa: bytes) -> BackupResponse:
        return BackupResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> BackupResponse:
        return BackupResponse.from_json(json=json)


class CoordinatorBondedDevicesFactory(BaseFactory):
    def create_from_dpa(self, dpa: bytes) -> BondedDevicesResponse:
        return BondedDevicesResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> BondedDevicesResponse:
        return BondedDevicesResponse.from_json(json=json)


class CoordinatorBondNodeFactory(BaseFactory):
    def create_from_dpa(self, dpa: bytes) -> BondNodeResponse:
        return BondNodeResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> BondNodeResponse:
        return BondNodeResponse.from_json(json=json)


class CoordinatorClearAllBondsFactory(BaseFactory):
    def create_from_dpa(self, dpa: bytes) -> ClearAllBondsResponse:
        return ClearAllBondsResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> ClearAllBondsResponse:
        return ClearAllBondsResponse.from_json(json=json)


class CoordinatorDiscoveredDevicesFactory(BaseFactory):
    def create_from_dpa(self, dpa: bytes) -> DiscoveredDevicesResponse:
        return DiscoveredDevicesResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> DiscoveredDevicesResponse:
        return DiscoveredDevicesResponse.from_json(json=json)


class CoordinatorDiscoveryFactory(BaseFactory):
    def create_from_dpa(self, dpa: bytes) -> DiscoveryResponse:
        return DiscoveryResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> DiscoveryResponse:
        return DiscoveryResponse.from_json(json=json)


class CoordinatorRemoveBondFactory(BaseFactory):
    def create_from_dpa(self, dpa: bytes) -> RemoveBondResponse:
        return RemoveBondResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> RemoveBondResponse:
        return RemoveBondResponse.from_json(json=json)


class CoordinatorRestoreFactory(BaseFactory):
    def create_from_dpa(self, dpa: bytes) -> RestoreResponse:
        return RestoreResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> RestoreResponse:
        return RestoreResponse.from_json(json=json)


class CoordinatorSetDpaParamsFactory(BaseFactory):
    def create_from_dpa(self, dpa: bytes) -> SetDpaParamsResponse:
        return SetDpaParamsResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> SetDpaParamsResponse:
        return SetDpaParamsResponse.from_json(json=json)


class CoordinatorSetHopsFactory(BaseFactory):
    def create_from_dpa(self, dpa: bytes) -> SetHopsResponse:
        return SetHopsResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> SetHopsResponse:
        return SetHopsResponse.from_json(json=json)


class CoordinatorSetMIDFactory(BaseFactory):
    def create_from_dpa(self, dpa: bytes) -> SetMIDResponse:
        return SetMIDResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> SetMIDResponse:
        return SetMIDResponse.from_json(json=json)


class CoordinatorSmartConnectFactory(BaseFactory):
    def create_from_dpa(self, dpa: bytes) -> SmartConnectResponse:
        return SmartConnectResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> SmartConnectResponse:
        return SmartConnectResponse.from_json(json=json)


# OS factories


class OSReadFactory(BaseFactory):

    def create_from_dpa(self, dpa: bytes) -> OsResponses.ReadResponse:
        return OsResponses.ReadResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> OsResponses.ReadResponse:
        return OsResponses.ReadResponse.from_json(json=json)


# LEDR factories


class LedrSetOnFactory(BaseFactory):

    def create_from_dpa(self, dpa: bytes) -> LedrResponses.SetOnResponse:
        return LedrResponses.SetOnResponse.from_dpa(dpa)

    def create_from_json(self, json: dict) -> LedrResponses.SetOnResponse:
        return LedrResponses.SetOnResponse.from_json(json)


class LedrSetOffFactory(BaseFactory):

    def create_from_dpa(self, dpa: bytes) -> LedrResponses.SetOffResponse:
        return LedrResponses.SetOffResponse.from_dpa(dpa)

    def create_from_json(self, json: dict) -> LedrResponses.SetOffResponse:
        return LedrResponses.SetOffResponse.from_json(json)


class LedrPulseFactory(BaseFactory):

    def create_from_dpa(self, dpa: bytes) -> LedrResponses.PulseResponse:
        return LedrResponses.PulseResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> LedrResponses.PulseResponse:
        return LedrResponses.PulseResponse.from_json(json=json)


class LedrFlashingFactory(BaseFactory):

    def create_from_dpa(self, dpa: bytes) -> LedrResponses.FlashingResponse:
        return LedrResponses.FlashingResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> LedrResponses.FlashingResponse:
        return LedrResponses.FlashingResponse.from_json(json=json)


def _get_factory_from_dpa(pnum: Union[EmbedPeripherals, Standards], pcmd: Command) -> BaseFactory:
    factories = {
        EmbedPeripherals.COORDINATOR: {
            CoordinatorResponseCommands.ADDR_INFO: CoordinatorAddrInfoFactory(),
            CoordinatorResponseCommands.AUTHORIZE_BOND: CoordinatorAuthorizeBondFactory(),
            CoordinatorResponseCommands.BACKUP: CoordinatorBackupFactory(),
            CoordinatorResponseCommands.BONDED_DEVICES: CoordinatorBondedDevicesFactory(),
            CoordinatorResponseCommands.BOND_NODE: CoordinatorBondNodeFactory(),
            CoordinatorResponseCommands.CLEAR_ALL_BONDS: CoordinatorClearAllBondsFactory(),
            CoordinatorResponseCommands.DISCOVERED_DEVICES: CoordinatorDiscoveredDevicesFactory(),
            CoordinatorResponseCommands.DISCOVERY: CoordinatorDiscoveryFactory(),
            CoordinatorResponseCommands.REMOVE_BOND: CoordinatorRemoveBondFactory(),
            CoordinatorResponseCommands.RESTORE: CoordinatorRestoreFactory(),
            CoordinatorResponseCommands.SET_DPA_PARAMS: CoordinatorSetDpaParamsFactory(),
            CoordinatorResponseCommands.SET_HOPS: CoordinatorSetHopsFactory(),
            CoordinatorResponseCommands.SET_MID: CoordinatorSetMIDFactory(),
            CoordinatorResponseCommands.SMART_CONNECT: CoordinatorSmartConnectFactory(),
        },
        EmbedPeripherals.OS: {
            OSResponseCommands.READ: OSReadFactory(),
        },
        EmbedPeripherals.LEDR: {
            LEDResponseCommands.SET_ON: LedrSetOnFactory(),
            LEDResponseCommands.SET_OFF: LedrSetOffFactory(),
            LEDResponseCommands.PULSE: LedrPulseFactory(),
            LEDResponseCommands.FLASHING: LedrFlashingFactory(),
        }
    }
    if pnum in factories:
        if pcmd in factories[pnum]:
            return factories[pnum][pcmd]
        raise UnsupportedPeripheralCommandError(f'Unknown or unsupported peripheral command: {pcmd}')
    raise UnsupportedPeripheralError(f'Unknown or unsupported peripheral: {pnum}')


def _get_factory_from_mtype(mtype: MessageType) -> BaseFactory:
    factories = {
        CoordinatorMessages.ADDR_INFO: CoordinatorAddrInfoFactory(),
        CoordinatorMessages.AUTHORIZE_BOND: CoordinatorAuthorizeBondFactory(),
        CoordinatorMessages.BACKUP: CoordinatorBackupFactory(),
        CoordinatorMessages.BONDED_DEVICES: CoordinatorBondedDevicesFactory(),
        CoordinatorMessages.BOND_NODE: CoordinatorBondNodeFactory(),
        CoordinatorMessages.CLEAR_ALL_BONDS: CoordinatorClearAllBondsFactory(),
        CoordinatorMessages.DISCOVERED_DEVICES: CoordinatorDiscoveredDevicesFactory(),
        CoordinatorMessages.DISCOVERY: CoordinatorDiscoveryFactory(),
        CoordinatorMessages.REMOVE_BOND: CoordinatorRemoveBondFactory(),
        CoordinatorMessages.RESTORE: CoordinatorRestoreFactory(),
        CoordinatorMessages.SET_DPA_PARAMS: CoordinatorSetDpaParamsFactory(),
        CoordinatorMessages.SET_HOPS: CoordinatorSetHopsFactory(),
        CoordinatorMessages.SET_MID: CoordinatorSetMIDFactory(),
        CoordinatorMessages.SMART_CONNECT: CoordinatorSmartConnectFactory(),
        OSMessages.READ: OSReadFactory(),
        LEDRMessages.SET_ON: LedrSetOnFactory(),
        LEDRMessages.SET_OFF: LedrSetOffFactory(),
        LEDRMessages.PULSE: LedrPulseFactory(),
        LEDRMessages.FLASHING: LedrFlashingFactory(),
    }

    if mtype in factories:
        return factories[mtype]
    raise UnsupportedMessageTypeError(f'Unknown or unsupported message type: {mtype}')
