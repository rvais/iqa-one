import logging

from iqa.utils.walk_package import walk_package_and_import
from iqa.utils.utils import get_subclass_with_prop_value
from iqa.system.executor.executor_factory import ExecutorFactory
from iqa.system.node.base.node import Node
from iqa.system.node import __package__

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, List, Type
    from iqa.system.executor.base.executor import ExecutorBase


class NodeFactory(object):
    logger = logging.getLogger(__name__)
    __known_implementations: 'List[Type[Node]]' = walk_package_and_import(__package__, Node)

    @staticmethod
    def get_known_implementations() -> 'List[Type[Node]]':
        return NodeFactory.__known_implementations.copy()

    @staticmethod
    def create_node(
        hostname: str = 'localhost',
        ip: 'Optional[str]' = None,
        executor: 'Optional[ExecutorBase]' = None,
        **kwargs
    ) -> Node:
        """
        Creates a Node object based on provided arguments.
        :param hostname:
        :param executor:
        :param ip:
        :param kwargs:
        :return:
        """

        if executor is None:
            executor = ExecutorFactory.create_executor(implementation='local')

        executor_type: str = executor.implementation()

        try:
            node = get_subclass_with_prop_value(
                superclass=Node,
                in_class_property='implementation',
                cls_property_val=executor_type
            )

            NodeFactory.logger.info(
                'Creating %s [hostname=%s, host=%s]'
                % (node.__class__.__name__, hostname, ip)
            )
            return node(hostname=hostname, executor=executor, ip=ip, **kwargs)
        except ValueError:
            NodeFactory.logger.error(
                'Implementation of specific node with "%s" executor was not found!'
                % executor_type
            )
