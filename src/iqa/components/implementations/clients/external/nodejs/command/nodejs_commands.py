"""
Specialized implementation of external command for cli-rhea clients (NodeJS).
"""
from iqa.components.clients.external.command.client_command import (
    ConnectorClientCommand,
    ReceiverClientCommand,
    SenderClientCommand,
)
from iqa.components.clients.external.command.options.client_options import (
    LinkOptionsSenderReceiver,
    ReactorOptionsSenderReceiver,
)
from iqa.components.clients.external.nodejs.command.nodejs_options import (
    NodeJSControlOptionsCommon,
    NodeJSConnectionOptionsCommon,
    NodeJSControlOptionsReceiver,
    NodeJSControlOptionsSender,
)


class NodeJSConnectorClientCommand(ConnectorClientCommand):
    """
    CLI RHEA connector client command specialization.
    In Node JS client we must provide --broker and (optionally) --address.
    The control property instance used here is RHEAControlOptionsCommon.
    """

    def __init__(
        self,
        stdout: bool = False,
        stderr: bool = False,
        daemon: bool = False,
        timeout: int = 0,
        encoding: str = 'utf-8',
    ) -> None:
        super(NodeJSConnectorClientCommand, self).__init__(
            stdout, stderr, daemon, timeout, encoding
        )
        self.control: NodeJSControlOptionsCommon = NodeJSControlOptionsCommon()
        self.connection: NodeJSConnectionOptionsCommon = NodeJSConnectionOptionsCommon()

    def main_command(self) -> list:
        return ['cli-rhea-connector']


class NodeJSReceiverClientCommand(ReceiverClientCommand):
    """
    CLI RHEA receiver client command specialization.
    In Node JS client we must provide --broker and (optionally) --address.
    The control property instance used here is RHEAControlOptionsCommon.
    """

    def __init__(
        self,
        stdout: bool = False,
        stderr: bool = False,
        daemon: bool = False,
        timeout: int = 0,
        encoding: str = 'utf-8',
    ) -> None:
        super(NodeJSReceiverClientCommand, self).__init__(
            stdout, stderr, daemon, timeout, encoding
        )
        self.control: NodeJSControlOptionsReceiver = NodeJSControlOptionsReceiver()
        self.connection: NodeJSConnectionOptionsCommon = NodeJSConnectionOptionsCommon()
        self.link: LinkOptionsSenderReceiver = LinkOptionsSenderReceiver()
        self.reactor: ReactorOptionsSenderReceiver = ReactorOptionsSenderReceiver()

    def main_command(self) -> list:
        return ['cli-rhea-receiver']


class NodeJSSenderClientCommand(SenderClientCommand):
    """
    CLI RHEA sender client command specialization.
    In Node JS client we must provide --broker and (optionally) --address.
    The control property instance used here is RHEAControlOptionsCommon.
    """

    def __init__(
        self,
        stdout: bool = False,
        stderr: bool = False,
        daemon: bool = False,
        timeout: int = 0,
        encoding: str = 'utf-8',
    ) -> None:
        super(NodeJSSenderClientCommand, self).__init__(
            stdout, stderr, daemon, timeout, encoding
        )
        self.control: NodeJSControlOptionsSender = NodeJSControlOptionsSender()
        self.connection: NodeJSConnectionOptionsCommon = NodeJSConnectionOptionsCommon()
        self.link: LinkOptionsSenderReceiver = LinkOptionsSenderReceiver()
        self.reactor: ReactorOptionsSenderReceiver = ReactorOptionsSenderReceiver()

    def main_command(self) -> list:
        return ['cli-rhea-sender']
