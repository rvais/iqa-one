from abc import abstractmethod

from iqa.abstract.client.messaging_client import MessagingClient


class Receiver(MessagingClient):
    """Abstract class of client's receivers."""

    def __init__(self, message_buffer: bool = True) -> None:
        super(Receiver, self).__init__(message_buffer)
        # Sender settings

    def receive(self) -> None:
        """Method for receiving messages.
        """
        recv_messages: list = self._receive()

        if self.message_buffer:
            self._messages.extend(recv_messages)  # multiple Messages

        self._message_counter += len(recv_messages)

    @abstractmethod
    def _receive(self):
        raise NotImplementedError
