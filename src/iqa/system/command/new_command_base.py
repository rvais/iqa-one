"""
Provides representation for Commands that can be executed against
ExecutorBase instances.
"""
from iqa.system.command.new_options_base import EmptyOptions

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, List, Callable, Union, Dict, Any
    from iqa.system.command.new_options_base import OptionsBase
    from os import PathLike


class CommandBase:
    """
    Represents a command that can be executed against different
    executors, behaving similarly across them.
    """

    def __init__(
            self,
            args: 'Optional[List[str]]' = None,
            path_to_exec: 'Optional[Union[str, bytes, PathLike]]' = None,
            stdout: bool = True,
            stderr: bool = True,
            daemon: bool = False,
            timeout: int = 0,
            encoding: str = 'utf-8',
            wait_for: bool = False,
            env: 'Optional[Dict]' = None,
            args_before_opts: bool = True,
            **kwargs
    ) -> None:
        self._args: List[str] = args if args is not None else []
        self._path_to_exec: Optional[Union[str, bytes, PathLike]] = path_to_exec
        self.stdout: bool = stdout
        self.stderr: bool = stderr
        self.damon: bool = daemon
        self.timeout: int = timeout
        self.encoding: str = encoding
        self.wait_for: bool = wait_for

        if env is None:
            env = {}
        self.env: dict = env

        self._options: Optional[OptionsBase] = None
        self._args_before_opts: bool = args_before_opts

        self._timeout_callbacks: List[Callable] = []
        self._interrupt_callbacks: List[Callable] = []
        self._pre_exec_hooks: List[Callable] = []
        self._post_exec_hooks: List[Callable] = []

    def build(self) -> 'List[str]':
        """
        Builds the external client command based on all
        ClientOptionsBase properties available on implementing class,
        using optconstruct to produce the arguments list.
        :return:
        """

        # Crate base list for the command
        command: List[str] = []
        if self._path_to_exec is not None:
            command.append(self._path_to_exec)

        # implementation of the options classes ensures that only populated ones are returned
        all_options: Dict = {}
        key: str
        value: Any
        for key, value in self._options.to_dictionary().items():
            all_options[key.replace('_', '-')] = value

        # Generates parameters list (only allowed will be added)
        params: List[str] = []
        for opt in self._options.valid_options():
            if opt.satisfied(all_options):
                params.extend(opt.generate(all_options).split(' ', 1))

        # based on selected ordering extend command first with arguments, then options or vice versa
        if self._args_before_opts:
            command.extend(self._args)
            command.extend(params)
        else:
            command.extend(params)
            command.extend(self._args)

        return command

    @property
    def args(self) -> 'List[str]':
        return self._args.copy()

    @args.setter
    def args(self, args: 'List[str]') -> None:
        self._args = args

    @property
    def path_to_exec(self) -> 'Optional[Union[str, bytes, PathLike]]':
        return self._path_to_exec

    @path_to_exec.setter
    def path_to_exec(self, path_to_exec: 'Optional[Union[str, bytes, PathLike]]') -> None:
        self._path_to_exec = path_to_exec

    @property
    def options(self) -> 'OptionsBase':
        """
        Delegated method that must return a list of all valid
        options allowed by the client command.
        List must be composed of OptionAbstract objects.
        :return:
        """
        if self._options is None:
            self._options = EmptyOptions()
        return self._options

    def add_timeout_callback(self, callback_method: 'Callable') -> None:
        """
        Adds a callback method to a list of methods that will
        be called in case this execution times out.
        Following argument types will be passed to the
        callback method: (execution: Execution).
        :param callback_method:
        :return:
        """
        self._timeout_callbacks.append(callback_method)

    @property
    def timeout_callbacks(self) -> 'List[Callable]':
        return self._timeout_callbacks.copy()

    def clear_timeout_callbacks(self) -> None:
        self._timeout_callbacks.clear()

    def add_interrupt_callback(self, callback_method: 'Callable') -> None:
        """
        Adds a callback method to a list of methods that will
        be called in case this execution is interrupted.
        Following argument types will be passed to the
        callback method: (execution: Execution).
        :param callback_method:
        :return:
        """
        self._interrupt_callbacks.append(callback_method)

    @property
    def interrupt_callbacks(self) -> 'List[Callable]':
        return self._interrupt_callbacks.copy()

    def clear_interrupt_callbacks(self) -> None:
        self._interrupt_callbacks.clear()

    def add_pre_exec_hook(self, pre_exec_hook_method: 'Callable') -> None:
        """
        Adds a callback method to a list of methods that will
        be called before Executor starts the process.
        Following argument types will be passed to the
        callback method: (command: Command, executor: Executor).
        :param pre_exec_hook_method:
        :return:
        """
        self._pre_exec_hooks.append(pre_exec_hook_method)

    @property
    def pre_exec_hooks(self) -> 'List[Callable]':
        return self._pre_exec_hooks.copy()

    def clear_pre_exec_hooks(self) -> None:
        self._pre_exec_hooks.clear()

    def add_post_exec_hook(self, post_exec_hook_method: 'Callable') -> None:
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

    @property
    def post_exec_hooks(self) -> 'List[Callable]':
        return self._post_exec_hooks.copy()

    def clear_post_exec_hooks(self) -> None:
        self._post_exec_hooks.clear()
