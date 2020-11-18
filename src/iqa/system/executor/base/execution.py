"""
Defines the representation of a command Execution that is generated
by the Executor implementations when a command is executed.
"""
import logging
import subprocess
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import iqa.logger
from iqa.utils.timeout import TimeoutCallback

if TYPE_CHECKING:
    from typing import Optional, Union, List, IO
    from iqa.system.command.command_base import CommandBase
    from iqa.system.executor.base.executor import ExecutorBase

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
            executor: Optional[ExecutorBase] = None,
            modified_args: Optional[List[str]] = None,
            env: Optional[dict] = None
    ) -> None:
        """
        Instance is initialized with command that was effectively
        executed and the Executor instance that produced this new object.
        :param command:
        :param executor:
        :param modified_args:
        :param env:
        """
        self.command: CommandBase = command
        self.executor: Optional[ExecutorBase] = executor

        # Prepare stdout and stderr default file descriptors
        self._fd_stdout: int = subprocess.DEVNULL
        self._fd_stderr: int = subprocess.DEVNULL

        # Prepare file handles and update file descriptors if applicable
        self._stdout: Optional[IO] = None
        self._stderr: Optional[IO] = None

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

    @property
    def fd_stdout(self) -> int:
        return self._fd_stdout

    @property
    def fd_stderr(self) -> int:
        return self._fd_stderr

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

    # TODO(rvais): reimplement read operations using yield if appropriate
    def read_stdout(self, lines: bool = False, closefd: bool = True) -> Optional[Union[str, List[str]]]:
        """
        Returns a string with the whole STDOUT content if the original
        command has stdout property defined as True. Otherwise
        None will be returned.
        :param lines: whether to return stdout as a list of lines
        :type lines: bool
        :param closefd: closefd parameter to pass to underlying open()
        :type closefd: bool
        :return: Stdout content as str if lines is False, or as a list
        """
        if self._stdout is None and self.fd_stdout != subprocess.DEVNULL:
            return None

        if self._stdout is None:
            self._stdout = open(self.fd_stdout, "r", encoding=self.command.encoding, closefd=closefd)

        self._stdout.seek(0)

        if lines:
            return self._stdout.readlines()

        return self._stdout.read()

    def read_stderr(self, lines: bool = False, closefd: bool = True) -> Optional[Union[str, List[str]]]:
        """
        Returns a string with the whole STDERR content if the original
        command has stderr property defined as True. Otherwise
        None will be returned.
        :param lines: whether to return stdout as a list of lines
        :type lines: bool
        :param closefd: closefd parameter to pass to underlying open()
        :type closefd: bool
        :return: Stdout content as str if lines is False, or as a list
        """
        if self._stderr is None and self._fd_stderr != subprocess.DEVNULL:
            return None

        if self._stderr is None:
            self._stderr = open(self.fd_stderr, "r", encoding=self.command.encoding, closefd=closefd)

        self._stderr.seek(0)

        if lines:
            return self._stderr.readlines()

        return self._stderr.read()

    def close_io(self):
        if self._stdout is not None:
            self._stdout.close()

        if self._stderr is not None:
            self._stderr.close()
