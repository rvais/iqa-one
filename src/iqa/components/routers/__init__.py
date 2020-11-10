import logging
from typing import TYPE_CHECKING

from iqa.abstract.server.router import Router
from iqa.system.executor.executor import ExecutorBase
from iqa.system.node.node import Node
from iqa.system.service.service import Service

if TYPE_CHECKING:
    from iqa.utils.types import RouterType


class RouterFactory(object):
    @staticmethod
    def create_router(
        implementation: str,
        node: Node,
        executor: ExecutorBase,
        service_impl: Service,
        **kwargs
    ) -> 'RouterType':

        for router in Router.__subclasses__():

            # Ignore router with different implementation
            if router.implementation != implementation:
                continue

            name: str = '%s-%s-%s' % ('router', router.__name__, node.hostname)
            return router(
                name=name, node=node, executor=executor, service=service_impl, **kwargs
            )

        exception: ValueError = ValueError(
            'Invalid router implementation: %s' % implementation
        )
        logging.getLogger(RouterFactory.__module__).error(exception)
        raise exception
