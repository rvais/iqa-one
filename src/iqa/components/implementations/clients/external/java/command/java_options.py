from typing import Optional

from optconstruct.types import Prefixed

from iqa.components.clients.external.command.options.client_options import (
    ControlOptionsCommon,
    ControlOptionsSenderReceiver,
    ControlOptionsReceiver,
    ConnectionOptionsCommon,
)

"""
Specialized options for external Java client commands (cli-qpid.jar).
"""


class JavaControlOptionsCommon(ControlOptionsCommon):
    """
    Specialized implementation of control options for java client commands.
    """

    def __init__(
        self,
        broker: str = '127.0.0.1:5672',
        count: int = 1,
        timeout: int = None,
        sync_mode: str = None,
        close_sleep: int = None,
    ) -> None:
        super(JavaControlOptionsCommon, self).__init__(
            count, timeout, sync_mode, close_sleep
        )
        self.broker: str = broker
        # No timeout on java client is -1
        if timeout is None:
            self.timeout = -1

    def valid_options(self) -> list:
        return ControlOptionsCommon.valid_options(self) + [
            Prefixed('broker', '--broker')
        ]


class JavaControlOptionsSenderReceiver(
    ControlOptionsSenderReceiver, JavaControlOptionsCommon
):
    """
    Specialized implementation of control options for Sender and Receiver Java client commands.
    """

    def __init__(
        self,
        broker: str = '127.0.0.1:5672',
        address: str = 'examples',
        count: int = 1,
        timeout: int = None,
        sync_mode: str = None,
        close_sleep: int = None,
        duration: int = None,
        duration_mode: str = None,
        capacity: int = None,
    ) -> None:
        ControlOptionsSenderReceiver.__init__(
            self, duration=duration, duration_mode=duration_mode, capacity=capacity
        )
        JavaControlOptionsCommon.__init__(
            self,
            broker=broker,
            count=count,
            timeout=timeout,
            sync_mode=sync_mode,
            close_sleep=close_sleep,
        )
        self.address: str = address

    def valid_options(self) -> list:
        return JavaControlOptionsCommon.valid_options(self) + [
            Prefixed('address', '--address')
        ]


class JavaControlOptionsReceiver(
    ControlOptionsReceiver, JavaControlOptionsSenderReceiver
):
    """
    Specialized implementation of control options for Receiver Java client command.
    """

    def __init__(
        self,
        broker: str = '127.0.0.1:5672',
        address: str = 'examples',
        count: int = 1,
        timeout: int = None,
        sync_mode: str = None,
        duration: int = None,
        duration_mode: str = None,
        capacity: int = None,
        dynamic: bool = False,
    ) -> None:
        ControlOptionsReceiver.__init__(self, dynamic=dynamic)
        JavaControlOptionsSenderReceiver.__init__(
            self,
            broker=broker,
            address=address,
            count=count,
            timeout=timeout,
            sync_mode=sync_mode,
            duration=duration,
            duration_mode=duration_mode,
            capacity=capacity,
        )

    def valid_options(self) -> list:
        return JavaControlOptionsSenderReceiver.valid_options(self)


class JavaConnectionOptionsCommon(ConnectionOptionsCommon):
    def __init__(
        self,
        conn_auth_mechanisms: Optional[str] = None,
        conn_username: Optional[str] = None,
        conn_password: Optional[str] = None,
        conn_ssl_keystore_location: Optional[str] = None,
        conn_ssl_keystore_password: Optional[str] = None,
        conn_ssl_key_alias: Optional[str] = None,
        conn_ssl_trust_all: Optional[str] = None,
        conn_ssl_verify_host: Optional[str] = None,
        urls: Optional[str] = None,
        reconnect: bool = None,
        reconnect_interval: int = None,
        reconnect_limit: int = None,
        reconnect_timeout: int = None,
        heartbeat: int = None,
        max_frame_size: int = None,
    ) -> None:
        ConnectionOptionsCommon.__init__(
            self,
            urls=urls,
            reconnect=reconnect,
            reconnect_interval=reconnect_interval,
            reconnect_limit=reconnect_limit,
            reconnect_timeout=reconnect_timeout,
            heartbeat=heartbeat,
            max_frame_size=max_frame_size,
        )
        self.conn_auth_mechanisms: Optional[str] = conn_auth_mechanisms
        self.conn_username: Optional[str] = conn_username
        self.conn_password: Optional[str] = conn_password
        self.conn_ssl_keystore_location: Optional[str] = conn_ssl_keystore_location
        self.conn_ssl_keystore_password: Optional[str] = conn_ssl_keystore_password
        self.conn_ssl_key_alias: Optional[str] = conn_ssl_key_alias
        self.conn_ssl_trust_all: Optional[str] = conn_ssl_trust_all
        self.conn_ssl_verify_host: Optional[str] = conn_ssl_verify_host

    def valid_options(self) -> list:
        return ConnectionOptionsCommon.valid_options(self) + [
            Prefixed('conn-auth-mechanisms', '--conn-auth-mechanisms'),
            Prefixed('conn-username', '--conn-username'),
            Prefixed('conn-password', '--conn-password'),
            Prefixed('conn-ssl-keystore-location', '--conn-ssl-keystore-location'),
            Prefixed('conn-ssl-keystore-password', '--conn-ssl-keystore-password'),
            Prefixed('conn-ssl-key-alias', '--conn-ssl-key-alias'),
            Prefixed('conn-ssl-trust-all', '--conn-ssl-trust-all'),
            Prefixed('conn-ssl-verify-host', '--conn-ssl-verify-host'),
        ]
