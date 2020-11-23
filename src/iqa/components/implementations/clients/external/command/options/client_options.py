from typing import Optional

from optconstruct.types import Toggle, Prefixed, KWOption, ListOption

from iqa.abstract.message.application_data import ApplicationData

"""
This modules defines all supported command line options for external
abstract clients, with specialized classes for sender and receivers.
Each implementation of ClientOptionsBase must provide a list of
OptionAbstract (optconstruct) that is supported.
"""


class ClientOptionsBase(object):
    """
    Base abstraction for options (arguments) that can be used
    in an external client command.
    """

    def valid_options(self) -> list:
        """
        Delegated method that must return a list of all valid
        options allowed by the client command.
        List must be composed of OptionAbstract objects.
        :return:
        """
        raise NotImplementedError

    @staticmethod
    def option_mapper() -> dict:
        """
        Allows a specific argument to have a different name
        depending on concrete implementation.
        :return:
        """
        return {}

    def to_dict(self) -> dict:
        """
        Generate a dict with all internal items, replacing
        underscores with dashes, example: a broker_url property
        becomes 'broker-url'.
        It also allows internal property to be renamed to something else,
        like: { 'property_xyz': 'property_abc' } (see: option_mapper()).
        :return:
        """
        nd: dict = {}
        for (k, v) in self.__dict__.items():
            rk = k
            if k in self.option_mapper():
                rk = self.option_mapper()[k]
            nd['%s' % rk.replace('_', '-')] = v
        return nd


class ControlOptionsCommon(ClientOptionsBase):
    """
    Common control options for all clients.
    """

    def __init__(
        self,
        count: Optional[int] = 1,
        timeout: Optional[int] = None,
        sync_mode: Optional[str] = None,
        close_sleep: Optional[int] = None,
    ) -> None:
        self.count: Optional[int] = count
        self.timeout: Optional[int] = timeout
        self.sync_mode: Optional[str] = sync_mode
        self.close_sleep: Optional[int] = close_sleep

    def valid_options(self) -> list:
        return [
            Prefixed('count', '--count'),
            Prefixed('timeout', '--timeout'),
            Prefixed('sync-mode', '--sync-mode'),
            Prefixed('close-sleep', '--close-sleep'),
        ]


class ControlOptionsSenderReceiver(ControlOptionsCommon):
    """
    Common control options for all Sender and Receiver commands.
    """

    def __init__(
        self,
        count: int = 1,
        timeout: int = None,
        sync_mode: str = None,
        close_sleep: int = None,
        duration: Optional[int] = None,
        duration_mode: Optional[str] = None,
        capacity: Optional[int] = None,
    ) -> None:
        super(ControlOptionsSenderReceiver, self).__init__(
            count, timeout, sync_mode, close_sleep
        )
        self.duration: Optional[int] = duration
        self.duration_mode: Optional[str] = duration_mode
        self.capacity: Optional[int] = capacity

    def valid_options(self) -> list:
        return super(ControlOptionsSenderReceiver, self).valid_options() + [
            Prefixed('duration', '--duration'),
            Prefixed('duration-mode', '--duration-mode'),
            Prefixed('capacity', '--capacity'),
        ]


class ControlOptionsReceiver(ControlOptionsSenderReceiver):
    """
    Common control options for all Receiver commands.
    """

    def __init__(
        self,
        count: int = 1,
        timeout: int = None,
        sync_mode: str = None,
        close_sleep: int = None,
        duration: int = None,
        duration_mode: str = None,
        capacity: int = None,
        dynamic: bool = False,
    ) -> None:
        super(ControlOptionsReceiver, self).__init__(
            count, timeout, sync_mode, close_sleep, duration, duration_mode, capacity
        )
        self.dynamic: bool = dynamic

    def valid_options(self) -> list:
        return super(ControlOptionsReceiver, self).valid_options()


class LoggingOptionsCommon(ClientOptionsBase):
    """
    Common logging options for all external client commands
    """

    def __init__(self, log_lib: str = None, log_stats: str = None) -> None:
        self.log_lib: Optional[str] = log_lib
        self.log_stats: Optional[str] = log_stats

    def valid_options(self) -> list:
        return [Prefixed('log-lib', '--log-lib'), Prefixed('log-stats', '--log-stats')]


