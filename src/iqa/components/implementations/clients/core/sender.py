from typing import TYPE_CHECKING

from iqa.abstract.client.sender import Sender
from iqa.components.implementations.clients.core.client import CoreMessagingClient

if TYPE_CHECKING:
    from iqa.abstract.listener import Listener
    from iqa.abstract.message.message import Message
    from iqa.system.node.base.node import Node


class SenderCore(CoreMessagingClient, Sender):
    """Core python sender client."""

    def __init__(self, name: str, node: 'Node'):
        super().__init__(name, node)
        #  TODO - Define what kind of object the core sender is going to use (maybe the default for python ext. client)

    def set_endpoint(self, listener: 'Listener') -> None:
        pass

    def connect(self) -> bool:
        pass

    def set_url(self, url: str) -> None:
        pass

    def _send(self, message: 'Message', **kwargs) -> None:
        pass
