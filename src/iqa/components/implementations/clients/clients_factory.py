import logging

from iqa.components.implementations.clients.external.client_external import ClientExternal
from iqa.utils.walk_package import walk_package_and_import
from iqa.components.implementations.component_factory import SpecificComponentFactory
from iqa.abstract.client.client import Client
from iqa.abstract.client.sender import Sender
from iqa.abstract.client.receiver import Receiver
from iqa.abstract.client.messaging_client import MessagingClient
from iqa.components.implementations.clients import __package__

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List, Type, Dict
    from iqa.components.abstract.component import Component
    from iqa.system.node.base.node import Node


class ClientFactory(SpecificComponentFactory):
    __client_implementations: 'List[Type[Client]]' = walk_package_and_import(__package__, Client)
    __type: 'Type[Component]' = Client
    __client_type_mapping: 'Dict[str, Type[MessagingClient]]' = {
        'sender': Sender,
        'receiver': Receiver,
        'connector': MessagingClient
    }

    @classmethod
    def get_type(cls) -> 'Type[Component]':
        return cls.__type

    @classmethod
    def get_available_implementations(cls) -> 'List[Type[Client]]':
        return cls.__client_implementations.copy()

    @staticmethod
    def create_component(implementation: str, node: 'Node', **kwargs) -> 'Client':
        # determine specific client type first
        client_type: Type[Client] = MessagingClient
        if 'type' in kwargs.keys() and kwargs['type'] in ClientFactory.__client_type_mapping.keys():
            client_type = ClientFactory.__client_type_mapping[kwargs['type']]
        elif 'type' in kwargs.keys():
            for cls in ClientFactory.get_available_implementations():
                if cls.__name__ == kwargs['type']:
                    client_type = cls
                    break

        for client in ClientFactory.get_available_implementations():
            # Ignore clients with different implementation
            if client.implementation != implementation or not issubclass(client, client_type):
                continue

            # Make sure component has a name
            name: str
            if 'name' not in kwargs.keys():
                name = f"{kwargs['type']}-{client.__name__}-{node.hostname}"
            else:
                name = kwargs['name']
                del kwargs['name']

            return client(name=name, node=node, **kwargs)

        err: str = f"Invalid client implementation '{implementation}' and/or client type '{client_type.__name__}'."
        raise ValueError(err)


class OldClientFactory(object):
    # Static element to store all available implementations
    _implementations: list = []

    @staticmethod
    def create_clients(
        implementation: str, node: Node,
        executor,  #: ExecutorBase,
        **kwargs
    ) -> list:
        for cl in ClientExternal.__subclasses__():

            # Ignore clients with different implementation
            if cl.implementation != implementation:
                continue

            # Now loop through concrete client types (sender, receiver, connector)
            clients: list = []
            if cl.__subclasses__():
                for client_impl in cl.__subclasses__():
                    name: str = '%s-%s-%s' % (
                        implementation,
                        client_impl.__name__.lower(),
                        node.hostname,
                    )
                    clients.append(
                        client_impl(name=name, node=node, executor=executor, **kwargs)
                    )
            else:
                name = '%s-%s-%s' % (implementation, cl.implementation, node.hostname)
                clients.append(cl(name=name, node=node, executor=executor, **kwargs))

            return clients

        exception: ValueError = ValueError(
            'Invalid client implementation: %s' % implementation
        )
        logging.getLogger(ClientFactory.__module__).error(exception)
        raise exception

    @staticmethod
    def get_available_implementations() -> list:

        # If implementations list has already been loaded, use it
        if ClientFactory._implementations:
            return ClientFactory._implementations

        result: list = []

        for cl in ClientExternal.__subclasses__():
            result.append(cl.implementation)

        ClientFactory._implementations = result

        return result
