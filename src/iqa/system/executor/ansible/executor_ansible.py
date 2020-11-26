from typing import TYPE_CHECKING

from iqa.system.command.command_ansible import CommandBaseAnsible
from iqa.system.executor.base.executor import ExecutorBase
from iqa.system.executor.localhost.execution_local import ExecutionProcess

if TYPE_CHECKING:
    from typing import Optional, Type
    from iqa.system.command.command_base import CommandBase
"""
Executor implementation that uses the "ansible" CLI to
run the given Command instance on the target host.
"""


class ExecutorAnsible(ExecutorBase):
    """
    Executes the given command using Ansible.
    """

    implementation = 'ansible'
    name: str = 'Ansible executor class'

    def __init__(
        self,
        ansible_host: Optional[str] = None,
        inventory: Optional[str] = None,
        ansible_user: Optional[str] = None,
        ansible_connection: str = 'ssh',
        module: str = 'raw',
        executor_name: str = 'ExecutorAnsible',
        docker_host: Optional[str] = None,
        **kwargs
    ) -> None:
        """
        Initializes the ExecutorAnsible instance based on provided arguments.
        When an inventory is provided, the 'ansible_host' can be an host address or any
        ansible name (machine or group) within the inventory. If an inventory is not
        provided, then 'ansible_host' must be a valid IP Address or Hostname.
        :param ansible_host:
        :param inventory:
        :param ansible_user:
        :param module:
        :param name:
        :param kwargs:
        """
        super(ExecutorAnsible, self).__init__(**kwargs)
        self.ansible_host: Optional[str] = ansible_host
        self.inventory: Optional[str] = inventory
        self.ansible_user: str = ansible_user
        self.ansible_connection: str = ansible_connection
        self.module: str = module
        self.name: str = executor_name
        self.docker_host: str = docker_host

    def _execute(self, command: CommandBase) -> ExecutionProcess:
        command = CommandBaseAnsible.convert(command, ansible_module=self.module)

        ansible_args: list = []
        if self.ansible_user is not None:
            self._logger.debug('Ansible user: %s' % self.inventory)
            ansible_args += ['-u', self.ansible_user]

        if self.inventory is not None:
            self._logger.debug('Using inventory: %s' % self.inventory)
            ansible_args += ['-i', self.inventory]
        else:
            self._logger.debug('Using inventory host: %s' % self.ansible_host)
            ansible_args += ['-i', '%s,' % self.ansible_host]

        self._logger.debug('Using Ansible module: %s' % command.ansible_module)
        ansible_args += ['-m', command.ansible_module, '-a']
        ansible_args.extend(command.ansible_args)

        # Appending command as a literal string
        ansible_args.append('%s' % ' '.join(command.args))

        # Host where command will be executed
        ansible_args.append(self.ansible_host)

        # Set new args
        return ExecutionProcess(command, executor=self, modified_args=ansible_args)

    @staticmethod
    def get_preferred_command_base() -> Type[CommandBase]:
        return CommandBaseAnsible
