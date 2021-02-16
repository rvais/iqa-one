import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from iqa.system.command.command_base import CommandBase

if TYPE_CHECKING:
    from os import PathLike
    from typing import Optional, List, Type, Union
    from iqa.system.executor.base.execution import ExecutionBase

from iqa.logger import logger


class ExecutorBase(ABC):
    """
    Defines the generic Executor class, which is responsible for
    running a given Command instance similarly across different
    implementations.
    """

    def __init__(
        self,
        host: 'Optional[str]' = None,
        port: 'Optional[int]' = None,
        user: 'Optional[str]' = None,
        password: 'Optional[str]' = None,
        ssh_key_path: 'Optional[Union[str, bytes, PathLike]]' = None,
        ssh_key_passphrase: 'Optional[Union[str, bytes, PathLike]]' = None,
        known_hosts_path: 'Optional[Union[str, bytes, PathLike]]' = None,
        **kwargs
    ) -> None:
        self._logger: logging.Logger = logger
        self._executions: 'List[ExecutionBase]' = []
        self._name: str = 'Abstract Executor class'

        self._host: Optional[str] = host
        self._port: Optional[int] = port
        self._user: Optional[str] = user
        self._password: Optional[str] = password
        self._ssh_key_path: Optional[Union[str, bytes, PathLike]] = ssh_key_path
        self._ssh_key_passphrase: Optional[Union[str, bytes, PathLike]] = ssh_key_passphrase
        self._known_hosts_path: Optional[Union[str, bytes, PathLike]] = known_hosts_path

    @staticmethod
    def _check_required_args(required: 'List[str]', **kwargs) -> 'List[str]':
        return [x for x in required if x not in kwargs.keys() or kwargs[x] is None]

    @staticmethod
    def implementation() -> str:
        return NotImplemented

    def execute(self, command: CommandBase) -> 'ExecutionBase':
        """
        Executes the given command differently based on
        concrete implementation of this generic Executor.
        An Execution instance will be returned and both
        pre and post execution handlers will be invoked
        on the given command.
        :param command:
        :return:
        """

        # Call pre-execution hooks
        # await command.on_pre_execution(self)

        # Delegate execution to concrete Executor
        self._logger.debug(
            'Executing command with [%s] - %s' % (self.__class__.__name__, command.args)
        )
        execution: ExecutionBase = self._execute(command)

        # Processing post-execution hooks
        # await command.on_post_execution(execution)

        # returning execution
        return execution

    @abstractmethod
    def _execute(self, command: CommandBase) -> 'ExecutionBase':
        """
        Abstract method that must be implemented by child classes.
        :param command:
        :return:
        """
        raise NotImplementedError

    @staticmethod
    def get_preferred_command_base() -> 'Type[CommandBase]':
        return CommandBase
