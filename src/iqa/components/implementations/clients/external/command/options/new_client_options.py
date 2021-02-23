from typing import TYPE_CHECKING

from iqa.system.command.command_options import OptionsBase
from optconstruct.types import Toggle, Prefixed, KWOption, ListOption
from iqa.abstract.message.application_data import ApplicationData

if TYPE_CHECKING:
    from typing import Optional, Union, List


class ControlOptionsCommon(OptionsBase):
    """
    Common control options for all clients.
    """

    def __init__(
        self,
        count: 'Optional[int]' = 1,
        timeout: 'Optional[int]' = None,
        sync_mode: 'Optional[str]' = None,
        close_sleep: 'Optional[int]' = None,
        **kwargs
    ) -> None:
        # dump arguments into dictionary
        inputs = locals()
        # remove self and kwargs variables as they would mess things up
        del inputs['self']
        del inputs['kwargs']
        # update kwargs to pass in super().__init__()
        kwargs.update(inputs)
        super(ControlOptionsCommon, self).__init__(**kwargs)

    @staticmethod
    def valid_options() -> 'List[Union[Toggle, Prefixed, KWOption, ListOption]]':
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
        timeout: 'Optional[int]' = None,
        sync_mode: 'Optional[str]' = None,
        close_sleep: 'Optional[int]' = None,
        duration: 'Optional[int]' = None,
        duration_mode: 'Optional[str]' = None,
        capacity: 'Optional[int]' = None,
        **kwargs
    ) -> None:
        # dump arguments into dictionary
        inputs = locals()
        # remove self and kwargs variables as they would mess things up
        del inputs['self']
        del inputs['kwargs']
        # update kwargs to pass in super().__init__()
        kwargs.update(inputs)
        super(ControlOptionsSenderReceiver, self).__init__(**kwargs)

    @staticmethod
    def valid_options() -> 'List[Union[Toggle, Prefixed, KWOption, ListOption]]':
        return [
            Prefixed('duration', '--duration'),
            Prefixed('duration-mode', '--duration-mode'),
            Prefixed('capacity', '--capacity'),
        ]


class LoggingOptionsCommon(OptionsBase):
    """
    Common logging options for all external client commands
    """

    def __init__(
        self,
        log_lib: 'Optional[str]' = None,
        log_stats: 'Optional[str]' = None,
        **kwargs
    ) -> None:
        # dump arguments into dictionary
        inputs = locals()
        # remove self and kwargs variables as they would mess things up
        del inputs['self']
        del inputs['kwargs']
        # update kwargs to pass in super().__init__()
        kwargs.update(inputs)
        super(LoggingOptionsCommon, self).__init__(**kwargs)

    @staticmethod
    def valid_options() -> 'List[Union[Toggle, Prefixed, KWOption, ListOption]]':
        return [Prefixed('log-lib', '--log-lib'), Prefixed('log-stats', '--log-stats')]


class LoggingOptionsSenderReceiver(LoggingOptionsCommon):
    """
    Common logging options for all Sender and Receiver client commands
    """

    def __init__(
        self,
        log_lib: 'Optional[str]' = None,
        log_stats: 'Optional[str]' = None,
        logs_msgs: 'Optional[str]' = None,
        **kwargs
    ) -> None:
        # dump arguments into dictionary
        inputs = locals()
        # remove self and kwargs variables as they would mess things up
        del inputs['self']
        del inputs['kwargs']
        # update kwargs to pass in super().__init__()
        kwargs.update(inputs)
        super(LoggingOptionsSenderReceiver, self).__init__(**kwargs)

    @staticmethod
    def valid_options() -> 'List[Union[Toggle, Prefixed, KWOption, ListOption]]':
        return [
            Prefixed('log-msgs', '--log-msgs')
        ]


class TransactionOptionsSenderReceiver(OptionsBase):
    """
    Common transaction options for all Sender and Receiver client commands
    """

    def __init__(
        self,
        tx_size: 'Optional[int]' = None,
        tx_action: 'Optional[str]' = None,
        tx_endloop_action: 'Optional[str]' = None,
        **kwargs
    ) -> None:
        # dump arguments into dictionary
        inputs = locals()
        # remove self and kwargs variables as they would mess things up
        del inputs['self']
        del inputs['kwargs']
        # update kwargs to pass in super().__init__()
        kwargs.update(inputs)
        super(TransactionOptionsSenderReceiver, self).__init__(**kwargs)

    @staticmethod
    def valid_options() -> 'List[Union[Toggle, Prefixed, KWOption, ListOption]]':
        return [
            Prefixed('tx-size', '--tx-size'),
            Prefixed('tx-action', '--tx-action'),
            Prefixed('tx-endloop-action', '--tx-endloop-action'),
        ]


