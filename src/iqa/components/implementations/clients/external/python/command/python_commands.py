"""
Implementation of cli-proton-python external client command.
"""
from iqa.components.clients.external.command.client_command import (
    ConnectorClientCommand,
    ReceiverClientCommand,
    SenderClientCommand,
)
from iqa.components.clients.external.command.options.client_options import (
    LinkOptionsReceiver,
    LinkOptionsSenderReceiver,
    ReactorOptionsSenderReceiver,
)
from iqa.components.clients.external.python.command.python_options import (
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
        stdout: bool = False,
        stderr: bool = False,
        daemon: bool = False,
        timeout: int = 0,
        encoding: str = 'utf-8',
    ) -> None:
        super(PythonConnectorClientCommand, self).__init__(
            stdout, stderr, daemon, timeout, encoding
        )
        self.control: PythonControlOptionsCommon = PythonControlOptionsCommon()
        self.connection: PythonConnectionOptionsCommon = PythonConnectionOptionsCommon()

    def main_command(self) -> list:
        return ['cli-proton-python-connector']


class PythonReceiverClientCommand(ReceiverClientCommand):
    """
    Receiver client command for cli-proton-python.
    In Python client there is --broker-url parameter and so we need
    to replace control instance by PythonControlOptionsCommon.
    """

    def __init__(
        self,
        stdout: bool = False,
        stderr: bool = False,
        daemon: bool = False,
        timeout: int = 0,
        encoding: str = 'utf-8',
    ) -> None:
        super(PythonReceiverClientCommand, self).__init__(
            stdout, stderr, daemon, timeout, encoding
        )
        self.control: PythonControlOptionsReceiver = PythonControlOptionsReceiver()
        self.link: LinkOptionsReceiver = LinkOptionsReceiver()
        self.reactor: ReactorOptionsSenderReceiver = ReactorOptionsSenderReceiver()
        self.connection: PythonConnectionOptionsCommon = PythonConnectionOptionsCommon()

    def main_command(self) -> list:
        return ['cli-proton-python-receiver']


class PythonSenderClientCommand(SenderClientCommand):
    """
    Sender client command for cli-proton-python.
    In Python client there is --broker-url parameter and so we need
    to replace control instance by PythonControlOptionsCommon.
    """

    def __init__(
        self,
        stdout: bool = False,
        stderr: bool = False,
        daemon: bool = False,
        timeout: int = 0,
        encoding: str = 'utf-8',
    ) -> None:
        super(PythonSenderClientCommand, self).__init__(
            stdout, stderr, daemon, timeout, encoding
        )
        self.control: PythonControlOptionsSenderReceiver = PythonControlOptionsSenderReceiver()
        self.link: LinkOptionsSenderReceiver = LinkOptionsSenderReceiver()
        self.reactor: ReactorOptionsSenderReceiver = ReactorOptionsSenderReceiver()
        self.connection: PythonConnectionOptionsCommon = PythonConnectionOptionsCommon()

    def main_command(self) -> list:
        return ['cli-proton-python-sender']
