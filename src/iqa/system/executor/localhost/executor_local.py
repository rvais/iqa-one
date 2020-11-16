from iqa.system.command import CommandBase
from iqa.system.executor import ExecutorBase, ExecutionBase

"""
Runs a local command using SSH CLI.
"""


class ExecutorLocal(ExecutorBase):
    """
    Executes a given command locally.
    """

    implementation = 'local'

    def __init__(self, name: str = 'ExecutorLocal', **kwargs) -> None:
        super(ExecutorLocal, self).__init__(**kwargs)
        self.name: str = name

    async def _execute(self, command: CommandBase) -> ExecutionBase:
        ex = ExecutionBase(command)
        return ex
