import abc
import logging
from typing import TYPE_CHECKING

from iqa.abstract.server.messaging_server import MessagingServer

if TYPE_CHECKING:
    from typing import Any, Optional, Union, List
    from os import PathLike
#    from iqa.abstract.destination.routing_type import RoutingType
    from iqa.components.abstract.component import Component
    from iqa.components.abstract.network.protocol.protocol import Protocol
    from iqa.abstract.destination.address import Address
    from iqa.abstract.destination.queue import Queue


class Broker(MessagingServer):
    """
    Abstract broker class
    """

    supported_protocols: List[Protocol] = []

    def __init__(
        self,
        broker_name: Optional[str] = None,
        broker_path: Optional[PathLike[Any]] = None,
        broker_web_port: Union[str, int] = 8161,
        broker_user: str = 'admin',
        broker_password: str = 'admin',
        **kwargs
    ) -> None:
        super(Broker, self).__init__(**kwargs)

        # Check and log missing arguments
        required_fields: dict = {
            'broker_name': broker_name,
            'broker_path': broker_path,
        }
        for field, value in required_fields:
            if value is None:
                logging.error('Missing requirement broker parameter: %s' % field)

        self.broker_name: Optional[str] = broker_name
        self.broker_path: Optional[PathLike[Any]] = broker_path
        self.web_port: Union[str, int] = broker_web_port
        self.user: str = broker_user
        self.password: str = broker_password
        self.cluster_member: Optional[Component] = None
        self.ha_member: Optional[Component] = None

    def set_as_cluster_member(self, cluster_component: Component):
        self.cluster_member = cluster_component

    def set_as_ha_member(self, ha_component: Component):
        self.ha_member = ha_component

    @abc.abstractmethod
    def queues(self, refresh: bool = True) -> List[Queue]:
        """
        Must return existing queues
        :return:
        """

    @abc.abstractmethod
    def addresses(self, refresh: bool = True) -> List[Address]:
        """
        Must return existing addresses
        :return:
        """
