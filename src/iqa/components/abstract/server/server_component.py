from typing import List, Optional

from iqa.abstract.listener import Listener
from iqa.components.abstract.component import Component
from iqa.components.abstract.configuration import Configuration
from iqa.components.abstract.management.client import ManagementClient
from iqa.system.node.node import Node
from iqa.system.service.service import Service


class ServerComponent(Component):
    """
    Super class for all Server component implementations (for now Routers and Brokers).
    """

    def __init__(
        self,
        name: str,
        node: Node,
        listeners: Optional[List[Listener]],
        configuration: Configuration = None,
        **kwargs
    ) -> None:
        super(ServerComponent, self).__init__(name, node)
        self.service: Service = kwargs.get('service')  # type: ignore
        self.name: str = name
        self.node: Node = node
        self.configuration: Optional[Configuration] = configuration
        self.listeners: Optional[List[Listener]] = listeners
        self.management_client: ManagementClient = self.get_management_client()

    def get_management_client(self) -> ManagementClient:
        raise NotImplementedError

    @property
    def implementation(self):
        raise NotImplementedError
