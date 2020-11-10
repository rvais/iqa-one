import logging

from iqa.components.clients.external.client_external import ClientExternal
from iqa.system.executor.executor import ExecutorBase
from iqa.system.node.node import Node


class ClientFactory(object):
    # Static element to store all available implementations
    _implementations: list = []

    @staticmethod
    def create_clients(
        implementation: str, node: Node, executor: ExecutorBase, **kwargs
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