class ConnectionOptionsCommon(OptionsBase):
    """
    Common connection options for all client commands
    """

    def __init__(
        self,
        urls: 'Optional[str]' = None,
        reconnect: 'Optional[bool]' = None,
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
        super(ConnectionOptionsCommon, self).__init__(**kwargs)

    @staticmethod
    def valid_options() -> 'List[Union[Toggle, Prefixed, KWOption, ListOption]]':
        return [
            Prefixed('conn-urls', '--conn-urls'),
            Prefixed('conn-reconnect', '--conn-reconnect'),
            Prefixed('conn-reconnect-interval', '--conn-reconnect-interval'),
            Prefixed('conn-reconnect-limit', '--conn-reconnect-limit'),
            Prefixed('conn-reconnect-timeout', '--conn-reconnect-timeout'),
            Prefixed('conn-heartbeat', '--conn-heartbeat'),
            Prefixed('conn-max-frame-size', '--conn-max-frame-size'),
        ]


class ConnectorOptions(OptionsBase):
    """
    Common options for connector client commands
    """

    def __init__(
        self,
        obj_ctrl: 'Optional[str]' = None,
        **kwargs
    ) -> None:
        # dump arguments into dictionary
        inputs = locals()
        # remove self and kwargs variables as they would mess things up
        del inputs['self']
        del inputs['kwargs']
        # update kwargs to pass in super().__init__()
        kwargs.update(inputs)
        super(ConnectorOptions, self).__init__(**kwargs)

    @staticmethod
    def valid_options() -> 'List[Union[Toggle, Prefixed, KWOption, ListOption]]':
        return [Prefixed('obj-ctrl', '--obj-ctrl')]


class LinkOptionsSenderReceiver(OptionsBase):
    """
    Common Link Options for all Sender and Receiver client commands
    """

    def __init__(
        self,
        link_durable: bool = False,
        link_at_least_once: bool = False,
        link_at_most_once: bool = False,
        **kwargs
    ) -> None:
        # dump arguments into dictionary
        inputs = locals()
        # remove self and kwargs variables as they would mess things up
        del inputs['self']
        del inputs['kwargs']
        # update kwargs to pass in super().__init__()
        kwargs.update(inputs)
        super(LinkOptionsSenderReceiver, self).__init__(**kwargs)

    @staticmethod
    def valid_options() -> 'List[Union[Toggle, Prefixed, KWOption, ListOption]]':
        return [
            Toggle('link-durable', '--link-durable'),
            Toggle('link-at-least-once', '--link-at-least-once'),
            Toggle('link-at-most-once', '--link-at-most-once'),
        ]


class LinkOptionsReceiverSpecific(LinkOptionsSenderReceiver):
    """
    Common Link Options for all Receiver client commands
    """

    def __init__(
        self,
        link_durable: bool = False,
        link_at_least_once: bool = False,
        link_at_most_once: bool = False,
        link_dynamic_node_properties: 'Optional[str]' = None,
        **kwargs
    ) -> None:
        # dump arguments into dictionary
        inputs = locals()
        # remove self and kwargs variables as they would mess things up
        del inputs['self']
        del inputs['kwargs']
        # update kwargs to pass in super().__init__()
        kwargs.update(inputs)
        super(LinkOptionsReceiverSpecific, self).__init__(**kwargs)

    @staticmethod
    def valid_options() -> 'List[Union[Toggle, Prefixed, KWOption, ListOption]]':
        return [
            Prefixed('link-dynamic-node-properties', '--link-dynamic-node-properties')
        ]


class MessageOptionsSender(OptionsBase):
    """
    Common options for all Sender client commands
    """

    def __init__(
        self,
        msg_id: 'Optional[str]' = None,
        msg_subject: 'Optional[str]' = None,
        msg_address: 'Optional[str]' = None,
        msg_reply_to: 'Optional[str]' = None,
        msg_durable: 'Optional[str]' = None,
        msg_ttl: 'Optional[int]' = None,
        msg_priority: 'Optional[str]' = None,
        msg_correlation_id: 'Optional[str]' = None,
        msg_user_id: 'Optional[str]' = None,
        msg_group_id: 'Optional[str]' = None,
        msg_group_seq: 'Optional[str]' = None,
        msg_property: 'Optional[str]' = None,
        msg_content_map_item: 'Optional[str]' = None,
        msg_content_list_item: 'Optional[str]' = None,
        msg_content_from_file: 'Optional[str]' = None,
        msg_content: 'Optional[ApplicationData]' = None,
        msg_content_type: 'Optional[str]' = None,
        content_type: 'Optional[str]' = None,
        **kwargs
    ) -> None:
        # dump arguments into dictionary
        inputs = locals()
        # remove self and kwargs variables as they would mess things up
        del inputs['self']
        del inputs['kwargs']
        # update kwargs to pass in super().__init__()
        kwargs.update(inputs)
        super(MessageOptionsSender, self).__init__(**kwargs)

    @staticmethod
    def valid_options() -> 'List[Union[Toggle, Prefixed, KWOption, ListOption]]':
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


class ReceiverSpecificOptions(OptionsBase):
    """
    Common client options for all Receiver client commands
    """

    def __init__(
        self,
        process_reply_to: 'Optional[str]' = None,
        action: 'Optional[str]' = None,
        recv_browse: 'Optional[bool]' = None,
        **kwargs
    ) -> None:
        # dump arguments into dictionary
        inputs = locals()
        # remove self and kwargs variables as they would mess things up
        del inputs['self']
        del inputs['kwargs']
        # update kwargs to pass in super().__init__()
        kwargs.update(inputs)
        super(ReceiverSpecificOptions, self).__init__(**kwargs)

    @staticmethod
    def valid_options() -> 'List[Union[Toggle, Prefixed, KWOption, ListOption]]':
        return [
            Prefixed('process-reply-to', '--process-reply-to'),
            Prefixed('action', '--action'),
            Toggle('recv-browse', '--recv-browse'),
        ]


class ReactorOptionsSenderReceiver(OptionsBase):
    """
    Common reactor options for all Sender and Receiver client commands
    """

    def __init__(
        self,
        reactor_auto_settle_off: 'Optional[bool]' = None,
        **kwargs
    ) -> None:
        # dump arguments into dictionary
        inputs = locals()
        # remove self and kwargs variables as they would mess things up
        del inputs['self']
        del inputs['kwargs']
        # update kwargs to pass in super().__init__()
        kwargs.update(inputs)
        super(ReactorOptionsSenderReceiver, self).__init__(**kwargs)

    @staticmethod
    def valid_options() -> 'List[Union[Toggle, Prefixed, KWOption, ListOption]]':
        return [Toggle('reactor-auto-settle-off', '--reactor-auto-settle-off')]
