"""
Provides representation for Commands that can be executed against
ExecutorBase instances.
"""
from typing import Optional, Any
from os import PathLike


class CommandBase:
    """
    Represents a command that can be executed against different
    executors, behaving similarly across them.
    """

    def __init__(
        self,
        args: list,
        path_to_exec: Optional[PathLike[Any]] = None,
        stdout: bool = True,
        stderr: bool = True,
        timeout: int = 0,
        encoding: str = 'utf-8',
        wait_for: bool = False,
        env: Optional[dict] = None
    ) -> None:
        """
        Creates an instance of a Command representation that can be passed to
        an ExecutorBase instance.
        :param args: List of arguments that compose the command to be executed
        :param stdout: If True stdout will be available at the
        resulting Execution instance.
        :param stderr: If True stderr will be available at the
        resulting Execution instance.
        :param timeout: If a positive number provided, the process
        will be terminated on timeout and the registered timeout
        callbacks will be invoked.
        :param encoding: Encoding when reading stdout and stderr.
        """

        self._args: list = args
        self.path_to_exec = path_to_exec if not None else ''
        self.stdout: bool = stdout
        self.stderr: bool = stderr
        self.timeout: int = timeout
        self.encoding: str = encoding
        self.wait_for: bool = wait_for

        if env is None:
            env = {}
        self.env: dict = env

        self._timeout_callbacks: list = []
        self._interrupt_callbacks: list = []
        self._pre_exec_hooks: list = []
        self._post_exec_hooks: list = []

    @property
    def args(self) -> list:
        return self._args

    @args.setter
    def args(self, args):
        self._args = args

    def __str__(self):
        return " ".join(self.args)

    def add_timeout_callback(self, callback_method) -> None:
        """
        Adds a callback method to a list of methods that will
        be called in case this execution times out.
        Following argument types will be passed to the
        callback method: (execution: Execution).
        :param callback_method:
        :return:
        """
        self._timeout_callbacks.append(callback_method)

    def add_interrupt_callback(self, callback_method) -> None:
        """
        Adds a callback method to a list of methods that will
        be called in case this execution is interrupted.
        Following argument types will be passed to the
        callback method: (execution: Execution).
        :param callback_method:
        :return:
        """
        self._interrupt_callbacks.append(callback_method)

    def add_pre_exec_hook(self, pre_exec_hook_method) -> None:
        """
        Adds a callback method to a list of methods that will
        be called before Executor starts the process.
        Following argument types will be passed to the
        callback method: (command: Command, executor: Executor).
        :param pre_exec_hook_method:
        :return:
        """
        self._pre_exec_hooks.append(pre_exec_hook_method)

    def add_post_exec_hook(self, post_exec_hook_method) -> None:
        """
        Adds a callback method to a list of methods that will
        be called after Execution instance is started by
        the related Executor.
        Following argument types will be passed to the
        callback method: (execution: Execution).
        :param post_exec_hook_method:
        :return:
        """
        self._post_exec_hooks.append(post_exec_hook_method)

    def on_timeout(self, execution) -> None:
        """
        Called by the Execution in case it times out. This method
        will call all registered timeout callbacks.
        :param execution:
        :return:
        """
        for timeout_callback in self._timeout_callbacks:
            timeout_callback(execution)

    def on_interrupt(self, execution) -> None:
        """
        Called by the Execution instance in case it gets interrupted.
        Once interrupted, this method will call all registered
        interrupt callbacks.
        :param execution:
        :return:
        """
        for interrupt_callback in self._interrupt_callbacks:
            interrupt_callback(execution)

    def on_pre_execution(self, executor) -> None:
        """
        This is called internally by the Executor when the execute()
        method is invoked, prior to creating the Execution instance.
        All registered pre-execution hooks will be called.
        :param executor:
        :return:
        """
        for pre_exec_hook in self._pre_exec_hooks:
            pre_exec_hook(self, executor)

    def on_post_execution(self, execution) -> None:
        """
        This is called internally by the Executor after Execution
        instance is created (and started), causing all registered
        post execution callbacks to be called.
        Note that this is not called when the execution completes,
        instead it will be called when execution has started.
        :param execution:
        :return:
        """
        for post_exec_hook in self._post_exec_hooks:
            post_exec_hook(execution)
