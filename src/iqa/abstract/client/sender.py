from abc import abstractmethod
from typing import TYPE_CHECKING

from iqa.abstract.client.messaging_client import MessagingClient

if TYPE_CHECKING:
    from iqa.abstract.message.message import Message


class Sender(MessagingClient):
    """Abstract class of sender client."""

    def __init__(self, **kwargs) -> None:
        super(Sender, self).__init__(**kwargs)
        # Sender settings

    def send(self, message: 'Message', **kwargs) -> None:
        """Method for sending a message.
        :param message: Message to be sent
        :type: iqa.iqa.abstract.message.Message
        """
        if self.message_buffer:
            self.messages.append(message)  # single sent Message

        self.message_counter += 1
        self._send(message, **kwargs)

    @abstractmethod
    def _send(self, message: 'Message', **kwargs) -> None:
        raise NotImplementedError
