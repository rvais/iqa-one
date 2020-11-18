import logging
import os
import tempfile
import threading

import urllib3
from kubernetes import config, client
from kubernetes.client import Configuration, CoreV1Api
from kubernetes.client.apis import core_v1_api
from kubernetes.stream import stream
from kubernetes.stream.ws_client import WSClient

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, List, Union
    from iqa.system.command.command_base import CommandBase

from iqa.system.executor.base.execution import ExecutionBase, ExecutionException
from iqa.system.executor.kubernetes.executor_kubernetes import ExecutorKubernetes

# Logger for ExecutionKubernetes
logger: logging.Logger = logging.getLogger(__name__)
urllib3.disable_warnings()


class ExecutionKubernetes(ExecutionBase):
    """
    Represents the Execution of a command that is performed through the Kubernetes Client API (No local PID generated).
    Executors that want to run a given command through the Kubernetes Client API must use this Execution strategy.
    """

    def __init__(
        self,
        command: CommandBase,
        executor: ExecutorKubernetes,
        modified_args: Optional[List[str]] = None,
        env: Optional[dict] = None,
    ) -> None:
        """
        Instance is initialized with a command that was effectively
        executed and the Executor instance that produced this new object.
        The KubernetesExecution expects that executor is an ExecutorKubernetes.
        :param command:
        :param executor:
        :param modified_args:
        :param env:
        """
        # Set the config and get Api instance
        client_config: Configuration = client.Configuration()
        client_config.verify_ssl = False
        client_config.assert_hostname = False
        client_config.host = executor.host

        # Initializes the super class which will invoke the run method
        super(ExecutionKubernetes, self).__init__(
            command=command, executor=executor, modified_args=modified_args, env=env
        )

        self.executor: ExecutorKubernetes  # necessary type casting

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

        # If a token has been provided use it
        if executor.token:
            client_config.api_key = {'authorization': 'Bearer' + executor.token}

        # Loading kubernetes config when config and context provided
        if executor.config and executor.context:
            config.load_kube_config(
                config_file=executor.config,
                client_configuration=client_config,
                context=executor.context,
            )

        # Kubernetes API instance
        self.api: CoreV1Api = core_v1_api.CoreV1Api(client.ApiClient(client_config))

        # Kubernetes response (internal execution)
        self.response: WSClient

    def _run(self) -> None:
        """
        Run a separate thread to perform the command, so the thread can monitor
        for command completion in a non-blocking way.
        :return:
        """
        threading.Thread(target=self._run_as_thread).start()
        while not self.response and not self.failure:
            pass

    def _run_as_thread(self) -> None:
        """
        Method triggered by Thread that is meant to effectively execute the command using Kubernetes Client API.

        If an error has occurred or the WSClient (self.response) is no longer opened,
        the process is considered as done and if a TimeoutCallback has been set, then it will be canceled.
        :return:
        """
        self.executor: ExecutorKubernetes  # necessary type casting

        try:
            logger.debug('Retrieving PODs')
            pods = self.api.list_namespaced_pod(
                self.executor.namespace, label_selector=self.executor.selector
            )

            # If no pods found, throw error
            if not pods or not pods.items:
                raise ExecutionException(
                    'No PODs found using provided selector: %s' % self.executor.selector
                )

            pod = pods.items[0]
            pod_name = pod.metadata.name

            logger.info('Executing command on POD: %s' % pod_name)
            self.response = stream(
                self.api.connect_post_namespaced_pod_exec,
                pod_name,
                self.executor.namespace,
                command=self.args,
                stderr=self.command.stderr,
                stdout=self.command.stdout,
                stdin=False,
                tty=False,
                _preload_content=False,
            )
        except Exception as ex:
            logger.error('Error executing kubernetes command', ex)
            self.cancel_timer()
            self.failure: bool = True
            raise ExecutionException('Error invoking Kubernetes API') from ex

        # Thread must wait till process is complete
        while self.response.is_open():
            pass

        logging.debug('Process has terminated')
        self.cancel_timer()

    def wait(self) -> None:
        """
        Waits till execution of Command is considered as done, or timed out.
        :return:
        """
        timeout_secs: int = 0
        if self.command.timeout:
            timeout_secs = self.command.timeout

        # Waits till execution completes or times out
        if self.response and self.response.is_open():
            self.response.run_forever(timeout=timeout_secs)

    def is_running(self) -> bool:
        """
        Returns true if the self.response (WSClient) is still opened.
        :return:
        """
        return self.response and self.response.is_open()

    def completed_successfully(self) -> bool:
        """
        As this Execution does not represent a Process ID with a return code,
        we are controlling if it completed successfully if:
        - Execution is no longer runnning
        - No timed out occurred
        - Not interrupted by user
        - No failure identified
        :return:
        """
        return not any(
            [self.is_running(), self.timed_out, self.interrupted, self.failure]
        )

    def on_timeout(self) -> None:
        """
        If timed out then this method will close the self.response (WSClient).
        :return:
        """
        self.terminate()

    def terminate(self) -> None:
        """
        Closes the WSClient (self.response) if it is still running.
        :return:
        """
        if self.response and self.response.is_open():
            self.response.close()

    def read_stdout(self, lines: bool = False, closefd: bool = True) -> Optional[Union[str, List[str]]]:
        """
        Reads data from WSClient stdout channel and append it to internal temporary file.
        Then it returns all data collected from stdout.
        If lines is true, then an array will be generated.
        :param lines:
        :param closefd: closefd does nothing in this implementation
        :type closefd: bool
        :return:
        """
        if self._stdout is None:
            return None

        # Set offset to end of file
        self._stdout.seek(0, os.SEEK_END)

        # If new info read from stdout, append it
        if self.response.peek_stdout():
            self._stdout.write(self.response.read_stdout())

        return self._read_temp_file(self._stdout, lines)

    def read_stderr(self, lines: bool = False, closefd: bool = True) -> Optional[Union[str, List[str]]]:
        """
        Reads data from WSClient stderr channel and append it to internal temporary file.
        Then it returns all data collected from stderr.
        If lines is true, then an array will be generated.
        :param lines:
        :return:
        """
        if self._stderr is None:
            return None

        # Set offset to end of file
        self._stderr.seek(0, os.SEEK_END)

        # If new info read from stderr, append it
        if self.response.peek_stderr():
            self._stderr.write(self.response.read_stderr())
            self.response.update(timeout=1)

        return self._read_temp_file(self._stderr, lines)

    @staticmethod
    def _read_temp_file(fh, lines):
        """
        Move cursor to beginning of file and then returns all data available as
        a string (if lines is false) and as an array of strings (if lines is true).
        :param fh:
        :param lines:
        :return:
        """

        # Move to beginning of file
        fh.seek(0, os.SEEK_SET)

        # Return content as requested
        if lines:
            return fh.readline()
        else:
            return fh.read()
