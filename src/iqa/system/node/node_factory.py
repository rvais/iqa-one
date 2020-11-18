import logging
from typing import TYPE_CHECKING

from iqa.system.executor.ansible.executor_ansible import ExecutorAnsible
from iqa.system.executor.docker.executor_docker import ExecutorDocker
from iqa.system.node.node_ansible import NodeAnsible
from iqa.system.node.node_docker import NodeDocker
from iqa.system.node.node_localhost import NodeLocal

if TYPE_CHECKING:
    from iqa.utils.types import ExecutorType, NodeType


class NodeFactory(object):
    logger: logging.Logger = logging.getLogger(__name__)

    @staticmethod
    def create_node(
        hostname: str, executor: 'ExecutorType', ip: str = None, **kwargs
    ) -> 'NodeType':
        """
        Creates a Node object based on provided arguments.
        :param hostname:
        :param executor:
        :param ip:
        :param kwargs:
        :return:
        """
        new_node: 'NodeType'
        if isinstance(executor, ExecutorAnsible):
            new_node = NodeAnsible(hostname, executor, ip)
        elif isinstance(executor, ExecutorDocker):
            new_node = NodeDocker(hostname, executor, ip)
        else:
            new_node = NodeLocal(hostname, executor, ip)

        NodeFactory.logger.info(
            'Creating %s [hostname=%s, host=%s]'
            % (new_node.__class__.__name__, hostname, ip)
        )
        return new_node
