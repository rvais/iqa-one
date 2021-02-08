from abc import abstractmethod
from typing import TYPE_CHECKING

from iqa.abstract.client.messaging_client import MessagingClient
from iqa.abstract.message.message import Message

if TYPE_CHECKING:
    from typing import Union, List


class Sender(MessagingClient):
    """Abstract class of sender client."""

    def __init__(self, **kwargs) -> None:
        super(Sender, self).__init__(**kwargs)
        # Sender settings

    def send(self, messages: 'Union[Message, List[Message]]', **kwargs) -> None:
        """Method for sending a message.
        :param messages: Message or list of messages to be sent
        :type: iqa.iqa.abstract.message.Message
        """
        if isinstance(messages, Message):
            messages = [messages]

        if self.message_buffer:
            self._messages.extend(messages)  # single sent Message

        self._message_counter += 1
        self._send(messages, **kwargs)

    @abstractmethod
    def _send(self, messages: 'Union[Message, List[Message]]', **kwargs) -> None:
        raise NotImplementedError
