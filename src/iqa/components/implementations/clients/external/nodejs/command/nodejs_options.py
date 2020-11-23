"""
Specialized options for external Node JS client commands (cli-rhea).
"""
from typing import Optional

from optconstruct.types import Prefixed, Toggle

from iqa.components.clients.external.command.options.client_options import (
    ControlOptionsCommon,
    ControlOptionsSenderReceiver,
    ControlOptionsReceiver,
    ConnectionOptionsCommon,
)


class NodeJSControlOptionsCommon(ControlOptionsCommon):
    """
    Specialized implementation of control options for cli-rhea client commands.
    """

    def __init__(
        self,
        broker: str = 'localhost:5672',
        count: int = 1,
        timeout: int = None,
        sync_mode: str = None,
        close_sleep: int = None,
    ) -> None:
        super(NodeJSControlOptionsCommon, self).__init__(
            count, timeout, sync_mode, close_sleep
        )
        self.broker: str = broker

    def valid_options(self) -> list:
        return super(NodeJSControlOptionsCommon, self).valid_options() + [
            Prefixed('broker', '--broker')
        ]


class NodeJSControlOptionsSenderReceiver(
    ControlOptionsSenderReceiver, NodeJSControlOptionsCommon
):
    """
    Specialized implementation of control options for cli-rhea Sender and Receiver client commands.
    """

    def __init__(
        self,
        broker: str = 'localhost:5672',
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
        NodeJSControlOptionsCommon.__init__(
            self,
            broker=broker,
            count=count,
            timeout=timeout,
            sync_mode=sync_mode,
            close_sleep=close_sleep,
        )
        self.address: str = address

    def valid_options(self) -> list:
        return NodeJSControlOptionsCommon.valid_options(self) + [
            Prefixed('address', '--address')
        ]


class NodeJSControlOptionsSender(NodeJSControlOptionsSenderReceiver):
    """
    Specialized implementation of control options for cli-rhea Sender and Receiver client commands.
    """

    def __init__(
        self,
        broker: str = 'localhost:5672',
        address: str = 'examples',
        count: int = 1,
        timeout: int = None,
        sync_mode: str = None,
        close_sleep: int = None,
        duration: int = None,
        duration_mode: str = None,
        capacity: int = None,
        on_release: str = 'retry',
    ) -> None:
        NodeJSControlOptionsSenderReceiver.__init__(
            self,
            broker=broker,
            count=count,
            timeout=timeout,
            sync_mode=sync_mode,
            duration=duration,
            duration_mode=duration_mode,
            capacity=capacity,
        )
        self.on_release: str = on_release

    def valid_options(self) -> list:
        return NodeJSControlOptionsSenderReceiver.valid_options(self) + [
            Prefixed('on-release', '--on-release')
        ]


class NodeJSControlOptionsReceiver(
    ControlOptionsReceiver, NodeJSControlOptionsSenderReceiver
):
    """
    Specialized implementation of control options for cli-rhea Receiver client command.
    """

    def __init__(
        self,
        broker: str = 'localhost:5672/examples',
        count: int = 1,
        timeout: int = None,
        sync_mode: str = None,
        duration: int = None,
        duration_mode: str = None,
        capacity: int = None,
        dynamic: bool = False,
    ) -> None:
        ControlOptionsReceiver.__init__(self, dynamic=dynamic)
        NodeJSControlOptionsSenderReceiver.__init__(
            self,
            broker=broker,
            count=count,
            timeout=timeout,
            sync_mode=sync_mode,
            duration=duration,
            duration_mode=duration_mode,
            capacity=capacity,
        )


class NodeJSConnectionOptionsCommon(ConnectionOptionsCommon):
    def __init__(
        self,
        conn_ssl: bool = None,
        conn_ssl_certificate: str = None,
        conn_ssl_private_key: str = None,
        conn_ws: bool = None,
        conn_ws_protocols: str = None,
        urls: str = None,
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
        self.conn_ssl: Optional[bool] = conn_ssl
        self.conn_ssl_certificate: Optional[str] = conn_ssl_certificate
        self.conn_ssl_private_key: Optional[str] = conn_ssl_private_key
        self.conn_ws: Optional[bool] = conn_ws
        self.conn_ws_protocols: Optional[str] = conn_ws_protocols

    def valid_options(self) -> list:
        return ConnectionOptionsCommon.valid_options(self) + [
            Toggle('conn-ssl', '--conn-ssl'),
            Prefixed('conn-ssl-certificate', '--conn-ssl-certificate'),
            Prefixed('conn-ssl-private-key', '--conn-ssl-private-key'),
            Toggle('conn-ws', '--conn-ws'),
            Prefixed('conn-ws-protocols', '--conn-ws-protocols'),
        ]
