import logging
from typing import List

from iqa.abstract.destination.address import Address
from iqa.abstract.destination.queue import Queue
from iqa.abstract.destination.routing_type import RoutingType
from iqa.abstract.listener import Listener
from iqa.abstract.server.broker import Broker
from iqa.components.abstract.server.server_component import ServerComponent
from iqa.components.brokers.artemis.artemis_config import ArtemisConfig
from iqa.components.brokers.artemis.management.jolokia_client import ArtemisJolokiaClient


class Activemq(ServerComponent, Broker):
    """
    Apache ActiveMQ has a proven non blocking architecture. It delivers outstanding performance.
    """

    supported_protocols: list = ["AMQP10", "MQTT", "STOMP", "Openwire"]
    name: str = 'Activemq'
    implementation: str = 'activemq'

    def __init__(self, name: str, **kwargs) -> None:
        super(Activemq, self).__init__(**kwargs)
        self._queues: List[Queue] = list()
        self._addresses: List[Address] = list()
        self._addresses_dict: dict = {}
        self.config: ArtemisConfig = ArtemisConfig(**kwargs)

        self.management_client: ArtemisJolokiaClient = ArtemisJolokiaClient()  # type: ignore
        self.users: dict = self.config.users

    def queues(self, refresh: bool = True) -> List[Queue]:
        """
        Retrieves and lists all queues
        :param refresh:
        :return:
        """
        if self._queues and not refresh:
            return self._queues

        self._refresh_addresses_and_queues()
        return self._queues

    def addresses(self, refresh: bool = True) -> List[Address]:
        """
        Retrieves and lists all addresses
        :param refresh:
        :return:
        """
        if self._addresses and not refresh:
            return self._addresses

        self._refresh_addresses_and_queues()
        return self._addresses

    def create_queue(self, queue: Queue, address: Address, durable: bool = True):
        """
        Creates a given queue based on provided arguments
        :param queue:
        :param address:
        :param durable:
        :return:
        """
        if queue.routing_type == RoutingType.BOTH:
            raise ValueError('Queues can only use ANYCAST or MULTICAST routing type')
        return self.management_client.create_queue(
            address.name, queue.name, durable, queue.routing_type.name
        )

    def delete_queue(self, name: str, remove_consumers: bool = False):
        """
        Deletes a queue
        :param name:
        :param remove_consumers:
        :return:
        """
        return self.management_client.delete_queue(name, remove_consumers)

    def _refresh_addresses_and_queues(self) -> None:
        """
        Need to combine both calls, in order to map queues to addresses
        and vice-versa.
        :return:
        """
        # Retrieving queues
        queues: list = list()
        addresses: list = list()

        # Save client queues and addresses
        queues_result = self.management_client.list_queues()
        addresses_result = self.management_client.list_addresses()

        # In case of errors, return empty list
        if not queues_result.success:
            logging.getLogger().warning('Unable to retrieve queues')
            return

        # In case of errors, return empty list
        if not addresses_result.success:
            logging.getLogger().warning('Unable to retrieve addresses')
            return

        # Dictionary containing retrieved addresses
        addresses_dict: dict = {}

        # If no address found, skip it
        if not addresses_result.data:
            logging.debug('No addresses available')
        else:
            # Parsing returned addresses
            for addr_info in addresses_result.data:
                logging.debug(
                    "Address found: %s - routingType: %s"
                    % (addr_info['name'], addr_info['routingTypes'])
                )
                address: Address = Address(
                    name=addr_info['name'],
                    routing_type=RoutingType.from_value(addr_info['routingTypes']),
                )
                addresses_dict[address.name] = address
                addresses.append(address)

        # If no queues returned
        if not queues_result.data:
            logging.debug('No queues available')
        else:
            # Parsing returned queues
            for queue_info in queues_result.data:
                logging.debug(
                    "Queue found: %s - routingType: %s"
                    % (queue_info['name'], queue_info['routingType'])
                )
                routing_type: RoutingType = RoutingType.from_value(
                    queue_info['routingType']
                )
                address = addresses_dict[queue_info['address']]
                queue: Queue = Queue(
                    name=queue_info['name'], routing_type=routing_type, address=address
                )
                queue.message_count = queue_info['messageCount']
                address.queues.append(queue)
                queues.append(queue)

        # Updating broker data
        self._addresses_dict = addresses_dict
        self._addresses = addresses
        self._queues = queues

    def get_management_client(self) -> ArtemisJolokiaClient:  # type: ignore
        """
        Creates a new instance of the Jolokia Client.
        :return:
        """
        client: ArtemisJolokiaClient = ArtemisJolokiaClient(
            self.config.instance_name,  # type: ignore
            self.node.ip,
            self.config.ports['web'],
            'admin',
            self.config.get_user_password('admin'),
        )
        return client

    @staticmethod
    def _get_routing_type(routing_type: RoutingType) -> str:
        """
        Returns the routing type str value, based on expected values on the broker.
        :param routing_type:
        :return:
        """
        if routing_type == RoutingType.BOTH:
            return 'ANYCAST, MULTICAST'
        return routing_type.name

    def get_url(self, port: int = None, listener: Listener = None) -> str:
        pass

    def get_urls(self, schema: str) -> List[Listener]:
        pass
