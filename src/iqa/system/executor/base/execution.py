"""
Defines the representation of a command Execution that is generated
by the Executor implementations when a command is executed.
"""
import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import iqa.logger
from iqa.utils.timeout import TimeoutCallback

if TYPE_CHECKING:
    from typing import Optional, List
    from iqa.system.command.command_base import CommandBase

logger = iqa.logger.logger


class ExecutionException(Exception):
    """
    Exception thrown if a given Execution instance could be created
    """


class ExecutionBase(ABC):
    """
    Represents the execution of a process that has been started by an Executor instance.
    It wraps the command that was triggered as well as the executor
    who generated the Execution instance.
    """

    def __init__(
            self,
            command: CommandBase,
            modified_args: Optional[List[str]] = None,
            env: Optional[dict] = None
    ) -> None:
        """
        Instance is initialized with command that was effectively
        executed and the Executor instance that produced this new object.
        :param command:
        :param modified_args:
        :param env:
        """
        self.command: CommandBase = command
        self.stdout = None
        self.stderr = None

        if env is None:
            env = {}
        self.env: dict = env

        # Flags to control whether execution has timed out or it has been interrupted by user
        self.timed_out: bool = False
        self.interrupted: bool = False
        self.failure: bool = False

        # Adjust time out settings if provided
        self._timeout: Optional[TimeoutCallback] = None
        if command.timeout and command.timeout > 0:
            self._timeout = TimeoutCallback(command.timeout, self._on_timeout)

        # Avoid unwanted modification of the command's arguments by executors
        self.args: List[str] = self.command.args
        if modified_args:
            self.args = modified_args

        self._logger: logging.Logger = logger

        self._logger.debug('Executing: %s' % self.args)

    @abstractmethod
    async def _run(self) -> None:
        """
        Executes the command with different execution strategies (subprocess or others).
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def wait(self) -> None:
        """
        Waits for command execution to complete.
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def is_running(self) -> bool:
        """
        Returns True if execution is still running and False otherwise.
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def completed_successfully(self) -> bool:
        """
        Returns True if execution is done and no errors observed or False otherwise.
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def on_timeout(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def terminate(self) -> None:
        """
        Terminates the execution.
        :return:
        """
        raise NotImplementedError

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
