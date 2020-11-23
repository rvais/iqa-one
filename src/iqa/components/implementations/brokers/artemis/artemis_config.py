import logging
import posixpath
from typing import Optional, Union

from amqcfg import amqcfg

from iqa.abstract.user import User
from iqa.components.abstract.server.server_component import ServerComponent
from iqa.components.brokers.broker_config import BrokerConfiguration
from iqa.system.executor import ExecutorBase
from iqa.system.executor import ExecutionBase
from iqa.system.service import ServiceFakeArtemis
from iqa.utils.exceptions import IQAConfigurationException
from iqa.utils.utils import remove_prefix


class ArtemisConfig(BrokerConfiguration):
    """Placeholder class of read configuration details for Artemis/AMQ 7
    from provided input file.
    Input file is json supported only (yaml in the future).

    This class is directly tied to ExternalBroker.
    """

    DEFAULT_HOME: str = '/opt/jboss-amq-7'
    DEFAULT_INSTANCE_HOME: str = '/opt/jboss-amq-7-i0'
    DEFAULT_INSTANCE_NAME: str = 'amq'
    DEFAULT_USERS: dict = {
        'admin': {
            'password': 'admin',
            'role': 'amq',
            'key': '/path/to/key',
            'ticket': '/path/to/ticket',
        },
        'tckuser': {
            'password': 'tckuser',
            'role': 'amq'
        },
        'superuser': {
            'password': 'superuser',
            'role': 'amq'
        },
        'administrator': {
            'password': 'administrator',
            'role': 'amq'
        },
        'nobody': {
            'password': 'nobody',
            'role': 'amq'
        },
    }
    DEFAULT_PORTS: dict = {
        'openwire': 61616,
        'amqp': 5672,
        'mqtt': 1883,
        'core': 5445,
        'stomp': 61613,
        'web': 8161,
        'jmx': 1099,
    }
    DEFAULT_PORT_JMX: int = 1099
    DEFAULT_PORT_WEB: int = 8161

    P_PROFILE_PATH: str = 'render/profile_path'
    P_HOME: str = 'artemis_profile/home'
    P_INSTANCE_NAME: str = 'broker_xml/name'
    P_INSTANCE_HOME: str = 'artemis_profile/instance'
    P_INSTANCE_DIR_ETC: str = 'artemis_profile/instance_etc_uri'
    P_INSTANCE_DIR_DATA: str = 'artemis_profile/data_dir'

    P_USERS: str = 'artemis_users'
    P_ROLES: str = 'artemis_roles'

    P_PORTS: str = 'broker_xml/acceptors'
    P_WEB_PORT: str = 'bootstrap_xml/web/bind/port'
    P_JMX_PORT: str = 'management_xml/connector_port'

    instance_name: Optional[Union[int, str, list, dict]]
    instance_home: Optional[Union[int, str, list, dict]]
    instance_home_etc: Union[int, str, list, dict]
    instance_home_data: Optional[Union[int, str, list, dict]]
    instance_home_log: Union[int, str, list, dict]
    instance_home_tmp: Union[int, str, list, dict]

    home: Optional[Union[int, str, list, dict]]
    amqcfg_profile_path: Optional[Union[int, str, list, dict]]

    def __init__(self, component: ServerComponent, **kwargs) -> None:
        """Initialize ExternalBrokerData from provided configuration file.

        :param broker_data: empty data object, to be filled with provided configuration data
        :type broker_data: ExternalBrokerData
        :param test_node: test node which is running given broker
        :type test_node: TestNode
        """

        super(ArtemisConfig, self).__init__(component, **kwargs)

    def create_default_configuration(self, **kwargs) -> None:
        self.home = kwargs.get('broker_home', self.DEFAULT_HOME)
        self.instance_home = kwargs.get('broker_path', self.DEFAULT_INSTANCE_HOME)
        self.instance_name = kwargs.get('broker_name', self.DEFAULT_INSTANCE_NAME)
        self.ports['web'] = kwargs.get('broker_web_port', self.DEFAULT_PORT_WEB)
        self.users['admin'] = User('admin', 'admin', roles=['amq'])

    def create_configuration(self, config_file_path: str) -> None:
        self.load_configuration_yaml(config_file_path)
        self.load_configuration()

    def load_configuration(self) -> None:
        self.home = self._data_getter(self.P_HOME, self.DEFAULT_HOME)
        self.instance_home = self._data_getter(
            self.P_INSTANCE_HOME, self.DEFAULT_INSTANCE_HOME
        )
        self.instance_name = self._data_getter(
            self.P_INSTANCE_NAME, self.DEFAULT_INSTANCE_NAME
        )
        self.instance_home_etc = remove_prefix(
            self._data_getter(
                self.P_INSTANCE_DIR_ETC, 'artemis_profile/instance_etc_uri'
            ),
            'file:',
        )
        self.node_config_dir: Union[int, str, list, dict] = self.instance_home_etc
        self.instance_home_data = self._data_getter(
            self.P_INSTANCE_DIR_DATA, 'artemis_profile/data_dir'
        )
        self.instance_home_log = posixpath.join(self.instance_home, 'log')  # type: ignore
        self.instance_home_tmp = posixpath.join(self.instance_home, 'tmp')  # type: ignore
        self.ports = self.assign_ports()
        self.assign_users()
        self.amqcfg_profile_path = self._data_getter(
            self.P_PROFILE_PATH, 'render/profile_path'
        )
        # self.topology = TopologyData(broker_data) or None

    def assign_ports(self) -> dict:
        ports = {}
        acceptors: dict = self._data_getter(self.P_PORTS, self.DEFAULT_PORTS)  # type: ignore

        for acceptor in acceptors:
            ports[acceptor.get('name')] = acceptor.get('port')

        ports['jmx'] = self._data_getter(self.P_JMX_PORT, self.DEFAULT_PORT_JMX)
        ports['web'] = self._data_getter(self.P_WEB_PORT, self.DEFAULT_PORT_WEB)
        return ports

    def assign_users(self) -> None:
        """
        :return:
        :rtype:
        """
        tmp_users: dict = self._data_getter(self.P_USERS, self.DEFAULT_USERS)  # type: ignore
        roles: dict = self._data_getter(self.P_ROLES, None)  # type: ignore

        for user in tmp_users:
            self.users[user] = User(user, tmp_users[user])

        for role in roles.keys():
            for user_in_role in roles[role]:
                user_obj: User = self._get_user(user_in_role)
                user_obj.roles.append(role)

    def get_users(self) -> dict:
        return self.users

    def get_acceptors(self) -> dict:
        return self.ports

    def _get_user(self, username: str) -> User:
        return self.users.get(username)  # type: ignore

    def get_username(self, user: User) -> str:
        return self._get_user(user.username).username

    def get_user_password(self, username: str) -> str:
        return self._get_user(username).password

    def apply_config(self, yaml_configuration_path: str, restart: bool = True):
        # self.store_configuration()
        self.component.service = ServiceFakeArtemis(None, ExecutorBase())

        try:
            # Todo hacky way to turn off debug logging from amqcfg module
            amqcfg.LOG.setLevel(logging.WARN)
            if self.LOGGER.level != logging.DEBUG:
                amqcfg.LOG.setLevel(logging.WARN)
            amqcfg.generate(
                profile=yaml_configuration_path,
                output_path=self.local_config_dir,
                write_profile_data=True,
            )
            execution: ExecutionBase = self.copy_configuration_files()

            if execution.completed_successfully():
                self.load_configuration_yaml(yaml_configuration_path)
                self.load_configuration()
            else:
                self.LOGGER.error(execution.read_stderr())
                raise IQAConfigurationException('Unable to copy config files to node.')
        except Exception:
            self.restore_config()
            raise IQAConfigurationException(
                'Unable to apply new configuration. Original config kept.'
            )
        finally:
            self.LOGGER.info(
                'Configuration from "%s" successfully applied.'
                % yaml_configuration_path
            )

        if restart and self.component.service is not None:
            self.component.service.restart(wait_for_messaging=True)
