"""
Implementation of cli-proton-python external client command.
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
    LinkOptionsReceiver,
    LinkOptionsSenderReceiver,
    ReactorOptionsSenderReceiver,
)
from iqa.components.implementations.clients.external.python.command.python_options import (
    PythonControlOptionsCommon,
    PythonControlOptionsReceiver,
    PythonControlOptionsSenderReceiver,
    PythonConnectionOptionsCommon,
)


class PythonConnectorClientCommand(ConnectorClientCommand):
    """
    Connector client command for cli-proton-python.
    In Python client there is --broker-url parameter and so we need
    to replace control instance by PythonControlOptionsCommon.
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
        super(PythonConnectorClientCommand, self).__init__(
            path_to_exec, stdout, stderr, daemon, timeout, encoding
        )
        self.control: PythonControlOptionsCommon = PythonControlOptionsCommon()
        self.connection: PythonConnectionOptionsCommon = PythonConnectionOptionsCommon()

    def main_command(self) -> 'List[str]':
        executable: str = 'cli-proton-python-connector'
        if self.path_to_exec:
            executable = os_path.join(self.path_to_exec, executable)
        return [executable]


class PythonReceiverClientCommand(ReceiverClientCommand):
    """
    Receiver client command for cli-proton-python.
    In Python client there is --broker-url parameter and so we need
    to replace control instance by PythonControlOptionsCommon.
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
        super(PythonReceiverClientCommand, self).__init__(
            path_to_exec, stdout, stderr, daemon, timeout, encoding
        )
        self.control: PythonControlOptionsReceiver = PythonControlOptionsReceiver()
        self.link: LinkOptionsReceiver = LinkOptionsReceiver()
        self.reactor: ReactorOptionsSenderReceiver = ReactorOptionsSenderReceiver()
        self.connection: PythonConnectionOptionsCommon = PythonConnectionOptionsCommon()

    def main_command(self) -> 'List[str]':
        executable: str = 'cli-proton-python-receiver'
        if self.path_to_exec:
            executable = os_path.join(self.path_to_exec, executable)
        return [executable]


class PythonSenderClientCommand(SenderClientCommand):
    """
    Sender client command for cli-proton-python.
    In Python client there is --broker-url parameter and so we need
    to replace control instance by PythonControlOptionsCommon.
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
        super(PythonSenderClientCommand, self).__init__(
            path_to_exec, stdout, stderr, daemon, timeout, encoding
        )
        self.control: PythonControlOptionsSenderReceiver = PythonControlOptionsSenderReceiver()
        self.link: LinkOptionsSenderReceiver = LinkOptionsSenderReceiver()
        self.reactor: ReactorOptionsSenderReceiver = ReactorOptionsSenderReceiver()
        self.connection: PythonConnectionOptionsCommon = PythonConnectionOptionsCommon()

    def main_command(self) -> 'List[str]':
        executable: str = 'cli-proton-python-sender'
        if self.path_to_exec:
            executable = os_path.join(self.path_to_exec, executable)
        return [executable]
