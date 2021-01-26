import logging
from typing import TYPE_CHECKING

from iqa.system.command.command_base import CommandBase
from iqa.system.service.base.service import Service
from iqa.system.service.system_d.service_systemd import ServiceSystemD
from iqa.system.service.system_init.service_system_init import ServiceSystemInit
from iqa.system.service import __package__
from iqa.utils.walk_package import walk_package_and_import

if TYPE_CHECKING:
    from typing import Optional, List, Type
    from iqa.system.executor.base.executor import ExecutorBase
    from iqa.system.executor.base.execution import ExecutionBase


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
    __known_implementations: 'List[Type[Service]]' = walk_package_and_import(__package__, Service)

    @staticmethod
    def create_service(
            executor: 'ExecutorBase',
            service_name: 'Optional[str]' = None,
            **kwargs
    ) -> Service:
        srv: Optional[Service] = None
        cls: Optional[Type] = None
        if service_name:
            # Try to find specific implementation by name
            for cls in ServiceFactory.__known_implementations:
                if cls.__name__ == service_name:
                    srv = cls(executor=executor, name=service_name, **kwargs)
                    break

            # If service instance haven't been created yet, try to get one with systemD or SystemInit
            if srv is None:
                # Check if systemD is available
                svc_cmd_exec: ExecutionBase = executor.execute(
                    CommandBase(['pidof', 'systemd'], stdout=True, timeout=30)
                )
                if svc_cmd_exec.completed_successfully():
                    # SystemD is available so create service using that
                    ServiceFactory._logger.debug(
                        'Creating ServiceSystemD - name: %s - executor: %s'
                        % (service_name, executor.__class__.__name__)
                    )
                    srv = ServiceSystemD(name=service_name, executor=executor, **kwargs)
                else:
                    # SystemD is not available so try to create service using alternative (SystemInit)
                    ServiceFactory._logger.debug(
                        'Creating ServiceSystemInit - name: %s - executor: %s'
                        % (service_name, executor.__class__.__name__)
                    )
                    srv = ServiceSystemInit(name=service_name, executor=executor)
        else:
            # Name of wanted service has not been provided, use executor type to create service.
            for cls in ServiceFactory.__known_implementations:
                impl: str = 'implementation'
                docker: str = 'docker'
                container: str = 'container_name'
                ans_conn: str = 'ansible_connection'
                ans_host: str = 'ansible_host'

                if getattr(cls, impl, '') == docker and getattr(executor, impl, '') == docker:
                    service_name = getattr(executor, container, service_name)
                    break

                elif getattr(cls, impl, '') == docker and getattr(executor, ans_conn, '') == docker:
                    service_name = getattr(executor, ans_host, service_name)
                    break

                elif getattr(cls, impl, 'ServiceImplementation') == getattr(executor, impl, 'ExecutorImplementation'):
                    break
                else:
                    cls = None

            if cls is None:
                raise ValueError('Unable to determine the kind of service based on given arguments.')

            ServiceFactory._logger.debug(
                'Creating service %s with name: %s and executor: %s'
                % (cls.__name__, service_name, executor.__class__.__name__)
            )
            srv = cls(executor=executor, name=service_name, **kwargs)

        return srv
