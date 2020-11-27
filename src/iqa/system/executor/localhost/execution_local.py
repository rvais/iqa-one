import logging
import tempfile
import threading
from typing import TYPE_CHECKING

from iqa.system.executor.base.execution import ExecutionBase, ExecutionException

if TYPE_CHECKING:
    from typing import Optional, List
    from iqa.system.command.command_base import CommandBase
    from iqa.system.executor.base.executor import ExecutorBase

from iqa.utils.process import Process
from iqa.utils.timeout import TimeoutCallback

logger: logging.Logger = logging.getLogger(__name__)


class ExecutionProcess(ExecutionBase):
    """
    Represents a command Execution that is performed by a Process (subprocess.Popen child).
    Executors that want to run a given command as a Process must use this Execution strategy.
    """

    def __init__(
            self,
            command: CommandBase,
            executor: Optional[ExecutorBase] = None,
            modified_args: Optional[List[str]] = None,
            env: Optional[dict] = None
    ) -> None:
        """
        Instance is initialized with a command that was effectively
        executed and the Executor instance that produced this new object.
        :param command:
        :param executor:
        :param modified_args:
        :param env:
        """
        # Initializes the super class which will invoke the run method
        super(ExecutionProcess, self).__init__(
            command=command, executor=executor, modified_args=modified_args, env=env
        )

        if command.stdout:
            self._stdout = tempfile.TemporaryFile(
                mode='w+t', encoding=command.encoding
            )
            self._fd_stdout = self._stdout.fileno()

        if command.stderr:
            self._stderr = tempfile.TemporaryFile(
                mode='w+t', encoding=command.encoding
            )
            self._fd_stderr = self._stderr.fileno()

        # Subprocess instance
        self._process: Optional[Process] = None
        self._timeout: Optional[TimeoutCallback] = None

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
                    stdout=self.fd_stdout,
                    stderr=self.fd_stderr,
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
        if self._process is not None:
            return self._process.is_running()

        return False

    def completed_successfully(self) -> bool:
        """
        Returns true if process has ended and return code was 0.
        :return:
        """
        if self._process is not None:
            return self._process.completed_successfully()

        return False

    def terminate(self) -> None:
        """
        Forces a given Process to terminate.
        :return:
        """
        logger.debug(
            'Terminating execution - PID: %s - CMD: %s' % (self._process.pid, self.args)
        )
        if self._process is not None:
            self._process.terminate()

    def wait(self) -> None:
        """
        Wraps the Popen wait method till process exits or times out.
        :return:
        """
        # Wait till process completes or timeout (notified by TimeoutCallback
        if self._process is not None:
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
