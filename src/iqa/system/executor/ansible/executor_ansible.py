from typing import TYPE_CHECKING

from iqa.system.command.command_ansible import CommandBaseAnsible
from iqa.system.executor.base.executor import ExecutorBase
from iqa.system.executor.localhost.execution_local import ExecutionProcess

if TYPE_CHECKING:
    from os import PathLike
    from typing import Optional, Dict, Type, Union
    from iqa.system.command.command_base import CommandBase
"""
Executor implementation that uses the "ansible" CLI to
run the given Command instance on the target host.
"""


class ExecutorAnsible(ExecutorBase):
    """
    Executes the given command using Ansible.
    """

    def __init__(
        self,
        host: 'Optional[str]' = None,
        port: 'Optional[int]' = None,
        user: 'Optional[str]' = None,
        password: 'Optional[str]' = None,
        ssh_key_path: 'Optional[Union[str, bytes, PathLike]]' = None,
        ssh_key_passphrase: 'Optional[Union[str, bytes, PathLike]]' = None,
        known_hosts_path: 'Optional[Union[str, bytes, PathLike]]' = None,
        ansible_connection: str = 'ssh',
        ansible_inventory: 'Optional[str]' = None,
        ansible_module: str = 'raw',
        # docker_host: 'Optional[str]' = None,
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
        args: Dict = locals()
        del args["self"]
        del args["kwargs"]
        del args["__class__"]
        kwargs.update(args)
        super(ExecutorAnsible, self).__init__(**kwargs)

        missing = self._check_required_args(['host'], **kwargs)
        if missing:
            raise ValueError(f"One or more mandatory arguments are missing: [{ ', '.join(missing)}]")

        self._connection: str = ansible_connection
        self._inventory: 'Optional[str]' = ansible_inventory
        self._module: str = ansible_module
        # self._docker_host: 'Optional[str]' = docker_host

    @staticmethod
    def implementation() -> str:
        return 'ansible'

    @property
    def ansible_host(self) -> str:
        return self._host

    @property
    def ansible_user(self) -> str:
        return self._user

    def _execute(self, command: 'CommandBase') -> 'ExecutionProcess':
        command = CommandBaseAnsible.convert(command, ansible_module=self._module)

        ansible_args: list = []
        if self.ansible_user is not None:
            self._logger.debug('Ansible user: %s' % self._inventory)
            ansible_args += ['-u', self.ansible_user]

        if self._inventory is not None:
            self._logger.debug('Using inventory: %s' % self._inventory)
            ansible_args += ['-i', self._inventory]
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
    def get_preferred_command_base() -> 'Type[CommandBase]':
        return CommandBaseAnsible
