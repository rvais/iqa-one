import logging
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

    def __init__(self, name: 'Optional[str]' = None, version: 'Optional[str]' = None, **kwargs) -> None:
        super(Client, self).__init__(**kwargs)
        self._version = version
        self._url = None  # connectionUrl
        self._users = None
        self._logs = None

        # Changes necessary due to the fact this class is used as one of the bases in multiple inheritance
        if not hasattr(self, '_name') and name is not None:
            self._name = name
        elif not hasattr(self, '_name') and name is None:
            self._name = self.__class__.__name__

        if not hasattr(self, '_logger') or not isinstance(self._logger, logging.Logger):
            self._logger: logging.Logger = logging.getLogger(self._name)

    @property
    def name(self) -> 'Optional[str]':
        """

        :return: String
        """
        return self._name

    @property
    def version(self) -> 'Optional[str]':
        """

        :return: String
        """
        return self._version

    @property
    @abstractmethod
    def supported_protocols(self) -> 'List[Protocol]':
        """

        :return: List
        """
        raise NotImplementedError

    @property
    def url(self) -> 'Optional[str]':
        return self._url

    def get_url(self) -> 'Optional[str]':
        return self.url

    @url.setter
    @abstractmethod
    def _set_url(self, url: str) -> None:
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
        raise NotImplementedError

    @property
    @abstractmethod
    def implementation(self) -> str:
        raise NotImplementedError
