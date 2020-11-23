from typing import Optional, Union, List

from iqa.abstract.listener import Listener
from iqa.abstract.server.router import Router
from iqa.components.abstract.server.server_component import ServerComponent
from iqa.system.command.command_base import CommandBase
from iqa.system.executor.execution import ExecutionBase
from iqa.system.node.node import Node
from iqa.utils.types import ManagementClientSubtype
from .config import Config
from .log import Log
from .management.qdmanage import QDManage
from .management.qdstat import QDStat


class Dispatch(ServerComponent, Router):
    """
    Dispatch router component
    """

    name: str = 'Qpid Dispatch Router'
    implementation: str = 'dispatch'

    def __init__(
        self,
        name: str,
        node: Node,
        listeners: Optional[List[Listener]] = None,
        **kwargs
    ) -> None:  # type: ignore
        super(Dispatch, self).__init__(name, node, listeners, **kwargs)

        self.qdmanage: QDManage = QDManage()
        self.qdstat: QDStat = QDStat()
        self.config: Config = Config()  # TODO - pass config as param to constructor
        self.log: Log = Log()
        self._version: Optional[str] = None

        self.port: str = kwargs.get('router_port', 5672)
        self.config = kwargs.get('router_config', None)
        self.user: Optional[str] = None
        self.password: Optional[str] = None
        self.pem_file: Optional[str] = None
        self.key_file: Optional[str] = None
        self.key_password: Optional[str] = None

        # initializing client from kwargs
        for func in [self.set_credentials, self.set_ssl_auth]:
            self.call_if_all_arguments_in_kwargs(func, **kwargs)

    @staticmethod
    def config_refresh_remote_to_testsuite() -> None:
        # TODO - This seems like a candidate to be part of Configuration class
        """
        Syncing router config from remote to test_suite
        :return:
        """

    @staticmethod
    def config_dump() -> None:
        # TODO - This seems like a candidate to be part of Configuration class
        """
        Dump (remote) router configuration file and create Configuration()
        :return:
        """

    def set_config(self, config_src, config_dst) -> None:
        # TODO - Need to describe the purpose of this method (unclear at the moment)
        """
        Set configuration from
        :param config_src:
        :param config_dst:
        :return:
        """

    @property
    def version(self) -> Optional[Union[str, list]]:
        """
        Get qdrouterd version
        :return:
        """
        if self._version:
            return self._version
        else:
            cmd = CommandBase(['qdrouterd', '-v'], stdout=True)
            cmd_exec: ExecutionBase = self.node.execute(cmd)
            return cmd_exec.read_stdout(lines=False)

    def set_credentials(self, user: str = None, password: str = None) -> None:
        """
        Stores user and password that must be used to communicate with the router instance
        through the main port defined in constructor method.
        :param user:
        :param password:
        :return:
        """
        self.user = user
        self.password = password

    def set_ssl_auth(
        self, pem_file: str = None, key_file: str = None, key_password: str = None
    ) -> None:
        """
        Defines SSL credentials that must be used to communicate with this router instance
        through its main port.
        :param pem_file:
        :param key_file:
        :param key_password:
        :return:
        """
        self.pem_file = pem_file
        self.key_file = key_file
        # Set to None when empty as well
        self.key_password = None if not key_password else key_password

    def has_credentials(self) -> bool:
        if self.user and self.password:
            return True
        else:
            return False

    def has_ssl_keys(self) -> bool:
        if self.pem_file and self.key_file:
            return True
        else:
            return False

    def get_management_client(self) -> ManagementClientSubtype:
        return NotImplemented
