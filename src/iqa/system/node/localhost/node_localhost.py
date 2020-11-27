"""
Basic concrete implementation of Node interface.
"""

import logging
import re
from typing import TYPE_CHECKING

from iqa.system.executor.executor_factory import ExecutorFactory
from iqa.system.node.base.node import Node

if TYPE_CHECKING:
    from typing import Optional, Union
    from iqa.system.command.command_base import CommandBase
    from iqa.system.executor.base.executor import ExecutorBase
    from iqa.system.executor.base.execution import ExecutionBase
    from iqa.system.executor.localhost.executor_local import ExecutorLocal
    from iqa.system.executor.asynclocalhost.executor import ExecutorAsyncio


class NodeLocal(Node):
    """Node component."""

    implementation: str = "local"

    def __init__(
        self,
        hostname: str,
        ip: Optional[str] = None,
        executor: Optional[Union[ExecutorBase, ExecutorLocal, ExecutorAsyncio]] = None,
        name: Optional[str] = "localhost"
    ) -> None:
        logging.getLogger().info('Initialization of NodeLocal: %s' % self.hostname)
        if executor is None:
            executor = ExecutorFactory.create_executor(self.implementation)
        super(NodeLocal, self).__init__(hostname, executor, ip=ip, name=name)

    def ping(self) -> bool:
        """Send ping to node"""
        cmd_ping: CommandBase = CommandBase([], stdout=True, timeout=20)

        # If unable to determine host address, then do not perform ping
        if self.get_ip() is None:
            return False
        cmd_ping.args = ['ping', '-c', '1', self.get_ip()]

        execution: ExecutionBase = await self.executor.execute(cmd_ping)

        # True if completed with exit code 0 and stdout has some data
        return execution.completed_successfully() and bool(execution.read_stdout())

    def get_ip(self):
        """Get host of node"""
        if self.ip is not None:
            return self.ip

        cmd_ip: CommandBase = CommandBase(['host', 'addr', 'list'], stdout=True, timeout=10)
        execution: ExecutionBase = self.execute(cmd_ip)

        # If execution failed, skip it
        if not execution.completed_successfully():
            return None

        # Parsing stdout and retrieving the IP
        ip_addr_out: Union[list, str] = execution.read_stdout()
        if not ip_addr_out:
            return None

        # Parse all returned host addresses
        ip_addresses: list = re.findall(
            r'([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', ip_addr_out, re.MULTILINE
        )
        try:
            ip_addresses.remove('127.0.0.1')
        except ValueError:
            return None

        # If only loop back defined, skip it
        if not ip_addresses:
            return None

        return ip_addresses[0]
