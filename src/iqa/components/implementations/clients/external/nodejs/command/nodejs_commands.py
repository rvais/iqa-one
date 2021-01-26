"""
Specialized implementation of external command for cli-rhea clients (NodeJS).
"""
import os.path as os_path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, List, Any
    from os import PathLike

from iqa.components.implementations.clients.external.command.client_command import (
    ConnectorClientCommand,
    ReceiverClientCommand,
    SenderClientCommand,
)
from iqa.components.implementations.clients.external.command.options.client_options import (
    LinkOptionsSenderReceiver,
    ReactorOptionsSenderReceiver,
)
from iqa.components.implementations.clients.external.nodejs.command.nodejs_options import (
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
        path_to_exec: 'Optional[PathLike[Any]]' = None,
        stdout: bool = False,
        stderr: bool = False,
        daemon: bool = False,
        timeout: int = 0,
        encoding: str = 'utf-8',
    ) -> None:
        super(NodeJSConnectorClientCommand, self).__init__(
            path_to_exec, stdout, stderr, daemon, timeout, encoding
        )
        self.control: NodeJSControlOptionsCommon = NodeJSControlOptionsCommon()
        self.connection: NodeJSConnectionOptionsCommon = NodeJSConnectionOptionsCommon()

    def main_command(self) -> 'List[str]':
        executable: str = 'cli-rhea-connector'
        if self.path_to_exec:
            executable = os_path.join(self.path_to_exec, executable)
        return [executable]


class NodeJSReceiverClientCommand(ReceiverClientCommand):
    """
    CLI RHEA receiver client command specialization.
    In Node JS client we must provide --broker and (optionally) --address.
    The control property instance used here is RHEAControlOptionsCommon.
    """

    def __init__(
        self,
        path_to_exec: 'Optional[PathLike[Any]]' = None,
        stdout: bool = False,
        stderr: bool = False,
        daemon: bool = False,
        timeout: int = 0,
        encoding: str = 'utf-8',
    ) -> None:
        super(NodeJSReceiverClientCommand, self).__init__(
            path_to_exec, stdout, stderr, daemon, timeout, encoding
        )
        self.control: NodeJSControlOptionsReceiver = NodeJSControlOptionsReceiver()
        self.connection: NodeJSConnectionOptionsCommon = NodeJSConnectionOptionsCommon()
        self.link: LinkOptionsSenderReceiver = LinkOptionsSenderReceiver()
        self.reactor: ReactorOptionsSenderReceiver = ReactorOptionsSenderReceiver()

    def main_command(self) -> 'List[str]':
        executable: str = 'cli-rhea-receiver'
        if self.path_to_exec:
            executable = os_path.join(self.path_to_exec, executable)
        return [executable]


class NodeJSSenderClientCommand(SenderClientCommand):
    """
    CLI RHEA sender client command specialization.
    In Node JS client we must provide --broker and (optionally) --address.
    The control property instance used here is RHEAControlOptionsCommon.
    """

    def __init__(
        self,
        path_to_exec: 'Optional[PathLike[Any]]' = None,
        stdout: bool = False,
        stderr: bool = False,
        daemon: bool = False,
        timeout: int = 0,
        encoding: str = 'utf-8',
    ) -> None:
        super(NodeJSSenderClientCommand, self).__init__(
          path_to_exec, stdout, stderr, daemon, timeout, encoding
        )
        self.control: NodeJSControlOptionsSender = NodeJSControlOptionsSender()
        self.connection: NodeJSConnectionOptionsCommon = NodeJSConnectionOptionsCommon()
        self.link: LinkOptionsSenderReceiver = LinkOptionsSenderReceiver()
        self.reactor: ReactorOptionsSenderReceiver = ReactorOptionsSenderReceiver()

    def main_command(self) -> 'List[str]':
        executable: str = 'cli-rhea-sender'
        if self.path_to_exec:
            executable = os_path.join(self.path_to_exec, executable)
        return [executable]
