"""
Specialized options for external Node JS client commands (cli-rhea).
"""
from optconstruct.types import Prefixed, Toggle

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from typing import Optional, Union, List
    from optconstruct.types import KWOption, ListOption

from iqa.components.implementations.clients.external.command.options.client_options import (
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
        timeout: 'Optional[int]' = None,
        sync_mode: 'Optional[str]' = None,
        close_sleep: 'Optional[int]' = None,
    ) -> None:
        super(NodeJSControlOptionsCommon, self).__init__(
            count, timeout, sync_mode, close_sleep
        )
        self.broker: str = broker

    def valid_options(self) -> 'List[Union[Toggle, Prefixed, KWOption, ListOption]]':
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
        timeout: 'Optional[int]' = None,
        sync_mode: 'Optional[str]' = None,
        close_sleep: 'Optional[int]' = None,
        duration: 'Optional[int]' = None,
        duration_mode: 'Optional[str]' = None,
        capacity: 'Optional[int]' = None,
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

    def valid_options(self) -> 'List[Union[Toggle, Prefixed, KWOption, ListOption]]':
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
        timeout: 'Optional[int]' = None,
        sync_mode: 'Optional[str]' = None,
        close_sleep: 'Optional[int]' = None,
        duration: 'Optional[int]' = None,
        duration_mode: 'Optional[str]' = None,
        capacity: 'Optional[int]' = None,
        on_release: str = 'retry'
    ) -> None:
        NodeJSControlOptionsSenderReceiver.__init__(
            self,
            broker=broker,
            address=address,
            count=count,
            timeout=timeout,
            sync_mode=sync_mode,
            close_sleep=close_sleep,
            duration=duration,
            duration_mode=duration_mode,
            capacity=capacity,
        )
        self.on_release: str = on_release

    def valid_options(self) -> 'List[Union[Toggle, Prefixed, KWOption, ListOption]]':
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
        timeout: 'Optional[int]' = None,
        sync_mode: 'Optional[str]' = None,
        duration: 'Optional[int]' = None,
        duration_mode: 'Optional[str]' = None,
        capacity: 'Optional[int]' = None,
        dynamic: 'Optional[bool]' = False
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
        conn_ssl: 'Optional[bool]' = None,
        conn_ssl_certificate: 'Optional[str]' = None,
        conn_ssl_private_key: 'Optional[str]' = None,
        conn_ws: 'Optional[bool]' = None,
        conn_ws_protocols: 'Optional[str]' = None,
        urls: 'Optional[str]' = None,
        reconnect: 'Optional[bool]' = None,
        reconnect_interval: 'Optional[int]' = None,
        reconnect_limit: 'Optional[int]' = None,
        reconnect_timeout: 'Optional[int]' = None,
        heartbeat: 'Optional[int]' = None,
        max_frame_size: 'Optional[int]' = None
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

    def valid_options(self) -> 'List[Union[Toggle, Prefixed, KWOption, ListOption]]':
        return ConnectionOptionsCommon.valid_options(self) + [
            Toggle('conn-ssl', '--conn-ssl'),
            Prefixed('conn-ssl-certificate', '--conn-ssl-certificate'),
            Prefixed('conn-ssl-private-key', '--conn-ssl-private-key'),
            Toggle('conn-ws', '--conn-ws'),
            Prefixed('conn-ws-protocols', '--conn-ws-protocols'),
        ]
