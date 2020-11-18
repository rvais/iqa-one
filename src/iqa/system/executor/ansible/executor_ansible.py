from typing import TYPE_CHECKING

from iqa.system.command.command_ansible import CommandBaseAnsible
from iqa.system.executor.base.executor import ExecutorBase
from iqa.system.executor.localhost.execution_local import ExecutionProcess

if TYPE_CHECKING:
    from typing import Optional
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
        module: str = 'raw',
        name: str = 'ExecutorAnsible',
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
        super(ExecutorAnsible, self).__init__()
        self.inventory: str = kwargs.get('inventory_file', inventory)
        self.ansible_host: str = kwargs.get(
            'ansible_host', ansible_host
        ) if not self.inventory else kwargs.get('inventory_hostname', ansible_host)
        self.ansible_user: str = kwargs.get('ansible_user', ansible_user)
        self.ansible_connection: str = kwargs.get('ansible_connection', 'ssh')
        self.module: str = kwargs.get('executor_module', module)
        self.name: str = kwargs.get('executor_name', name)
        self.docker_host: str = kwargs.get('executor_docker_host', None)

    def _execute(self, command: CommandBase) -> ExecutionProcess:

        ansible_args: list = ['ansible']

        if self.ansible_user is not None:
            ansible_args += ['-u', self.ansible_user]

        if self.inventory is not None:
            self._logger.debug('Using inventory: %s' % self.inventory)
            ansible_args += ['-i', self.inventory]
        else:
            self._logger.debug('Using inventory host: %s' % self.ansible_host)
            ansible_args += ['-i', '%s,' % self.ansible_host]

        # Executing using the "raw" module
        module: str = self.module

        # If given command is an instance of CommandAnsible
        # the module is read from it
        if isinstance(command, CommandBaseAnsible):
            self._logger.debug('Using Ansible module: %s' % command.ansible_module)
            module = command.ansible_module
        ansible_args += ['-m', module, '-a']

        # Appending command as a literal string
        ansible_args.append('%s' % ' '.join(command.args))

        # Host where command will be executed
        ansible_args.append(self.ansible_host)

        # Set new args
        return ExecutionProcess(command, executor=self, modified_args=ansible_args)
