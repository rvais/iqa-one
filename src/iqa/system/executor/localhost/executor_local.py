from iqa.system.executor.base.executor import ExecutorBase
from iqa.system.executor.localhost.execution_local import ExecutionProcess
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from os import PathLike
    from typing import Optional, Dict, Union
    from iqa.system.command.command_base import CommandBase
    from iqa.system.executor.base.execution import ExecutionBase


"""
Runs a local command using SSH CLI.
"""


class ExecutorLocal(ExecutorBase):
    """
    Executes a given command locally.
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
        super(ExecutorLocal, self).__init__(**kwargs)

    @staticmethod
    def implementation() -> str:
        return "local"

    def _execute(self, command: 'CommandBase') -> 'ExecutionBase':
        ex = ExecutionProcess(command)
        return ex
