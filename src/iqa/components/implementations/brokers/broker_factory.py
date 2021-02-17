from iqa.utils.walk_package import walk_package_and_import
from iqa.components.implementations.component_factory import SpecificComponentFactory
from iqa.abstract.server.broker import Broker
from iqa.components.implementations.brokers import __package__

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List, Type
    from iqa.components.abstract.component import Component
    from iqa.system.node.base.node import Node


class BrokerFactory(SpecificComponentFactory):
    __broker_implementations: 'List[Type[Broker]]' = walk_package_and_import(__package__, Broker)
    __type: 'Type[Component]' = Broker

    @classmethod
    def get_type(cls) -> 'Type[Component]':
        return cls.__type

    @classmethod
    def get_available_implementations(cls) -> 'List[Type[Broker]]':
        return BrokerFactory.__broker_implementations.copy()

    @staticmethod
    def create_component(implementation: str, node: 'Node', **kwargs) -> 'Broker':
        for broker in BrokerFactory.get_available_implementations():
            # Ignore broker with different implementation
            if broker.implementation != implementation:
                continue

            # Make sure component has a name
            name: str
            if 'name' not in kwargs.keys():
                name: str = f"Broker-{broker.__name__}-{node.hostname}"
            else:
                name = kwargs['name']
                del kwargs['name']

            return broker(name=name, node=node, **kwargs)

        raise ValueError(f"Invalid broker implementation: {implementation}")
