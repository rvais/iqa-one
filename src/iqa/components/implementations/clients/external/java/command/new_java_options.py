from typing import TYPE_CHECKING

from optconstruct.types import Prefixed

if TYPE_CHECKING:
    from typing import Optional, Union, List
    from optconstruct.types import Toggle, KWOption, ListOption

from iqa.components.implementations.clients.external.command.options.new_client_options import (
    ControlOptionsCommon,
    ControlOptionsSenderReceiver,
    ConnectionOptionsCommon,
    LoggingOptionsCommon
)

"""
Specialized options for external Java client commands (cli-qpid.jar).
"""

class JavaControlOptionsSenderReceiver(ControlOptionsSenderReceiver):
    """
    Specialized implementation of control options for Sender and Receiver Java client commands.
    """

    def __init__(
        self,
        broker: str = '127.0.0.1:5672',
        address: str = 'examples',
        count: int = 1,
        timeout: 'Optional[int]' = None,
        sync_mode: 'Optional[str]' = None,
        close_sleep: 'Optional[int]' = None,
        duration: 'Optional[int]' = None,
        duration_mode: 'Optional[str]' = None,
        capacity: 'Optional[int]' = None,
        **kwargs
    ) -> None:
        # No timeout on java client is -1
        if timeout is None:
            self.timeout = -1

        # dump arguments into dictionary
        inputs = locals()
        # remove self and kwargs variables as they would mess things up
        del inputs['self']
        del inputs['kwargs']
        # update kwargs to pass in super().__init__()
        kwargs.update(inputs)
        super(JavaControlOptionsSenderReceiver, self).__init__(**kwargs)

    @staticmethod
    def valid_options() -> 'List[Union[Toggle, Prefixed, KWOption, ListOption]]':
        return [

        ]


class JavaConnectionOptionsCommon(ConnectionOptionsCommon):

    def __init__(
        self,
        conn_auth_mechanisms: 'Optional[str]' = None,
        conn_username: 'Optional[str]' = None,
        conn_password: 'Optional[str]' = None,
        conn_ssl_keystore_location: 'Optional[str]' = None,
        conn_ssl_keystore_password: 'Optional[str]' = None,
        conn_ssl_key_alias: 'Optional[str]' = None,
        conn_ssl_trust_all: 'Optional[str]' = None,
        conn_ssl_verify_host: 'Optional[str]' = None,
        urls: 'Optional[str]' = None,
        reconnect: bool = False,
        reconnect_interval: 'Optional[int]' = None,
        reconnect_limit: 'Optional[int]' = None,
        reconnect_timeout: 'Optional[int]' = None,
        heartbeat: 'Optional[int]' = None,
        max_frame_size: 'Optional[int]' = None,
        **kwargs
    ) -> None:
        # dump arguments into dictionary
        inputs = locals()
        # remove self and kwargs variables as they would mess things up
        del inputs['self']
        del inputs['kwargs']
        # update kwargs to pass in super().__init__()
        kwargs.update(inputs)
        super(JavaConnectionOptionsCommon, self).__init__(**kwargs)

    @staticmethod
    def valid_options() -> 'List[Union[Toggle, Prefixed, KWOption, ListOption]]':
        return [
            Prefixed('broker', '--broker'),
            Prefixed('address', '--address'),
            Prefixed('conn-auth-mechanisms', '--conn-auth-mechanisms'),
            Prefixed('conn-username', '--conn-username'),
            Prefixed('conn-password', '--conn-password'),
            Prefixed('conn-ssl-keystore-location', '--conn-ssl-keystore-location'),
            Prefixed('conn-ssl-keystore-password', '--conn-ssl-keystore-password'),
            Prefixed('conn-ssl-key-alias', '--conn-ssl-key-alias'),
            Prefixed('conn-ssl-trust-all', '--conn-ssl-trust-all'),
            Prefixed('conn-ssl-verify-host', '--conn-ssl-verify-host'),
        ]


class JavaConnectorCommand(JavaConnectionOptionsCommon, ControlOptionsCommon, LoggingOptionsCommon):

    def __init__(
        self,
        broker: str = '127.0.0.1:5672',
        address: str = 'examples',
        count: int = 1,
        timeout: 'Optional[int]' = None,
        sync_mode: 'Optional[str]' = None,
        close_sleep: 'Optional[int]' = None,
        duration: 'Optional[int]' = None,
        duration_mode: 'Optional[str]' = None,
        capacity: 'Optional[int]' = None,
        log_lib: 'Optional[str]' = None,
        log_stats: 'Optional[str]' = None,
        conn_auth_mechanisms: 'Optional[str]' = None,
        conn_username: 'Optional[str]' = None,
        conn_password: 'Optional[str]' = None,
        conn_ssl_keystore_location: 'Optional[str]' = None,
        conn_ssl_keystore_password: 'Optional[str]' = None,
        conn_ssl_key_alias: 'Optional[str]' = None,
        conn_ssl_trust_all: 'Optional[str]' = None,
        conn_ssl_verify_host: 'Optional[str]' = None,
        urls: 'Optional[str]' = None,
        reconnect: bool = False,
        reconnect_interval: 'Optional[int]' = None,
        reconnect_limit: 'Optional[int]' = None,
        reconnect_timeout: 'Optional[int]' = None,
        heartbeat: 'Optional[int]' = None,
        max_frame_size: 'Optional[int]' = None,
        **kwargs
    ) -> None:
        # dump arguments into dictionary
        inputs = locals()
        # remove self and kwargs variables as they would mess things up
        del inputs['self']
        del inputs['kwargs']
        # update kwargs to pass in super().__init__()
        kwargs.update(inputs)
        super(JavaConnectionOptionsCommon, self).__init__(**kwargs)

class JavaSenderReceiverCommand(JavaConnectionOptionsCommon, ControlOptionsCommon, LoggingOptionsCommon):

    def __init__(
        self,
        broker: str = '127.0.0.1:5672',
        address: str = 'examples',
        count: int = 1,
        timeout: 'Optional[int]' = None,
        sync_mode: 'Optional[str]' = None,
        close_sleep: 'Optional[int]' = None,
        duration: 'Optional[int]' = None,
        duration_mode: 'Optional[str]' = None,
        capacity: 'Optional[int]' = None,
        log_lib: 'Optional[str]' = None,
        log_stats: 'Optional[str]' = None,
        conn_auth_mechanisms: 'Optional[str]' = None,
        conn_username: 'Optional[str]' = None,
        conn_password: 'Optional[str]' = None,
        conn_ssl_keystore_location: 'Optional[str]' = None,
        conn_ssl_keystore_password: 'Optional[str]' = None,
        conn_ssl_key_alias: 'Optional[str]' = None,
        conn_ssl_trust_all: 'Optional[str]' = None,
        conn_ssl_verify_host: 'Optional[str]' = None,
        urls: 'Optional[str]' = None,
        reconnect: bool = False,
        reconnect_interval: 'Optional[int]' = None,
        reconnect_limit: 'Optional[int]' = None,
        reconnect_timeout: 'Optional[int]' = None,
        heartbeat: 'Optional[int]' = None,
        max_frame_size: 'Optional[int]' = None,
        **kwargs
    ) -> None:
        # No timeout on java client is -1
        if timeout is None:
            self.timeout = -1

        # dump arguments into dictionary
        inputs = locals()
        # remove self and kwargs variables as they would mess things up
        del inputs['self']
        del inputs['kwargs']
        # update kwargs to pass in super().__init__()
        kwargs.update(inputs)
        super(JavaConnectionOptionsCommon, self).__init__(**kwargs)