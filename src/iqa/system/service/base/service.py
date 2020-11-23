from abc import ABC, abstractmethod
from enum import Enum

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional
    from iqa.system.executor.base.executor import ExecutorBase
    from iqa.system.executor.base.execution import ExecutionBase


class ServiceStatus(Enum):
    RUNNING = 'running'
    STOPPED = 'stopped'
    FAILED = 'failed'
    UNKNOWN = 'unknown'


class Service(ABC):
    """
    Represents a service used to control a Server component (Router or Broker).
    """

    TIMEOUT: int = 30

    def __init__(self, executor: ExecutorBase, name: Optional[str] = None, **kwargs) -> None:
        self.name: str = name if name is not None else self.__name__
        self.executor: ExecutorBase = executor

    @abstractmethod
    def status(self) -> ServiceStatus:
        """
        Returns the service status
        :return: The status of this specific service
        :rtype: ServiceStatus
        """
        return NotImplemented

    @abstractmethod
    def start(self) -> ExecutionBase:
        return NotImplemented

    @abstractmethod
    def stop(self) -> ExecutionBase:
        return NotImplemented

    @abstractmethod
    def restart(self) -> ExecutionBase:
        return NotImplemented

    @abstractmethod
    def enable(self) -> Optional[ExecutionBase]:
        return NotImplemented

    @abstractmethod
    def disable(self) -> Optional[ExecutionBase]:
        return NotImplemented