class LoggingOptionsSenderReceiver(LoggingOptionsCommon):
    """
    Common logging options for all Sender and Receiver client commands
    """

    def __init__(
        self, log_lib: str = None, log_stats: str = None, logs_msgs: str = None
    ) -> None:
        super(LoggingOptionsSenderReceiver, self).__init__(log_lib, log_stats)
        self.log_msgs: Optional[str] = logs_msgs

    def valid_options(self) -> list:
        return super(LoggingOptionsSenderReceiver, self).valid_options() + [
            Prefixed('log-msgs', '--log-msgs')
        ]


class TransactionOptionsSenderReceiver(ClientOptionsBase):
    """
    Common transaction options for all Sender and Receiver client commands
    """

    def __init__(
        self, tx_size: int = None, tx_action: str = None, tx_endloop_action: str = None
    ) -> None:
        self.tx_size: Optional[int] = tx_size
        self.tx_action: Optional[str] = tx_action
        self.tx_endloop_action: Optional[str] = tx_endloop_action

    def valid_options(self) -> list:
        return [
            Prefixed('tx-size', '--tx-size'),
            Prefixed('tx-action', '--tx-action'),
            Prefixed('tx-endloop-action', '--tx-endloop-action'),
        ]


class ConnectionOptionsCommon(ClientOptionsBase):
    """
    Common connection options for all client commands
    """

    def __init__(
        self,
        urls: str = None,
        reconnect: bool = None,
        reconnect_interval: int = None,
        reconnect_limit: int = None,
        reconnect_timeout: int = None,
        heartbeat: int = None,
        max_frame_size: int = None,
    ) -> None:
        self.conn_urls: Optional[str] = urls
        self.conn_reconnect: Optional[bool] = reconnect
        self.conn_reconnect_interval: Optional[int] = reconnect_interval
        self.conn_reconnect_limit: Optional[int] = reconnect_limit
        self.conn_reconnect_timeout: Optional[int] = reconnect_timeout
        self.conn_heartbeat: Optional[int] = heartbeat
        self.conn_max_frame_size: Optional[int] = max_frame_size

    def valid_options(self) -> list:
        return [
            Prefixed('conn-urls', '--conn-urls'),
            Prefixed('conn-reconnect', '--conn-reconnect'),
            Prefixed('conn-reconnect-interval', '--conn-reconnect-interval'),
            Prefixed('conn-reconnect-limit', '--conn-reconnect-limit'),
            Prefixed('conn-reconnect-timeout', '--conn-reconnect-timeout'),
            Prefixed('conn-heartbeat', '--conn-heartbeat'),
            Prefixed('conn-max-frame-size', '--conn-max-frame-size'),
        ]


class ConnectorOptions(ClientOptionsBase):
    """
    Common options for connector client commands
    """

    def __init__(self, obj_ctrl: Optional[str] = None) -> None:
        self.obj_ctrl: Optional[str] = obj_ctrl

    def valid_options(self) -> list:
        return [Prefixed('obj-ctrl', '--obj-ctrl')]


class LinkOptionsSenderReceiver(ClientOptionsBase):
    """
    Common Link Options for all Sender and Receiver client commands
    """

    def __init__(
        self,
        link_durable: bool = False,
        link_at_least_once: bool = False,
        link_at_most_once: bool = False,
    ) -> None:
        self.link_durable: bool = link_durable
        self.link_at_least_once: bool = link_at_least_once
        self.link_at_most_once: bool = link_at_most_once

    def valid_options(self) -> list:
        return [
            Toggle('link-durable', '--link-durable'),
            Toggle('link-at-least-once', '--link-at-least-once'),
            Toggle('link-at-most-once', '--link-at-most-once'),
        ]


class LinkOptionsReceiver(LinkOptionsSenderReceiver):
    """
    Common Link Options for all Receiver client commands
    """

    def __init__(
        self,
        link_durable: bool = False,
        link_at_least_once: bool = False,
        link_at_most_once: bool = False,
        link_dynamic_node_properties: str = None,
    ) -> None:
        super(LinkOptionsReceiver, self).__init__(
            link_durable, link_at_least_once, link_at_most_once
        )
        self.link_dynamic_node_properties = link_dynamic_node_properties

    def valid_options(self) -> list:
        return super(LinkOptionsReceiver, self).valid_options() + [
            Prefixed('link-dynamic-node-properties', '--link-dynamic-node-properties')
        ]


