import asyncio
import logging
from asyncio.subprocess import Process
from typing import Optional

from iqa.system.command.command_base import CommandBase
from iqa.system.executor.execution import ExecutionBase

logger = logging.getLogger(__name__)


"""
Defines the representation of a command Execution that is generated
by the Executor implementations when a command is executed.
"""


class ExecutionAsyncio(ExecutionBase):
    """
    Represents the execution of a process that has been started by an Executor instance.
    It wraps the command that was triggered as well as the executor
    who generated the Execution instance.
    """

    def __init__(self, command: CommandBase, modified_args: list = None, env=None) -> None:
        """
        Instance is initialized with the command that was effectively
        executed and the Executor instance that produced this new object.
        :param command:
        :param modified_args:
        :param env:
        """
        super().__init__(command, modified_args, env)
        self._proc: Optional[Process] = None

    async def __aenter__(self):
        await self.run()

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def run(self):
        self._logger.debug('Executing: %s' % self.args)
        await self._run()

    async def _run(self) -> None:
        """
        Executes the command with different execution strategies (subprocess or others).
        :return:
        """

        _stdout = asyncio.subprocess.PIPE if self.command.stdout else None
        _stderr = asyncio.subprocess.PIPE if self.command.stderr else None

        self._proc = await asyncio.create_subprocess_shell(
            str(self.command),
            env=self.env,
            stdin=asyncio.subprocess.PIPE,
            stdout=_stdout,
            stderr=_stderr)

        self.stdout, self.stderr = await self._proc.communicate()

    async def wait(self) -> None:
        """
        Waits for command execution to complete.
        :return:
        """
        await self._proc.wait()

    @property
    def return_code(self):
        return self._proc.returncode

    def is_running(self) -> bool:
        """
        Returns True if execution is still running and False otherwise.
        :return:
        """
        return False if self.return_code else True

    def completed_successfully(self) -> bool:
        """
        Returns True if execution is done and no errors observed or False otherwise.
        :return:
        """
        return True if self.return_code == 0 else False

    def on_timeout(self) -> None:
        raise NotImplementedError

    def terminate(self) -> None:
        """
        Terminates the execution.
        :return:
        """
        self._proc.terminate()

    def _on_timeout(self) -> None:
        """
        This method is called internally by the TimeoutCallback in case
        the execution times out. It will notify concrete Execution and the
        Command instance that it has timed out.
        :return:
        """
        if self.is_running():
            self.timed_out = True
            self.on_timeout()
            self.command.on_timeout(self)

    def interrupt(self) -> None:
        """
        Interrupts a running process (if it is still running).
        Once interrupted, if a timer is active, it will be cancelled and
        the command instance will be notified of the interruption.
        :return:
        """
        if not self.is_running():
            return

        self._logger.debug('Interrupting execution')

        self.terminate()
        self.interrupted = True
        self.cancel_timer()
        self.command.on_interrupt(self)

    def cancel_timer(self) -> None:
        """
        Cancels the TimeoutCallback handler used internally.
        :return:
        """
        if self._timeout is not None:
            self._timeout.interrupt()
