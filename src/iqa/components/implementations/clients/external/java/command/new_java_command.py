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
    from typing import Optional, Any, List, Dict, Union
    from iqa.system.command.new_options_base import OptionsBase
    from os import PathLike

from iqa.system.command.new_command_base import CommandBase
from iqa.system.command.new_options_base import EmptyOptions
from iqa.components.implementations.clients.external.command.options.client_options import (
    # ClientOptionsBase,
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


class JavaClientCommandBase(CommandBase):
    """
    Base abstraction class for external clients commands. It encapsulates the
    args property and getter generates a new list based on ClientCommand's
    implementation details (based on states of internal ClientOptionsBase
    properties).
    """

    def __init__(
            self,
            kind: 'Optional[str]' = None,
            args: 'Optional[List[str]]' = None,
            path_to_exec: 'Optional[Union[str, bytes, PathLike]]' = None,
            stdout: bool = True,
            stderr: bool = True,
            daemon: bool = False,
            timeout: int = 0,
            encoding: str = 'utf-8',
            wait_for: bool = False,
            env: 'Optional[Dict]' = None,
            args_before_opts: bool = True,
            **kwargs
    ) -> None:
        # dump arguments into dictionary
        inputs = locals()
        # remove self and kwargs variables as they would mess things up
        del inputs['self']
        del inputs['kwargs']
        # update kwargs to pass in super().__init__()
        kwargs.update(inputs)
        super(JavaClientCommandBase, self).__init__(**kwargs)
        self._kind = kind if kind is not None and kind != '' else 'connector'

    @property
    def options(self) -> 'OptionsBase':
        """
        Delegated method that must return a list of all valid
        options allowed by the client command.
        List must be composed of OptionAbstract objects.
        :return:
        """
        if self._options is None:
            self._options = EmptyOptions()
        return self._options

    def _build(self) -> 'List[str]':
        """
        Builds the external client command based on all
        ClientOptionsBase properties available on implementing class,
        using optconstruct to produce the arguments list.
        :return:
        """
        # Crate base list for the command
        command: List[str] = []
        if self.path_to_exec:
            command = ['java', '-jar', self.path_to_exec, self._kind]

        # implementation of the options classes ensures that only populated ones are returned
        all_options: Dict = {}
        key: str
        value: Any
        for key, value in self.options.to_dictionary().items():
            all_options[key.replace('_', '-')] = value

        # Generates parameters list (only allowed will be added)
        params: List[str] = []
        for opt in self.options.valid_options():
            if opt.satisfied(all_options):
                params.extend(opt.generate(all_options).split(' ', 1))

        # based on selected ordering extend command first with arguments, then options or vice versa
        if self._args_before_opts:
            command.extend(self._args)
            command.extend(params)
        else:
            command.extend(params)
            command.extend(self._args)

        return command


class JavaConnectorCommand(JavaClientCommandBase):
    """
    Abstract implementation of common Connector client options.
    """

    def __init__(
            self,
            args: 'Optional[List[str]]' = None,
            path_to_exec: 'Optional[Union[str, bytes, PathLike]]' = None,
            stdout: bool = True,
            stderr: bool = True,
            daemon: bool = False,
            timeout: int = 0,
            encoding: str = 'utf-8',
            wait_for: bool = False,
            env: 'Optional[Dict]' = None,
            args_before_opts: bool = True,
            **kwargs
    ) -> None:
        # dump arguments into dictionary
        inputs = locals()
        # remove self and kwargs variables as they would mess things up
        del inputs['self']
        del inputs['kwargs']
        inputs['kind'] = 'connector'
        # update kwargs to pass in super().__init__()
        kwargs.update(inputs)
        super(JavaConnectorCommand, self).__init__(**kwargs)

        self.control: ControlOptionsCommon = ControlOptionsCommon()
        self.logging: LoggingOptionsCommon = LoggingOptionsCommon()
        self.connection: ConnectionOptionsCommon = ConnectionOptionsCommon()
        self.connector: ConnectorOptions = ConnectorOptions()

    @property
    def options(self) -> 'OptionsBase':
        """
        Delegated method that must return a list of all valid
        options allowed by the client command.
        List must be composed of OptionAbstract objects.
        :return:
        """
        if self._options is None:
            self._options = EmptyOptions()
        return self._options


class JavaReceiverCommand(JavaClientCommandBase):
    """
    Abstract implementation of common Receiver client options.
    """

    def __init__(
            self,
            args: 'Optional[List[str]]' = None,
            path_to_exec: 'Optional[Union[str, bytes, PathLike]]' = None,
            stdout: bool = True,
            stderr: bool = True,
            daemon: bool = False,
            timeout: int = 0,
            encoding: str = 'utf-8',
            wait_for: bool = False,
            env: 'Optional[Dict]' = None,
            args_before_opts: bool = True,
            **kwargs
    ) -> None:
        # dump arguments into dictionary
        inputs = locals()
        # remove self and kwargs variables as they would mess things up
        del inputs['self']
        del inputs['kwargs']
        inputs['kind'] = 'receiver'
        # update kwargs to pass in super().__init__()
        kwargs.update(inputs)
        super(JavaReceiverCommand, self).__init__(**kwargs)

        self.control: ControlOptionsReceiver = ControlOptionsReceiver()
        self.logging: LoggingOptionsSenderReceiver = LoggingOptionsSenderReceiver()
        self.transaction: TransactionOptionsSenderReceiver = TransactionOptionsSenderReceiver()
        self.connection: ConnectionOptionsCommon = ConnectionOptionsCommon()
        self.receiver: ReceiverOptions = ReceiverOptions()

    @property
    def options(self) -> 'OptionsBase':
        """
        Delegated method that must return a list of all valid
        options allowed by the client command.
        List must be composed of OptionAbstract objects.
        :return:
        """
        if self._options is None:
            self._options = EmptyOptions()
        return self._options


class JavaSenderCommand(JavaClientCommandBase):
    """
        Abstract implementation of common Sender client options.
    """

    def __init__(
            self,
            args: 'Optional[List[str]]' = None,
            path_to_exec: 'Optional[Union[str, bytes, PathLike]]' = None,
            stdout: bool = True,
            stderr: bool = True,
            daemon: bool = False,
            timeout: int = 0,
            encoding: str = 'utf-8',
            wait_for: bool = False,
            env: 'Optional[Dict]' = None,
            args_before_opts: bool = True,
            **kwargs
    ) -> None:
        # dump arguments into dictionary
        inputs = locals()
        # remove self and kwargs variables as they would mess things up
        del inputs['self']
        del inputs['kwargs']
        inputs['kind'] = 'sender'
        # update kwargs to pass in super().__init__()
        kwargs.update(inputs)
        super(JavaSenderCommand, self).__init__(**kwargs)

        self.control: ControlOptionsSenderReceiver = ControlOptionsSenderReceiver()
        self.logging: LoggingOptionsSenderReceiver = LoggingOptionsSenderReceiver()
        self.transaction: TransactionOptionsSenderReceiver = TransactionOptionsSenderReceiver()
        self.connection: ConnectionOptionsCommon = ConnectionOptionsCommon()
        self.message: MessageOptionsSender = MessageOptionsSender()

    @property
    def options(self) -> 'OptionsBase':
        """
        Delegated method that must return a list of all valid
        options allowed by the client command.
        List must be composed of OptionAbstract objects.
        :return:
        """
        if self._options is None:
            self._options = EmptyOptions()
        return self._options
