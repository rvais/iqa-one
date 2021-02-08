from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, List
    from iqa.abstract.listener import Listener
    from iqa.components.abstract.network.protocol.protocol import Protocol


class Client(ABC):
    """
    Abstract class for every abstract client
    """

    def __init__(self, **kwargs) -> None:
        self._url = None  # connectionUrl
        self._users = None
        self._logs = None

    @property
    @abstractmethod
    def name(self) -> 'Optional[str]':
        """

        :return: String
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def version(self) -> 'Optional[str]':
        """

        :return: String
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def supported_protocols(self) -> List[Protocol]:
        """

        :return: List
        """
        raise NotImplementedError

    @abstractmethod
    def set_url(self, url: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_endpoint(self, listener: 'Listener') -> None:
        raise NotImplementedError

    @abstractmethod
    def connect(self):
        """
        Create connection to the endpoint
        :return:
        :rtype:
        """

    @property
    @abstractmethod
    def implementation(self) -> str:
        raise NotImplementedError
