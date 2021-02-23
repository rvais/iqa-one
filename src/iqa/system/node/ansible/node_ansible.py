"""
Ansible Node implementation of Node Interface.
"""

import logging
import re

from iqa.system.command.command_ansible import CommandBaseAnsible
from iqa.system.node.base.node import Node
from iqa.system.executor.executor_factory import ExecutorFactory

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Dict, Union
    from iqa.system.executor.ansible.executor_ansible import ExecutorAnsible
    from iqa.system.executor.base.execution import ExecutionBase


class NodeAnsible(Node):
    """Ansible implementation for Node interface."""

    implementation: str = "ansible"

    def __init__(
        self,
        hostname: str,
        ip: 'Optional[str]' = None,
        executor: 'Optional[ExecutorAnsible]' = None,
        name: 'Optional[str]' = None,
        **kwargs
    ) -> None:
        if executor is None:
            executor = ExecutorFactory.create_executor(self.implementation)

        args: Dict = locals()
        del args["self"]
        del args["kwargs"]
        del args["__class__"]
        kwargs.update(args)

        super(NodeAnsible, self).__init__(**kwargs)

    def ping(self) -> bool:
        """Send ping to Ansible node"""
        cmd_ping: CommandBaseAnsible = CommandBaseAnsible(
            ansible_module='ping', stdout=True, timeout=20
        )
        execution: ExecutionBase = self.executor.execute(cmd_ping)

        # True if completed with exit code 0 and stdout has some data
        return execution.completed_successfully() and bool(execution.read_stdout())

    def get_ip(self):
        """Get host of Ansible node"""
        if self.ip:
            return self.ip

        cmd_ping: CommandBaseAnsible = CommandBaseAnsible(
            ansible_module='setup',
            ansible_args=['filter=ansible_default_ipv4'],
            stdout=True,
            stderr=True,
            timeout=20,
        )
        execution: ExecutionBase = self.executor.execute(cmd_ping)
        execution.wait()

        if not execution.completed_successfully() or not execution.read_stdout():
            return None

        ip_addr_out: Union[list, str] = execution.read_stdout()
        ip_addresses: list = re.findall(
            r'([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', ip_addr_out, re.MULTILINE
        )

        # If only loop back defined, skip it
        if not ip_addresses:
            return None

        return ip_addresses[0]
