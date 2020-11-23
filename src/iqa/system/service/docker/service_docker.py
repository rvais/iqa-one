import logging
from enum import Enum
from typing import TYPE_CHECKING

from docker.errors import APIError, NotFound

from iqa.system.service.base.service import Service, ServiceStatus
from iqa.utils.docker_util import get_container

if TYPE_CHECKING:
    from typing import Optional
    from iqa.system.executor.base.execution import ExecutionBase
    from iqa.system.executor.docker.executor_docker import ExecutorDocker


class ServiceDocker(Service):
    """
    Implementation of a service represented by a docker container.
    So startup and shutdown are done by managing current state of related
    docker container name.
    """

    _logger: logging.Logger = logging.getLogger(__name__)

    def __init__(self, executor: ExecutorDocker, name: str, **kwargs) -> None:
        super().__init__(executor, name, **kwargs)
        self.docker_host: Optional[str] = executor.docker_host
        self.container = get_container(name=self.name)

    class ServiceDockerState(Enum):
        STARTED = ('start', 'started')
        STOPPED = ('stop', 'exited')
        RESTARTED = ('restart', 'started')

        def __init__(self, system_state, ansible_state) -> None:
            self.system_state = system_state
            self.ansible_state = ansible_state

    @property
    def status(self) -> ServiceStatus:
        """
        Returns the status based on status of container name.
        :return: The status of this specific service
        :rtype: ServiceStatus
        """
        try:
            self.container.reload()

            if not self.container:
                ServiceDocker._logger.debug('Service: %s - Status: UNKNOWN' % self.name)
                return ServiceStatus.UNKNOWN

            if self.container.status == 'running':
                ServiceDocker._logger.debug('Service: %s - Status: RUNNING' % self.name)
                return ServiceStatus.RUNNING

            elif self.container.status == 'exited':
                ServiceDocker._logger.debug('Service: %s - Status: STOPPED' % self.name)
                return ServiceStatus.STOPPED

        except APIError or NotFound:
            ServiceDocker._logger.exception(
                'Error retrieving status of docker container'
            )
            return ServiceStatus.FAILED

        return ServiceStatus.UNKNOWN

    async def start(self) -> ExecutionBase:
        return self.container.start()

    async def stop(self) -> ExecutionBase:
        return self.container.stop()

    async def restart(self) -> ExecutionBase:
        return self.container.restart()

    def enable(self) -> Optional[ExecutionBase]:
        """
        Simply ignore it (not applicable to containers)
        :return:
        """
        return None

    def disable(self) -> Optional[ExecutionBase]:
        """
        Simply ignore it (not applicable to containers)
        :return:
        """
        return None
