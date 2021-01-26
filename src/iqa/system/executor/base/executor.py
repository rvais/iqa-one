import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from iqa.system.command.command_base import CommandBase

if TYPE_CHECKING:
    from typing import List, Type
    from iqa.system.executor.base.execution import ExecutionBase

from iqa.logger import logger


class ExecutorBase(ABC):
    """
    Defines the generic Executor class, which is responsible for
    running a given Command instance similarly across different
    implementations.
    """

    def __init__(self, **kwargs) -> None:
        self._logger: logging.Logger = logger
        self._executions: 'List[ExecutionBase]' = []
        self._name: str = 'Abstract Executor class'

    @staticmethod
    def implementation() -> str:
        return NotImplemented

    @property
    def name(self) -> str:
        return self._name

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
