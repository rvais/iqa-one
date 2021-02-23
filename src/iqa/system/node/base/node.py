"""
Interface for Node element. A node holds a running messaging component and it
must provide some basic behaviors, like ping, get_ip and execute command.
"""
import abc
import logging
from typing import TYPE_CHECKING

from iqa.utils.ping import ping
from iqa.system.executor.base.execution import ExecutionException

if TYPE_CHECKING:
    from typing import Optional, List, Dict  # , Union
    from iqa.system.command.command_base import CommandBase
    from iqa.system.executor.base.execution import ExecutionBase
    from iqa.system.executor.base.executor import ExecutorBase


class Node(abc.ABC):
    """Node abstract component"""

    implementation = NotImplemented

    def __init__(
        self,
        hostname: str,
        executor: 'ExecutorBase',
        ip: 'Optional[str]' = None,
        name: 'Optional[str]' = None,
        **kwargs
    ) -> None:
        logging.getLogger().info(f"Initialization of Node ({self.__class__.__name__}): {hostname}")
        self.hostname: str = hostname
        self.name: str = name if name else hostname
        self._executors: List[ExecutorBase] = [executor]
        self._tasks: Dict[CommandBase, Optional[ExecutionBase]] = {}
        # In case we want to keep more than just last execution of given command
        # self._tasks: Dict[CommandBase, Optional[Union[ExecutionBase, List[ExecutionBase]]]] = {}
        self.ip: Optional[str] = ip
        self.reachable: bool = False

        self._is_reachable()

    def execute(self, command: 'CommandBase') -> 'ExecutionBase':
        """Execute command using Node's executor"""
        executor: ExecutorBase
        result: Optional[ExecutionBase] = None
        for executor in self._executors:
            if isinstance(command, executor.get_preferred_command_base()):
                result = executor.execute(command)
                break

        if result is None:
            msg: str = f"No suitable executor for {command.__class__.__name__} on node {self.name} {self.hostname}."
            raise ExecutionException(msg)

        return result

    def execute_all(self, execute_completed: bool = False) -> 'List[ExecutionBase]':
        command: CommandBase
        result: ExecutionBase
        executions: List[ExecutionBase] = []
        for command, result in self._tasks.items():
            if result is None or execute_completed:
                result = self.execute(command)
                executions.append(result)

        for execution in executions:
            self._tasks[execution.command] = execution

        # In case we want to keep more than just last execution of given command
        # for execution in executions:
        #     if isinstance(self._tasks[execution.command], list):
        #         self._tasks[execution.command].append(execution)
        #     elif self._tasks[execution.command] is not None:
        #         self._tasks[execution.command] = execution

        return executions

    def add_executor(self, executor: 'ExecutorBase') -> None:
        if executor is not None:
            self._executors.append(executor)

    def add_task(self, command: 'CommandBase') -> None:
        if command is not None and command not in self._tasks.keys():
            self._tasks[command] = None

    def get_result(self, command: 'CommandBase') -> 'ExecutionBase':
        if command is not None:
            self.add_task(command)
            self._tasks[command] = self.execute(command)
            return self._tasks[command]
        msg: str = "Value of command parameter must be CommandBase object to search for and or execute. 'None' given."
        raise ValueError(msg)

    def get_results(self) -> 'Dict[CommandBase, ExecutionBase]':
        return self._tasks.copy()

    def get_executions(self) -> 'List[ExecutionBase]':
        executions: List[ExecutionBase] = []
        for item in self._tasks.values():
            if item is not None and isinstance(item, list):
                executions.extend(item)
            elif item is not None:
                executions.append(item)

        return executions

    @abc.abstractmethod
    def ping(self) -> bool:
        raise NotImplemented

    @abc.abstractmethod
    def get_ip(self) -> str:
        raise NotImplemented

    def _is_reachable(self) -> bool:
        """ Is node reachable?

        Try to ping node from the host where IQA running if is reachable.
        """
        if self.ip:
            reachable: bool = ping(host=self.ip)

            if reachable:
                logging.getLogger().info('Node %s is reachable.' % self.hostname)
                self.reachable = True
            else:
                logging.getLogger().warning('Node %s is not reachable from IQA!' % self.hostname)
                self.reachable = False

            return reachable
        else:
            logging.getLogger().warning('Node %s does not have an IP address!' % self.hostname)
            self.reachable = False
            return False
