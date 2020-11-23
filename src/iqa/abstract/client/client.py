from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional

from iqa.abstract.listener import Listener


class Client(ABC):
    """
    Abstract class for every abstract client
    """

    def __init__(self) -> None:
        self.url = None  # connectionUrl
        self.users = None
        self.logs = None

    @property
    @abstractmethod
    def name(self) -> Optional[str]:
        """

        :return: String
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def version(self) -> Optional[str]:
        """

        :return: String
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def supported_protocols(self) -> list:
        """

        :return: List
        """
        raise NotImplementedError

    @abstractmethod
    def set_url(self, url: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_endpoint(self, listener: Listener) -> None:
        raise NotImplementedError

    @abstractmethod
    def connect(self):
        """
        Create connection to the endpoint
        :return:
        :rtype:
        """

    @property
    def implementation(self):
        raise NotImplementedError
