import logging

from iqa.utils.walk_package import walk_package_and_import
from iqa.utils.utils import get_subclass_with_prop_value
# from iqa.system.executor.executor_factory import ExecutorFactory
from iqa.system.node.base.node import Node

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, List, Type


class NodeFactory(object):
    logger = logging.getLogger(__name__)
    __known_implementations: List[Type[Node]] = walk_package_and_import(__path__, Node)

    @staticmethod
    def get_known_implementations() -> List[Type[Node]]:
        return NodeFactory.__known_implementations.copy()

    @staticmethod
    def create_node(
        hostname: str = 'localhost',
        executor_type: str = 'local',
        ip: Optional[str] = None,
        **kwargs
    ) -> Node:
        """
        Creates a Node object based on provided arguments.
        :param hostname:
        :param executor_type:
        :param ip:
        :param kwargs:
        :return:
        """
        try:
            node = get_subclass_with_prop_value(
                superclass=Node,
                cls_property_val='implementation',
                in_class_property=executor_type
            )

            NodeFactory.logger.info(
                'Creating %s [hostname=%s, host=%s]'
                % (node.__class__.__name__, hostname, ip)
            )
            return node(hostname=hostname, ip=ip, **kwargs)
        except ValueError:
            NodeFactory.logger.error(
                'Implementation of specific node with "%s" executor was not found!'
                % executor_type
            )
