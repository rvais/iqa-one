from iqa.system.executor.base.executor import ExecutorBase
from iqa.system.executor.base.execution import ExecutionBase
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from iqa.system.command.command_base import CommandBase


"""
Runs a local command using SSH CLI.
"""


class ExecutorLocal(ExecutorBase):
    """
    Executes a given command locally.
    """

    implementation: str = "local"
    name: str = 'Executor class for localhost execution'

    def __init__(self, name: str = 'ExecutorLocal', **kwargs) -> None:
        super(ExecutorLocal, self).__init__(**kwargs)
        self.name: str = name

    async def _execute(self, command: CommandBase) -> ExecutionBase:
        ex = ExecutionBase(command)
        return ex
