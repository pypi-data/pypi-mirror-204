"""
Transport abstract class.
"""
from abc import ABC, abstractmethod
from typing import Callable, Optional
from iqrfpy.messages.requests.irequest import IRequest
from iqrfpy.messages.responses.iresponse import IResponse
from iqrfpy.messages.responses.confirmation import Confirmation


class ITransport(ABC):
    """
    Abstract class providing interface for communication channels.
    """

    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize transport and create a connection if applicable.

        Returns
        -------
        None
        """
        raise NotImplementedError("Abstract method not implemented.")

    @abstractmethod
    def send(self, request: IRequest) -> None:
        """
        Serialize passed request to format acceptable by the communication channel and send request.

        Parameters
        ----------
        request: IRequest
            Request to send

        Returns
        -------
        None
        """
        raise NotImplementedError("Abstract method not implemented.")

    @abstractmethod
    def send_and_receive(self, request: IRequest, timeout: Optional[int] = None) -> IResponse:
        raise NotImplementedError("Abstract method not implemented.")

    @abstractmethod
    def receive(self) -> IResponse:
        """
        Return first unhandled response.

        Returns
        -------
        response: IResponse
            Response object
        """
        raise NotImplementedError("Abstract method not implemented.")

    @abstractmethod
    def confirmation(self) -> Confirmation:
        """
        Return first unhandled confirmation.

        Returns
        -------
        confirmation: Confirmation
            Confirmation object
        """
        raise NotImplementedError("Abstract method not implemented.")

    @abstractmethod
    def set_receive_callback(self, callback: Callable[[IResponse], None]) -> None:
        """
        Receive a response asynchronously, deserialize data from communication channel to a response object
        and execute a callback if a function was passed.

        Parameters
        ----------
        callback: Callable[[IResponse], None
            Function to call once a message has been received and successfully deserialized

        Returns
        -------
        None
        """
        raise NotImplementedError("Abstract method not implemented.")
