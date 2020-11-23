from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, List
    from iqa.abstract.listener import Listener


class MessagingServer(ABC):
    implementation = NotImplemented

    def __init__(self) -> None:
        self.listeners: Optional[List[Listener]] = []
        self.connectors: list = []

    @abstractmethod
    def get_url(self, port: Optional[int] = None, listener: Optional[Listener] = None) -> str:
        return NotImplemented
