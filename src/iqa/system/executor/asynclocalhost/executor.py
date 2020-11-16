from typing import Optional
import asyncio

from iqa.system.executor.localhost.execution import ExecutionAsyncio
from iqa.system.executor.executor import ExecutorBase
from iqa.system.command import CommandBase


class ExecutorAsyncio(ExecutorBase):
    """ Executor implementation for localhost AsyncIO executions
    """
    def __init__(self, user: str = 'root', password: str = None, **kwargs) -> None:

        super().__init__(**kwargs)
        self._user = user
        self._password = password

    async def _execute(self, command: CommandBase) -> ExecutionAsyncio:
        execution = ExecutionAsyncio(command)
        await execution.run()
        return execution
