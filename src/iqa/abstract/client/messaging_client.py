from abc import ABC
from typing import TYPE_CHECKING

from iqa.abstract.client.client import Client

if TYPE_CHECKING:
    from typing import Optional, List
    from iqa.abstract.message.message import Message
    from iqa.components.abstract.network.protocol.protocol import Protocol


class MessagingClient(Client, ABC):
    """
    Abstract class for every abstract messaging client
    """

    # Required variables
    supported_protocols: 'List[Protocol]' = []
    name: 'Optional[str]' = None
    version: 'Optional[str]' = None

    def __init__(self, message_buffer: bool = True, **kwargs) -> None:
        super(MessagingClient, self).__init__(**kwargs)
        self._message_buffer: bool = message_buffer
        self._messages: List[Message] = []
        self._message_counter: int = 0

    def clear_buffer(self) -> None:
        self._message_counter += self._messages
        self._messages.clear()

    @property
    def message_buffer(self) -> bool:
        return self._message_buffer

    @message_buffer.setter
    def set_message_buffer(self, message_buffer: bool) -> None:
        self._message_buffer = message_buffer
        if not message_buffer:
            self.clear_buffer()

    @property
    def messages(self) -> 'List[Message]':
        if self.message_buffer:
            return self._messages.copy()
        return []

    @property
    def message_counter(self) -> int:
        if self.message_buffer:
            return len(self._messages) + self._message_counter
        return self._message_counter

    def reset_message_counter(self) -> int:
        counter = self._message_counter
        return counter

    @property
    def last_message(self) -> 'Optional[Message]':
        """Method for picking up last received message.
        :return: Last message received or None
        :rtype: iqa.iqa.abstract.message.Message
        """
        return self.messages[-1] if self.messages else None
