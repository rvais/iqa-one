import abc

from iqa.components.abstract.configuration import Configuration
from iqa.components.abstract.server.server_component import ServerComponent


class BrokerConfiguration(Configuration):
    users: dict = {}
    ports: dict = {}

    def __init__(self, component: ServerComponent, **kwargs) -> None:
        super(BrokerConfiguration, self).__init__(component, **kwargs)

    @abc.abstractmethod
    def assign_ports(self):
        pass

    @abc.abstractmethod
    def create_default_configuration(self, **kwargs):
        pass

    @abc.abstractmethod
    def get_users(self):
        pass

    @abc.abstractmethod
    def get_acceptors(self):
        pass

    get_listeners = get_acceptors

    @abc.abstractmethod
    def apply_config(self, yaml_configuration: str) -> None:
        pass
