import abc

from iqa.components.abstract.management.client import ManagementClient
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from iqa.abstract.destination.address import Address
    from iqa.abstract.destination.destination import Destination
    from iqa.abstract.destination.queue import Queue


class ManagementBroker(ManagementClient):
    def __init__(self) -> None:
        super(ManagementBroker, self).__init__()

    def create_destination(self, destination: 'Destination') -> 'Destination':  # Address
        pass

    def delete_destination(
        self, name: str, remove_consumers: bool = False
    ) -> None:  # Address
        pass

    @abc.abstractmethod
    def create_address(self, address: 'Address') -> 'Address':
        """
        Creates an address using its name and specialized type (ANYCAST, MULTICAST).
        :param address:
        :return:
        """

    @abc.abstractmethod
    def create_queue(
        self, queue: 'Queue', address: 'Address', durable: bool = True
    ) -> 'Queue':
        """
        Creates a queue using its name and specialized type, nested to the given address.
        :param queue:
        :param address:
        :param durable:
        :return:
        """

    @abc.abstractmethod
    def delete_address(self, name: str, force: bool = False) -> None:
        """
        Deletes a given address.
        :param name:
        :param force:
        :return:
        """

    @abc.abstractmethod
    def delete_queue(self, name: str, remove_consumers: bool = False) -> None:
        """
        Deletes a given queue.
        :param name:
        :param remove_consumers:
        :return:
        """
