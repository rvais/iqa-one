import asyncio

from iqa.system.executor.asynclocalhost.execution import ExecutionAsyncio
from iqa.system.executor.base.executor import ExecutorBase
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from os import PathLike
    from typing import Optional, Dict, Union
    from iqa.system.command.command_base import CommandBase


class ExecutorAsyncio(ExecutorBase):
    """ Executor implementation for localhost AsyncIO executions
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
        super(ExecutorAsyncio, self).__init__(**kwargs)

    @staticmethod
    def implementation() -> str:
        return "async local"

    async def _execute(self, command: 'CommandBase') -> ExecutionAsyncio:
        execution = ExecutionAsyncio(command)
        await execution.run()
        return execution
