"""
Specialized implementation of external command for java clients (currently cli-qpid.jar only).
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
from iqa.components.implementations.clients.external.java.command.java_options import (
    JavaControlOptionsCommon,
    JavaConnectionOptionsCommon,
    JavaControlOptionsReceiver,
    JavaControlOptionsSenderReceiver,
)


class JavaConnectorClientCommand(ConnectorClientCommand):
    """
    Java connector client command specialization.
    In Java client we must provide --broker and (optionally) --address.
    The control property instance used here is JavaControlOptionsCommon.
    """

    def __init__(
        self,
        path_to_exec: Optional[PathLike[Any]] = None,
        stdout: bool = False,
        stderr: bool = False,
        daemon: bool = False,
        timeout: int = 0,
        encoding: str = 'utf-8',
    ) -> None:
        super(JavaConnectorClientCommand, self).__init__(
            path_to_exec, stdout, stderr, daemon, timeout, encoding
        )
        self.control: JavaControlOptionsCommon = JavaControlOptionsCommon()
        self.connection: JavaConnectionOptionsCommon = JavaConnectionOptionsCommon()

    def main_command(self) -> List[str]:
        jar: str = 'cli-qpid-jms.jar'
        if self.path_to_exec:
            jar = os_path.join(self.path_to_exec, jar)
        return ['java', '-jar', jar, "connector"]


class JavaReceiverClientCommand(ReceiverClientCommand):
    def __init__(
        self,
        path_to_exec: Optional[PathLike[Any]] = None,
        stdout: bool = False,
        stderr: bool = False,
        daemon: bool = False,
        timeout: int = 0,
        encoding: str = 'utf-8',
    ) -> None:
        """
        Java receiver client command specialization.
        In Java client we must provide --broker and (optionally) --address.
        The control property instance used here is JavaControlOptionsCommon.
        """
        super(JavaReceiverClientCommand, self).__init__(
            path_to_exec, stdout, stderr, daemon, timeout, encoding
        )
        self.control: JavaControlOptionsReceiver = JavaControlOptionsReceiver()
        self.connection: JavaConnectionOptionsCommon = JavaConnectionOptionsCommon()

    def main_command(self) -> List[str]:
        jar: str = 'cli-qpid-jms.jar'
        if self.path_to_exec:
            jar = os_path.join(self.path_to_exec, jar)
        return ['java', '-jar', jar, "receiver"]


class JavaSenderClientCommand(SenderClientCommand):
    def __init__(
        self,
        path_to_exec: Optional[PathLike[Any]] = None,
        stdout: bool = False,
        stderr: bool = False,
        daemon: bool = False,
        timeout: int = 0,
        encoding: str = 'utf-8',
    ) -> None:
        """
        Java sender client command specialization.
        In Java client we must provide --broker and (optionally) --address.
        The control property instance used here is JavaControlOptionsCommon.
        """
        super(JavaSenderClientCommand, self).__init__(
            path_to_exec, stdout, stderr, daemon, timeout, encoding
        )
        self.control: JavaControlOptionsSenderReceiver = JavaControlOptionsSenderReceiver()
        self.connection: JavaConnectionOptionsCommon = JavaConnectionOptionsCommon()

    def main_command(self) -> List[str]:
        jar: str = 'cli-qpid-jms.jar'
        if self.path_to_exec:
            jar = os_path.join(self.path_to_exec, jar)
        return ['java', '-jar', jar, "sender"]
