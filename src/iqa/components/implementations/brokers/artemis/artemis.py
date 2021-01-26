import logging
from typing import TYPE_CHECKING

from iqa.abstract.destination.address import Address
from iqa.abstract.destination.queue import Queue
from iqa.abstract.destination.routing_type import RoutingType
from iqa.abstract.server.broker import Broker
from iqa.components.abstract.network.protocol.protocol import Protocol
from iqa.components.abstract.server.server_component import ServerComponent
from iqa.components.implementations.brokers.artemis.new_artemis_config import ArtemisConfig
from iqa.components.implementations.brokers.artemis.management.jolokia_client import ArtemisJolokiaClient

if TYPE_CHECKING:
    from os import PathLike
    from typing import Optional, Any, List, Union
    from iqa.abstract.listener import Listener
    from iqa.system.node.base.node import Node
    from iqa.system.service.base.service import Service
    from iqa.components.abstract.configuration import Configuration


class Artemis(ServerComponent, Broker):
    """
    Apache ActiveMQ Artemis has a proven non blocking architecture. It delivers outstanding performance.
    """

    supported_protocols: 'List[Protocol]' = [
        Protocol.CORE, Protocol.AMQP10, Protocol.MQTT, Protocol.STOMP, Protocol.Openwire
    ]

    name: str = 'Artemis'
    implementation: str = 'artemis'

    # parameters here are purely for typing purposes, autocompletion and to know method signature without need to look
    # at signature of parent classes
    def __init__(
        self,
        node: 'Node',
        name: 'Optional[str]' = None,
        service: 'Optional[Service]' = None,
        listeners: 'Optional[List[Listener]]' = None,
        configuration: 'Optional[Configuration]' = None,
        broker_name: 'Optional[str]' = None,
        broker_path: 'Optional[PathLike[Any]]' = None,
        broker_web_port: 'Union[str, int]' = 8161,
        broker_user: str = 'admin',
        broker_password: str = 'admin',
        **kwargs
    ) -> None:
        # dump arguments into dictionary
        inputs = locals()
        # remove self and kwargs variables as they would mess things up
        del inputs['self']
        del inputs['kwargs']
        # update kwargs to pass in super().__init__()
        if name is None:
            inputs['name'] = self.name
        kwargs.update(inputs)

        super(Artemis, self).__init__(**kwargs)

        self._queues: List[Queue] = list()
        self._addresses: List[Address] = list()
        self._addresses_dict: dict = {}
        self.configuration: ArtemisConfig = ArtemisConfig(self, **kwargs)
        self.configuration.create_configuration(
            kwargs.get('inventory_file', 'inventory.yml')
        )

        self._management_client: ArtemisJolokiaClient = self._get_management_client()

    @property
    def management_client(self) -> ArtemisJolokiaClient:
        if self._management_client is None:
            self._get_management_client()
        return self._management_client

    def queues(self, refresh: bool = True) -> list:
        """
        Retrieves and lists all queues
        :param refresh:
        :return:
        """
        if self._queues and not refresh:
            return self._queues

        self._refresh_addresses_and_queues()
        return self._queues

    def addresses(self, refresh: bool = True) -> list:
        """
        Retrieves and lists all addresses
        :param refresh:
        :return:
        """
        if self._addresses and not refresh:
            return self._addresses

        self._refresh_addresses_and_queues()
        return self._addresses

    def create_address(self, address: Address):
        """
        Creates the given address
        :param address:
        :return:
        """
        routing_type = self._get_routing_type(address.routing_type)
        return self.management_client.create_address(address.name, routing_type)

    def create_queue(self, queue: 'Queue', address: 'Address', durable: bool = True):
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

    def delete_address(self, name: str, force: bool = False):
        """
        Deletes an address
        :param name:
        :param force:
        :return:
        """
        return self.management_client.delete_address(name, force)

    def delete_queue(self, name: str, remove_consumers: bool = False):
        """
        Deletes a queue
        :param name:
        :param remove_consumers:
        :return:
        """
        return self.management_client.delete_queue(name, remove_consumers)

    def _refresh_addresses_and_queues(self):
        """
        Need to combine both calls, in order to map queues to addresses
        and vice-versa.
        :return:
        """
        # Retrieving queues
        queues: list = list()
        addresses: list = list()

        # Get a new client instance
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
        addresses_dict = {}

        # If no address found, skip it
        if not addresses_result.data:
            logging.debug('No addresses available')
        else:
            # Parsing returned addresses
            for addr_info in addresses_result.data:
                logging.debug(
                    'Address found: %s - routingType: %s'
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
                    'Queue found: %s - routingType: %s'
                    % (queue_info['name'], queue_info['routingType'])
                )
                routing_type: RoutingType = RoutingType.from_value(
                    queue_info['routingType']
                )
                address: Address = addresses_dict[queue_info['address']]
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

    def _get_management_client(self) -> ArtemisJolokiaClient:  # type: ignore
        """
        Creates a new instance of the Jolokia Client.
        :return:
        """
        client = ArtemisJolokiaClient(
            self.configuration.instance_name,  # type: ignore
            self.node.ip,
            self.configuration.ports['web'],
            'admin',
            self.configuration.get_user_password('admin'),
        )
        return client

    @staticmethod
    def _get_routing_type(routing_type: 'RoutingType') -> str:
        """
        Returns the routing type str value, based on expected values on the broker.
        :param routing_type:
        :return:
        """
        if routing_type == RoutingType.BOTH:
            return 'ANYCAST, MULTICAST'
        return routing_type.name

    def get_url(self, port: int = None, listener: 'Listener' = None) -> str:
        pass
