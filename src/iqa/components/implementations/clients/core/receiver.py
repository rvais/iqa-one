from typing import TYPE_CHECKING

from iqa.abstract.client.receiver import Receiver
from iqa.components.implementations.clients.core.client import CoreMessagingClient

if TYPE_CHECKING:
    from iqa.abstract.listener import Listener
    from iqa.system.node.base.node import Node


class ReceiverCore(CoreMessagingClient, Receiver):
    """Core python receiver client."""

    def __init__(self, name: str, node: 'Node') -> None:
        super(ReceiverCore, self).__init__(name, node)
        #  TODO - Define what kind of object the core receiver is
        #   going to use (maybe the default for python ext. client)

    def set_endpoint(self, listener: 'Listener') -> None:
        pass

    def connect(self) -> bool:
        pass

    def set_url(self, url: str) -> None:
        pass

    def _receive(self):
        pass
