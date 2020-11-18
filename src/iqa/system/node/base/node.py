"""
Interface for Node element. A node holds a running messaging component and it
must provide some basic behaviors, like ping, get_ip and execute command.
"""
import abc
import logging
from typing import TYPE_CHECKING

from iqa.utils.ping import ping

if TYPE_CHECKING:
    from typing import Optional
    from iqa.system.command.command_base import CommandBase
    from iqa.system.executor.base.execution import ExecutionBase
    from iqa.system.executor.base.executor import ExecutorBase


class Node(abc.ABC):
    """Node abstract component"""

    implementation = NotImplemented

    def __init__(
        self,
        hostname: str,
        executor: ExecutorBase,
        ip: Optional[str] = None,
        name: Optional[str] = None
    ) -> None:
        logging.getLogger().info('Initialization of Node: %s' % hostname)
        self.hostname: str = hostname
        self.name: str = name if name else hostname
        self.executor: ExecutorBase = executor
        self.ip: Optional[str] = ip
        self.reachable: bool = False

        self._is_reachable()

    def execute(self, command: CommandBase) -> ExecutionBase:
        """Execute command using Node's executor"""
        return await self.executor.execute(command)

    @abc.abstractmethod
    def ping(self) -> bool:
        raise NotImplemented

    @abc.abstractmethod
    def get_ip(self) -> str:
        raise NotImplemented

    def _is_reachable(self) -> bool:
        """ Is node reachable?

        Try to ping node from the host where IQA running if is reachable.
        """
        if self.ip:
            reachable: bool = ping(host=self.ip)

            if reachable:
                logging.getLogger().info('Node %s is reachable.' % self.hostname)
                self.reachable = True
            else:
                logging.getLogger().warning('Node %s is not reachable from IQA!' % self.hostname)
                self.reachable = False

            return reachable
        else:
            logging.getLogger().warning('Node %s does not have an IP address!' % self.hostname)
            self.reachable = False
            return False
