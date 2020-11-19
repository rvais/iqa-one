from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional

from iqa.system.executor.executor import ExecutorBase
from iqa.system.executor.execution import ExecutionBase


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

    def __init__(self, name: Optional[str], executor: ExecutorBase) -> None:
        self.name: Optional[str] = name
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