class MessageOptionsSender(ClientOptionsBase):
    """
    Common options for all Sender client commands
    """

    def __init__(
        self,
        msg_id: Optional[str] = None,
        msg_subject: Optional[str] = None,
        msg_address: Optional[str] = None,
        msg_reply_to: Optional[str] = None,
        msg_durable: Optional[str] = None,
        msg_ttl: Optional[int] = None,
        msg_priority: Optional[str] = None,
        msg_correlation_id: Optional[str] = None,
        msg_user_id: Optional[str] = None,
        msg_group_id: Optional[str] = None,
        msg_group_seq: Optional[str] = None,
        msg_property: Optional[str] = None,
        msg_content_map_item: Optional[str] = None,
        msg_content_list_item: Optional[str] = None,
        msg_content_from_file: Optional[str] = None,
        msg_content: Optional[ApplicationData] = None,
        msg_content_type: Optional[str] = None,
        content_type: Optional[str] = None,
    ) -> None:
        self.msg_id: Optional[str] = msg_id
        self.msg_subject: Optional[str] = msg_subject
        self.msg_address: Optional[str] = msg_address
        self.msg_reply_to: Optional[str] = msg_reply_to
        self.msg_durable: Optional[str] = msg_durable
        self.msg_ttl: Optional[int] = msg_ttl
        self.msg_priority: Optional[str] = msg_priority
        self.msg_correlation_id: Optional[str] = msg_correlation_id
        self.msg_user_id: Optional[str] = msg_user_id
        self.msg_group_id: Optional[str] = msg_group_id
        self.msg_group_seq: Optional[str] = msg_group_seq
        self.msg_property: Optional[str] = msg_property
        self.msg_content_map_item: Optional[str] = msg_content_map_item
        self.msg_content_list_item: Optional[str] = msg_content_list_item
        self.msg_content_from_file: Optional[str] = msg_content_from_file
        self.msg_content: Optional[ApplicationData] = msg_content
        self.msg_content_type: Optional[str] = msg_content_type
        self.content_type: Optional[str] = content_type

    def valid_options(self) -> list:
        return [
            Prefixed('msg-id', '--msg-id'),
            Prefixed('msg-subject', '--msg-subject'),
            Prefixed('msg-reply-to', '--msg-reply-to'),
            Prefixed('msg-durable', '--msg-durable'),
            Prefixed('msg-ttl', '--msg-ttl'),
            Prefixed('msg-priority', '--msg-priority'),
            Prefixed('msg-correlation-id', '--msg-correlation-id'),
            Prefixed('msg-user-id', '--msg-user-id'),
            Prefixed('msg-group-id', '--msg-group-id'),
            KWOption('msg-property', '--msg-property'),
            KWOption('msg-content-map-item', '--msg-content-map-item'),
            ListOption('msg-content-list-item', '--msg-content-list-item'),
            Prefixed('msg-content-from-file', '--msg-content-from-file'),
            Prefixed('msg-content', '--msg-content'),
            Prefixed('msg-content-type', '--msg-content-type'),
            Prefixed('content-type', '--content-type'),
        ]


class ReceiverOptions(ClientOptionsBase):
    """
    Common client options for all Receiver client commands
    """

    def __init__(
        self,
        process_reply_to: Optional[str] = None,
        action: Optional[str] = None,
        recv_browse: Optional[bool] = None,
    ) -> None:
        self.process_reply_to: Optional[str] = process_reply_to
        self.action: Optional[str] = action
        self.recv_browse: Optional[bool] = recv_browse

    def valid_options(self) -> list:
        return [
            Prefixed('process-reply-to', '--process-reply-to'),
            Prefixed('action', '--action'),
            Toggle('recv-browse', '--recv-browse'),
        ]


class ReactorOptionsSenderReceiver(ClientOptionsBase):
    """
    Common reactor options for all Sender and Receiver client commands
    """

    def __init__(self, reactor_auto_settle_off: Optional[bool] = None) -> None:
        self.reactor_auto_settle_off: Optional[bool] = reactor_auto_settle_off

    def valid_options(self) -> list:
        return [Toggle('reactor-auto-settle-off', '--reactor-auto-settle-off')]
