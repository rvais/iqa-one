"""
Specialized options for external Python Proton client commands (cli-proton-python).
"""
from typing import TYPE_CHECKING

from optconstruct.types import Prefixed

if TYPE_CHECKING:
    from typing import Optional, Union, List
    from optconstruct.types import Toggle, KWOption, ListOption

from iqa.components.implementations.clients.external.command.options.client_options import (
    ControlOptionsCommon,
    ControlOptionsSenderReceiver,
    ControlOptionsReceiver,
    ConnectionOptionsCommon,
)


class PythonControlOptionsCommon(ControlOptionsCommon):
    """
    Specialized implementation of control options for python client commands.
    """

    def __init__(
        self,
        broker_url: str = '127.0.0.1:5672',
        count: int = 1,
        timeout: 'Optional[int]' = None,
        sync_mode: 'Optional[str]' = None,
        close_sleep: 'Optional[int]' = None,
    ) -> None:
        super(PythonControlOptionsCommon, self).__init__(
            count, timeout, sync_mode, close_sleep
        )
        self.broker_url: str = broker_url

    def valid_options(self) -> 'List[Union[Toggle, Prefixed, KWOption, ListOption]]':
        return ControlOptionsCommon.valid_options(self) + [
            Prefixed('broker-url', '--broker-url')
        ]


class PythonControlOptionsSenderReceiver(
    ControlOptionsSenderReceiver, PythonControlOptionsCommon
):
    """
    Specialized implementation of control options for Sender and Receiver Python client commands.
    """

    def __init__(
        self,
        broker_url: str = '127.0.0.1:5672/examples',
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
        PythonControlOptionsCommon.__init__(
            self,
            broker_url=broker_url,
            count=count,
            timeout=timeout,
            sync_mode=sync_mode,
            close_sleep=close_sleep,
        )


class PythonControlOptionsReceiver(
    ControlOptionsReceiver, PythonControlOptionsSenderReceiver
):
    """
    Specialized implementation of control options for Receiver Python client command.
    """

    def __init__(
        self,
        broker_url: str = '127.0.0.1:5672/examples',
        count: int = 1,
        timeout: 'Optional[int]' = None,
        sync_mode: 'Optional[str]' = None,
        duration: 'Optional[int]' = None,
        duration_mode: 'Optional[str]' = None,
        capacity: 'Optional[int]' = None,
        dynamic: bool = False,
    ) -> None:
        ControlOptionsReceiver.__init__(self, dynamic=dynamic)
        PythonControlOptionsSenderReceiver.__init__(
            self,
            broker_url=broker_url,
            count=count,
            timeout=timeout,
            sync_mode=sync_mode,
            duration=duration,
            duration_mode=duration_mode,
            capacity=capacity,
        )


class PythonConnectionOptionsCommon(ConnectionOptionsCommon):
    def __init__(
        self,
        conn_allowed_mechs: 'Optional[str]' = None,
        conn_ssl_certificate: 'Optional[str]' = None,
        conn_ssl_private_key: 'Optional[str]' = None,
        urls: 'Optional[str]' = None,
        reconnect: 'Optional[bool]' = None,
        reconnect_interval: 'Optional[int]' = None,
        reconnect_limit: 'Optional[int]' = None,
        reconnect_timeout: 'Optional[int]' = None,
        heartbeat: 'Optional[int]' = None,
        max_frame_size: 'Optional[int]' = None,
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
        self.conn_allowed_mechs: Optional[str] = conn_allowed_mechs
        self.conn_ssl_certificate: Optional[str] = conn_ssl_certificate
        self.conn_ssl_private_key: Optional[str] = conn_ssl_private_key

    def valid_options(self) -> 'List[Union[Toggle, Prefixed, KWOption, ListOption]]':
        return ConnectionOptionsCommon.valid_options(self) + [
            Prefixed('conn-allowed-mechs', '--conn-allowed-mechs'),
            Prefixed('conn-ssl-certificate', '--conn-ssl-certificate'),
            Prefixed('conn-ssl-private-key', '--conn-ssl-private-key'),
        ]
