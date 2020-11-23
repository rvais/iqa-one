import logging
import posixpath
import re
import time
from enum import Enum
from typing import TYPE_CHECKING

from iqa.system.command.command_ansible import CommandBaseAnsible
from iqa.system.command.command_base import CommandBase
from iqa.system.executor.ansible.executor_ansible import ExecutorAnsible
from iqa.system.service.base.service import ServiceStatus
from iqa.system.service.mock.service_fake import ServiceFake
from iqa.utils.tcp_util import is_tcp_port_available

if TYPE_CHECKING:
    from typing import Optional, Union
    from typing.re import Pattern
    from iqa.system.executor.base.executor import ExecutorBase
    from iqa.system.executor.base.execution import ExecutionBase


class ServiceFakeArtemis(ServiceFake):
    """
    Implementation of a Artemis pseudo-service to manage a Server component.
    """

    MAX_ATTEMPTS: int = 10
    DELAY: int = 3

    _logger: logging.Logger = logging.getLogger(__name__)

    def __init__(self, executor: ExecutorBase, name: Optional[str] = None, **kwargs) -> None:
        name = name if name is not None or name != '' else 'artemis-service'
        super().__init__(executor, name, **kwargs)

        self.ansible_host: str = kwargs.get('ansible_host', 'localhost')
        self.service_default_port: str = kwargs.get('artemis_port', '61616')
        self.service_web_port: str = kwargs.get('broker_web_port', '8161')
        self.service_path: str = posixpath.join(kwargs.get('broker_path'), 'bin', 'artemis-service')  # type: ignore
        self.service_username: str = kwargs.get('broker_service_user', 'jamq')

    class ServiceSystemState(Enum):
        STARTED = ('start', 'started')
        STOPPED = ('stop', 'stopped')
        RESTARTED = ('restart', 'restarted')

        def __init__(self, system_state, ansible_state):
            self.system_state = system_state
            self.ansible_state = ansible_state

    def status(self) -> ServiceStatus:
        """
        Returns the service status based on linux service.
        :return: The status of this specific service
        :rtype: ServiceStatus
        """
        # service output :
        # is running
        # is stopped

        # systemctl output:
        # (running)
        # (dead)

        # On RHEL7> service is automatically redirected to systemctl
        cmd_status: CommandBase = CommandBase(
            ['runuser', '-l', self.service_username, '%s status' % self.service_path],
            stdout=True,
            timeout=self.TIMEOUT,
        )
        execution: ExecutionBase = await self.executor.execute(cmd_status)

        service_output: Optional[Union[str, list]] = execution.read_stdout()

        if not service_output:
            ServiceFakeArtemis._logger.debug('Service: %s - Status: FAILED' % self.name)
            return ServiceStatus.FAILED

        running_pattern: Pattern = r'(is running|\(running\)|Running)'
        stopped_pattern: Pattern = r'(is stopped|\(dead\)|Stopped)'
        if re.search(running_pattern, service_output):
            ServiceFakeArtemis._logger.debug(
                'Service: %s - Status: RUNNING' % self.name
            )
            return ServiceStatus.RUNNING
        elif re.search(stopped_pattern, service_output):
            ServiceFakeArtemis._logger.debug(
                'Service: %s - Status: STOPPED' % self.name
            )
            return ServiceStatus.STOPPED

        ServiceFakeArtemis._logger.debug('Service: %s - Status: UNKNOWN' % self.name)
        return ServiceStatus.UNKNOWN

    def start(self, wait_for_messaging=False) -> ExecutionBase:
        execution: ExecutionBase = await self.executor.execute(
            self._create_command(self.ServiceSystemState.STARTED)
        )
        self._wait_for_messaging(wait_for_messaging)
        return execution

    def stop(self) -> ExecutionBase:
        return await self.executor.execute(
            self._create_command(self.ServiceSystemState.STOPPED)
        )

    def enable(self) -> ExecutionBase:
        return NotImplemented

    def disable(self) -> ExecutionBase:
        return NotImplemented

    def restart(self, wait_for_messaging=False) -> ExecutionBase:
        execution: ExecutionBase = await self.executor.execute(
            self._create_command(self.ServiceSystemState.RESTARTED)
        )
        self._wait_for_messaging(wait_for_messaging)
        return execution

    def _wait_for_messaging(self, messaging_wait=False):
        # Wait until broker web port is available
        self.__tcp_wait_for_accessible_port(self.service_web_port, self.ansible_host)

        # Or also messaging subsystem goes up
        if messaging_wait:
            self.__tcp_wait_for_accessible_port(
                self.service_default_port, self.ansible_host
            )

    @staticmethod
    def __tcp_wait_for_accessible_port(port, host):
        for attempt in range(ServiceFakeArtemis.MAX_ATTEMPTS):
            if attempt == ServiceFakeArtemis.MAX_ATTEMPTS - 1:
                print(
                    '     broker is not reachable after %d attempts'
                    % ServiceFakeArtemis.MAX_ATTEMPTS
                )

            if is_tcp_port_available(int(port), host):
                return True

            time.sleep(ServiceFakeArtemis.DELAY)
        ServiceFakeArtemis._logger.warning(
            'Unable to connect to hostname:port: %s:%s' % (host, port)
        )
        return False

    def _create_command(self, service_state: ServiceSystemState):
        """
        Creates a Command instance based on executor type and state
        that is specific to each type of command.
        :param service_state:
        :return:
        :return:
        """
        command: str = 'runuser -l %s %s %s' % (
            self.service_username,
            self.service_path,
            service_state.system_state,
        )
        if isinstance(self.executor, ExecutorAnsible):
            return CommandBaseAnsible(
                command, ansible_module='command', stdout=True, timeout=self.TIMEOUT
            )
        else:
            return CommandBase(command.split(), stdout=True, timeout=self.TIMEOUT)
