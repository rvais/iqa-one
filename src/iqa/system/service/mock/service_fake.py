import abc

from typing import TYPE_CHECKING
from iqa.system.service.base.service import Service, ServiceStatus

if TYPE_CHECKING:
    # from typing import Optional
    from iqa.system.executor.base.executor import ExecutorBase
    from iqa.system.executor.base.execution import ExecutionBase


class ServiceFake(Service):
    """
    Represents a service used to control a Server component (Router or Broker).
    """

    TIMEOUT: int = 30

    def __init__(self, executor: 'ExecutorBase', name: str, **kwargs) -> None:
        super().__init__(executor, name, **kwargs)

    @abc.abstractmethod
    def status(self) -> ServiceStatus:
        """
        Returns the service status
        :return: The status of this specific service
        :rtype: ServiceStatus
        """
        return NotImplemented

    @abc.abstractmethod
    def start(self, wait_for_messaging: bool = False) -> 'ExecutionBase':
        return NotImplemented

    @abc.abstractmethod
    def stop(self) -> 'ExecutionBase':
        return NotImplemented

    @abc.abstractmethod
    def restart(self, wait_for_messaging: bool = False) -> 'ExecutionBase':
        return NotImplemented

    @abc.abstractmethod
    def enable(self) -> 'ExecutionBase':
        return NotImplemented

    @abc.abstractmethod
    def disable(self) -> 'ExecutionBase':
        return NotImplemented
