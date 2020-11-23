import abc
import logging
from typing import TYPE_CHECKING

from iqa.abstract.server.messaging_server import MessagingServer

if TYPE_CHECKING:
    from typing import List
#    from iqa.abstract.destination.routing_type import RoutingType
    from iqa.abstract.destination.address import Address
    from iqa.abstract.destination.queue import Queue


class Broker(MessagingServer):
    """
    Abstract broker class
    """

    supported_protocols: list = []

    def __init__(self, **kwargs) -> None:
        super(Broker, self).__init__()

        # Log missing arguments
        required_fields: list = ['broker_name', 'broker_path']
        for field in required_fields:
            if field not in kwargs:
                logging.error('Missing requirement broker parameter: %s' % field)

        self.broker_name: str = kwargs.get('broker_name', None)
        self.broker_path: str = kwargs.get('broker_path', None)
        self.web_port: str = kwargs.get('broker_web_port', 8161)
        self.user: str = kwargs.get('broker_user', 'admin')
        self.password: str = kwargs.get('broker_password', 'admin')
        self.cluster_member = None
        self.ha_member = None

    def set_cluster_member(self, cluster_component):
        self.cluster_member = cluster_component

    def set_ha_member(self, ha_component):
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
