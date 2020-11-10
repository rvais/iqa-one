import abc
from typing import Optional

from iqa.system.executor.executor import ExecutorBase
from iqa.system.executor.execution import ExecutionBase
from .service import Service, ServiceStatus


class ServiceFake(Service):
    """
    Represents a service used to control a Server component (Router or Broker).
    """

    TIMEOUT: int = 30

    def __init__(self, name: Optional[str], executor: ExecutorBase):
        super().__init__(name, executor)
        self.name: Optional[str] = name
        self.executor: ExecutorBase = executor

    @abc.abstractmethod
    def status(self) -> ServiceStatus:
        """
        Returns the service status
        :return: The status of this specific service
        :rtype: ServiceStatus
        """
        return NotImplemented

    @abc.abstractmethod
    def start(self, wait_for_messaging: bool = False) -> ExecutionBase:
        return NotImplemented

    @abc.abstractmethod
    def stop(self) -> ExecutionBase:
        return NotImplemented

    @abc.abstractmethod
    def restart(self, wait_for_messaging: bool = False) -> ExecutionBase:
        return NotImplemented

    @abc.abstractmethod
    def enable(self) -> ExecutionBase:
        return NotImplemented

    @abc.abstractmethod
    def disable(self) -> ExecutionBase:
        return NotImplemented
