import os

from iqa.system.executor.base.executor import ExecutorBase
from iqa.system.executor.localhost.execution_local import ExecutionProcess
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from os import PathLike
    from typing import Optional, Dict, Union
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

    def __init__(
        self,
        host: 'Optional[str]' = None,
        port: 'Optional[int]' = None,
        user: 'Optional[str]' = None,
        password: 'Optional[str]' = None,
        ssh_key_path: 'Optional[Union[str, bytes, PathLike]]' = None,
        ssh_key_passphrase: 'Optional[Union[str, bytes, PathLike]]' = None,
        known_hosts_path: 'Optional[Union[str, bytes, PathLike]]' = None,
        **kwargs
    ) -> None:
        args: Dict = locals()
        del args["self"]
        del args["kwargs"]
        del args["__class__"]
        kwargs.update(args)
        super(ExecutorSshOld, self).__init__(**kwargs)

        missing = self._check_required_args(['host'], **kwargs)
        if missing:
            raise ValueError(f"One or more mandatory arguments are missing: [{ ', '.join(missing)}]")

    @staticmethod
    def implementation() -> str:
        return "ssh"

    def _execute(self, command: 'CommandBase') -> ExecutionProcess:
        ssh_args: list = ['ssh', '-p', '%s' % self._port]

        # If an SSL private key given, use it
        if self._ssh_key_path is not None and os.path.isfile(self._ssh_key_path):
            self._logger.debug('Using SSL Private Key - %s' % self._ssh_key_path)
            ssh_args += ['-i', self._ssh_key_path]

        # if not self.stricthostkeychecking:
        #     self._logger.debug('Using StrictHostKeyChecking no')
        #     ssh_args += ['-o', '"StrictHostKeyChecking no"']

        ssh_args += ['%s@%s' % (self._user, self._host)]

        return ExecutionProcess(command, executor=self, modified_args=ssh_args + command.args)
