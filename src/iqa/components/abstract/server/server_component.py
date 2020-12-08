from abc import abstractmethod
from typing import TYPE_CHECKING

from iqa.components.abstract.component import Component

if TYPE_CHECKING:
    from typing import Optional, List
    from iqa.abstract.listener import Listener
    from iqa.system.node.base.node import Node
    from iqa.system.service.base.service import Service
    from iqa.components.abstract.management.client import ManagementClient
    from iqa.components.abstract.new_configuration import Configuration


class ServerComponent(Component):
    """
    Super class for all Server component implementations (for now Routers and Brokers).
    """

    def __init__(
        self,
        name: str,
        node: Node,
        service: Optional[Service] = None,
        listeners: Optional[List[Listener]] = None,
        configuration: Optional[Configuration] = None,
        **kwargs
    ) -> None:
        super(ServerComponent, self).__init__(name, node)
        self._service: Optional[Service] = service
        self.configuration: Optional[Configuration] = configuration
        self.listeners: List[Listener] = listeners if listeners is not None else []

    @abstractmethod
    def _get_management_client(self) -> ManagementClient:
        raise NotImplemented

    def get_management_client(self) -> ManagementClient:
        client = getattr(self, "_management_client", None)
        if client is None:
            return self._get_management_client()
        return client

    @property
    def management_client(self) -> ManagementClient:
        return self.get_management_client()

    @property
    def implementation(self):
        raise NotImplementedError

    @property
    def service(self) -> Optional[Service]:
        return self._service
