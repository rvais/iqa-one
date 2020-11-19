import logging
from typing import Optional, TYPE_CHECKING

from iqa.system.command.command_base import CommandBase
from iqa.system.executor.docker.executor_docker import ExecutorDocker
from iqa.system.executor.ansible.executor_ansible import ExecutorAnsible
from iqa.system.executor.execution import ExecutionBase
from iqa.system.service.service import Service
from .service_artemis import ServiceFakeArtemis
from .service_docker import ServiceDocker
from .service_system_init import ServiceSystemInit
from .service_systemd import ServiceSystemD

if TYPE_CHECKING:
    from iqa.utils.types import ExecutorType


class ServiceFactory(object):
    """
    This factory class can be used to help defining how Service implementation of the
    given Server Component will be used to manage startup/shutdown and ping of related
    component.

    When component is running in a docker container, startup/shutdown is done by
    starting / stopping the container.

    Otherwise a valid service name must be provided.
    """

    _logger: logging.Logger = logging.getLogger(__name__)

    @staticmethod
    def create_service(
        executor: 'ExecutorType', service_name: Optional[str] = None, **kwargs
    ) -> Service:
        if service_name:
            # Validate if systemd is available
            svc_cmd_exec: ExecutionBase = executor.execute(
                CommandBase(['pidof', 'systemd'], stdout=True, timeout=30)
            )
            if svc_cmd_exec.completed_successfully():
                # Create ServiceSystemD
                ServiceFactory._logger.debug(
                    'Creating ServiceSystemD - name: %s - executor: %s'
                    % (service_name, executor.__class__.__name__)
                )
                return ServiceSystemD(name=service_name, executor=executor)
            else:
                ServiceFactory._logger.debug(
                    'Creating ServiceSystemInit - name: %s - executor: %s'
                    % (service_name, executor.__class__.__name__)
                )
                return ServiceSystemInit(name=service_name, executor=executor)
        else:
            container_name: Optional[str] = None
            if isinstance(executor, ExecutorDocker):
                container_name = executor.container_name
            elif (
                isinstance(executor, ExecutorAnsible)
                and executor.ansible_connection == 'docker'
            ):
                container_name = executor.ansible_host
            elif isinstance(executor, ExecutorAnsible):
                ServiceFactory._logger.debug(
                    'Creating ServiceArtemis - name: %s - executor: %s'
                    % (service_name, executor.__class__.__name__)
                )
                return ServiceFakeArtemis(
                    name=service_name, executor=executor, **kwargs
                )

            if container_name:
                ServiceFactory._logger.debug(
                    'Creating ServiceDocker - name: %s - executor: %s'
                    % (container_name, executor.__class__.__name__)
                )
                return ServiceDocker(name=container_name, executor=executor)  # type: ignore

        ServiceFactory._logger.debug('Unable to determine Service')
        raise ValueError('Unable to determine service for server component')
