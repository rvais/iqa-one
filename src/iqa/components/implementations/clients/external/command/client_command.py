"""
Abstract (base) implementations of supported external client commands.
All options here are common to all kind of client commands, be it a
receiver, sender or connector.
Options are also common to implementation language (java, python, etc).
In case an implementation has a different set of options, specialize it
in a separate module inside abstract.client.command.impl.
"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Any, List
    from os import PathLike

from iqa.components.implementations.clients.external.command.options.client_options import (
    ClientOptionsBase,
    ControlOptionsCommon,
    LoggingOptionsCommon,
    ConnectionOptionsCommon,
    ConnectorOptions,
    ControlOptionsReceiver,
    LoggingOptionsSenderReceiver,
    TransactionOptionsSenderReceiver,
    ReceiverOptions,
    ControlOptionsSenderReceiver,
    MessageOptionsSender,
)
from iqa.system.command.command_base import CommandBase


class ClientCommandBase(CommandBase):
    """
    Base abstraction class for external clients commands. It encapsulates the
    args property and getter generates a new list based on ClientCommand's
    implementation details (based on states of internal ClientOptionsBase
    properties).
    """

    def __init__(
        self,
        args: list,
        path_to_exec: 'Optional[PathLike[Any]]' = None,
        stdout: bool = True,
        stderr: bool = True,
        daemon: bool = False,
        timeout: int = 0,
        encoding: str = 'utf-8',
    ) -> None:
        super(ClientCommandBase).__init__(args, path_to_exec, stdout, stderr, daemon, timeout, encoding)
        self.control: Optional[ControlOptionsCommon] = None
        self.logging: Optional[LoggingOptionsCommon] = None

    @property  # type: ignore
    def args(self) -> 'List[str]':
        return self._build_command()

    def main_command(self) -> 'List[str]':
        """
        List of arguments needed to run the client implementation.
        :return:
        """
        raise NotImplemented

    def _build_command(self) -> 'List[str]':
        """
        Builds the external client command based on all
        ClientOptionsBase properties available on implementing class,
        using optconstruct to produce the arguments list.
        :return:
        """
        all_options: dict = {}
        valid_options: list = []

        for opt_name, opt_value in self.__dict__.items():
            # Skip members that are not an instance of ClientOptionsBase
            if not isinstance(opt_value, ClientOptionsBase):
                continue
            # List of populated options
            all_options.update(opt_value.to_dict())
            # Append list of valid options for each ClientOptionsBase
            # implementation
            valid_options += opt_value.valid_options()

        # Generates parameters list (only allowed will be added)
        params: list = [
            opt.generate(all_options).split(' ', 1)
            for opt in valid_options
            if opt.satisfied(all_options)
        ]
        params_flat: list = [item for param in params for item in param]

        return self.main_command() + params_flat


class ConnectorClientCommand(ClientCommandBase):
    """
    Abstract implementation of common Connector client options.
    """

    def main_command(self) -> 'List[str]':
        raise NotImplemented

    def __init__(
        self,
        path_to_exec: 'Optional[PathLike[Any]]' = None,
        stdout: bool = False,
        stderr: bool = False,
        daemon: bool = False,
        timeout: int = 0,
        encoding: str = 'utf-8',
    ) -> None:
        super(ConnectorClientCommand, self).__init__(
            [], path_to_exec, stdout, stderr, daemon, timeout, encoding
        )
        self.control: ControlOptionsCommon = ControlOptionsCommon()
        self.logging: LoggingOptionsCommon = LoggingOptionsCommon()
        self.connection: ConnectionOptionsCommon = ConnectionOptionsCommon()
        self.connector: ConnectorOptions = ConnectorOptions()


class ReceiverClientCommand(ClientCommandBase):
    """
    Abstract implementation of common Receiver client options.
    """

    def main_command(self) -> 'List[str]':
        raise NotImplemented

    def __init__(
        self,
        path_to_exec: 'Optional[PathLike[Any]]' = None,
        stdout: bool = False,
        stderr: bool = False,
        daemon: bool = False,
        timeout: int = 0,
        encoding: str = 'utf-8',
    ):
        super(ReceiverClientCommand, self).__init__(
            [], path_to_exec, stdout, stderr, daemon, timeout, encoding
        )
        self.control: ControlOptionsReceiver = ControlOptionsReceiver()
        self.logging: LoggingOptionsSenderReceiver = LoggingOptionsSenderReceiver()
        self.transaction: TransactionOptionsSenderReceiver = TransactionOptionsSenderReceiver()
        self.connection: ConnectionOptionsCommon = ConnectionOptionsCommon()
        self.receiver: ReceiverOptions = ReceiverOptions()


class SenderClientCommand(ClientCommandBase):
    """
        Abstract implementation of common Sender client options.
    """

    def main_command(self) -> 'List[str]':
        raise NotImplemented

    def __init__(
        self,
        path_to_exec: 'Optional[PathLike[Any]]' = None,
        stdout: bool = False,
        stderr: bool = False,
        daemon: bool = False,
        timeout: int = 0,
        encoding: str = 'utf-8',
    ) -> None:
        super(SenderClientCommand, self).__init__(
            [], path_to_exec, stdout, stderr, daemon, timeout, encoding
        )
        self.control: ControlOptionsSenderReceiver = ControlOptionsSenderReceiver()
        self.logging: LoggingOptionsSenderReceiver = LoggingOptionsSenderReceiver()
        self.transaction: TransactionOptionsSenderReceiver = TransactionOptionsSenderReceiver()
        self.connection: ConnectionOptionsCommon = ConnectionOptionsCommon()
        self.message: MessageOptionsSender = MessageOptionsSender()
