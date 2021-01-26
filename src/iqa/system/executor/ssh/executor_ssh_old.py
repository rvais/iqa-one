import os

from iqa.system.executor.base.executor import ExecutorBase
from iqa.system.executor.localhost.execution_local import ExecutionProcess
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional
    from iqa.system.command.command_base import CommandBase

"""
Runs a command using SSH CLI.
"""


class ExecutorSshOld(ExecutorBase):
    """
    Executor that runs Command instances via SSH CLI, based on provided
    configuration (user, hostname and port).
    The SSL KEY for the given user on the remote host must be authorized,
    otherwise it may run indefinitely or timeout.
    """

    implementation = 'ssh'
    name: str = 'Executor class for SSH remote execution'

    def __init__(
        self,
        hostname: str,
        port: str = '22',
        user: str = 'root',
        ssl_private_key: 'Optional[str]' = None,
        name: str = 'ExecutorSsh',
        **kwargs
    ) -> None:
        super(ExecutorSshOld, self).__init__()
        self.hostname: str = kwargs.get('executor_hostname', hostname)
        self.port: str = kwargs.get('executor_port', port)
        self.user: str = kwargs.get('executor_user', user)
        self.name: str = kwargs.get('executor_name', name)
        self.ssl_private_key: Optional[str] = kwargs.get(
            'executor_ssl_private_key', ssl_private_key
        )

    def _execute(self, command: 'CommandBase') -> ExecutionProcess:
        ssh_args: list = ['ssh', '-p', '%s' % self.port]

        # If an SSL private key given, use it
        if self.ssl_private_key is not None and os.path.isfile(self.ssl_private_key):
            self._logger.debug('Using SSL Private Key - %s' % self.ssl_private_key)
            ssh_args += ['-i', self.ssl_private_key]

        # if not self.stricthostkeychecking:
        #     self._logger.debug('Using StrictHostKeyChecking no')
        #     ssh_args += ['-o', '"StrictHostKeyChecking no"']

        ssh_args += ['%s@%s' % (self.user, self.hostname)]

        return ExecutionProcess(command, executor=self, modified_args=ssh_args + command.args)
