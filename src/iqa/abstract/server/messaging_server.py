from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, List, Any
    from iqa.abstract.listener import Listener


class MessagingServer(ABC):
    implementation = NotImplemented

    def __init__(self, **kwargs) -> None:
        self.listeners: List[Listener] = []
        self.connectors: List[Any] = []

    @abstractmethod
    def get_url(self, port: Optional[int] = None, listener: Optional[Listener] = None) -> str:
        return NotImplemented
