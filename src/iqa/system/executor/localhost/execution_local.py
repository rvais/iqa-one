import logging
import subprocess
import tempfile
import threading
from typing import Union, Optional, IO

from iqa.system.command.command_base import CommandBase
from iqa.system.executor.execution import ExecutionBase, ExecutionException
from iqa.system.executor.executor import ExecutorBase

from iqa.utils.process import Process
from iqa.utils.timeout import TimeoutCallback

logger: logging.Logger = logging.getLogger(__name__)


class ExecutionProcess(ExecutionBase):
    """
    Represents a command Execution that is performed by a Process (subprocess.Popen child).
    Executors that want to run a given command as a Process must use this Execution strategy.
    """

    def __init__(
        self, command: CommandBase, executor: ExecutorBase, modified_args: list = None, env=None
    ) -> None:
        """
        Instance is initialized with the command that was effectively
        executed and the Executor instance that produced this new object.
        :param command:
        :param executor:
        :param modified_args:
        :param env:
        """

        # Prepare stdout handler
        if command.stdout:
            self.fh_stdout: Union[IO[str], int] = tempfile.TemporaryFile(
                mode='w+t', encoding=command.encoding
            )
        else:
            self.fh_stdout = subprocess.DEVNULL

        # Prepare stderr handler
        if command.stderr:
            self.fh_stderr: Union[IO[str], int] = tempfile.TemporaryFile(
                mode='w+t', encoding=command.encoding
            )
        else:
            self.fh_stderr = subprocess.DEVNULL

        # Subprocess instance
        self._process: Optional[Process] = None  # type: ignore
        self._timeout: Optional[TimeoutCallback] = None

        # Initializes the super class which will invoke the run method
        super(ExecutionProcess, self).__init__(
            command=command, modified_args=modified_args, env=env
        )

    def _run(self) -> None:
        """
        Executes the given command in a separate Thread using a Process (child of subprocess.Popen)
        and monitoring it, till it's done running. When done (or failed), if a timeout was defined,
        the TimeoutCallback will be canceled.
        :return:
        """

        def start_process() -> None:
            """
            Trigger method for separate thread that will effectively run the command.
            :return:
            """
            try:
                self._process = Process(
                    self.args,
                    stdout=self.fh_stdout,
                    stderr=self.fh_stderr,
                    env=self.env,
                )
            except Exception as ex:
                logger.error('Error executing process', ex)
                self.cancel_timer()
                self.failure = True
                raise ExecutionException(ex)

            # do nothing while process still running
            while self._process.poll() is None:
                pass

            logger.debug('Process has terminated')
            self.cancel_timer()

        # Execute process in a thread, so we can interrupt the timeout callback
        # when process completes without blocking calling thread.
        threading.Thread(target=start_process).start()
        while not self._process and not self.failure:
            pass

    def is_running(self) -> bool:
        """
        Returns true if process is still running.
        :return:
        """
        return self._process.is_running()

    def completed_successfully(self) -> bool:
        """
        Returns true if process has ended and return code was 0.
        :return:
        """
        return self._process.completed_successfully()

    def terminate(self) -> None:
        """
        Forces a given Process to terminate.
        :return:
        """
        logger.debug(
            'Terminating execution - PID: %s - CMD: %s' % (self._process.pid, self.args)
        )
        self._process.terminate()

    def wait(self) -> None:
        """
        Wraps the Popen wait method till process exits or times out.
        :return:
        """
        # Wait till process completes or timeout (notified by TimeoutCallback
        self._process.wait()

    def on_timeout(self) -> None:
        """
        This method is called internally by the TimeoutCallback in case
        the execution times out. It will notify the command instance
        that it has timed out.
        :return:
        """
        logger.debug(
            'Execution timed out after %d - PID: %s - CMD: %s'
            % (self.command.timeout, self._process.pid, self.args)
        )
        self.terminate()

    def read_stdout(self, lines: bool = False) -> Optional[Union[str, list]]:
        """
        Returns a string with the whole STDOUT content if the original
        command has stdout property defined as True. Otherwise
        None will be returned.
        :param lines: whether to return stdout as a list of lines
        :type lines: bool
        :return: Stdout content as str if lines is False, or as a list
        """
        if not isinstance(self.fh_stdout, int) and self.fh_stdout != subprocess.DEVNULL:
            self.fh_stdout.seek(0)

            if lines:
                return self.fh_stdout.readlines()

            return self.fh_stdout.read()

        else:
            return None

    def read_stderr(self, lines: bool = False) -> Optional[Union[str, list]]:
        """
        Returns a string with the whole STDERR content if the original
        command has stderr property defined as True. Otherwise
        None will be returned.
        :param lines: whether to return stdout as a list of lines
        :type lines: bool
        :return: Stdout content as str if lines is False, or as a list
        """
        if not isinstance(self.fh_stderr, int) and self.fh_stderr != subprocess.DEVNULL:
            self.fh_stderr.seek(0)

            if lines:
                return self.fh_stderr.readlines()

            return self.fh_stderr.read()

        else:
            return None
