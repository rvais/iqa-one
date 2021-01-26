import asyncio

from iqa.system.executor.asynclocalhost.execution import ExecutionAsyncio
from iqa.system.executor.base.executor import ExecutorBase
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional
    from iqa.system.command.command_base import CommandBase


class ExecutorAsyncio(ExecutorBase):
    """ Executor implementation for localhost AsyncIO executions
    """

    def __init__(self, user: str = 'root', password: 'Optional[str]' = None, **kwargs) -> None:

        super(ExecutorAsyncio).__init__(**kwargs)
        self._user = user
        self._password = password

    @staticmethod
    def implementation() -> str:
        return "async local"

    @property
    def name(self) -> str:
        return 'Executor class for asynchronous localhost execution'

    async def _execute(self, command: 'CommandBase') -> ExecutionAsyncio:
        execution = ExecutionAsyncio(command)
        await execution.run()
        return execution
