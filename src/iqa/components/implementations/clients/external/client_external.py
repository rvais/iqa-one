from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

from iqa.abstract.client.messaging_client import MessagingClient
from iqa.components.abstract.external_component import ExternalComponent
from iqa.system.command.new_command_base import CommandBase

if TYPE_CHECKING:
    from typing import Optional, Union
    from os import PathLike
    from iqa.system.node.base.node import Node


class ClientExternal(MessagingClient, ExternalComponent, ABC):
    """
    Represents abstract clients that are executed externally as command line applications.
    """

    # Default is run forever
    # As mixing --timeout with --count is causing issues
    TIMEOUT: int = 90

    def __init__(
            self,
            path_to_exec: 'Optional[Union[str, bytes, PathLike]]' = None,
            name: 'Optional[str]' = None,
            node: 'Optional[Node]' = None,
            message_buffer: bool = True,
            **kwargs
    ) -> None:
        # dump arguments into dictionary
        inputs = locals()
        # remove self and kwargs variables as they would mess things up
        del inputs['self']
        del inputs['kwargs']
        kwargs.update(inputs)

        super(ClientExternal, self).__init__(**kwargs)
        self._command: Optional[CommandBase] = None
        self._url: Optional[str] = None
        self.reset_command()

        # initializing client from kwargs
        for func in [self.set_url, self.set_auth_mechs, self.set_ssl_auth]:
            self.call_if_all_arguments_in_kwargs(func, **kwargs)

    @property
    def command(self) -> 'CommandBase':
        if self._command is None:
            self.reset_command()
        return self._command

    def reset_command(self) -> None:
        """
        Creates a new command instance based on concrete implementation.
        :return:
        """
        self._command = self._new_command(
            stdout=True, stderr=True, timeout=ClientExternal.TIMEOUT, daemon=True
        )

    @abstractmethod
    def _new_command(
        self,
        stdout: bool = False,
        stderr: bool = False,
        daemon: bool = False,
        timeout: int = 0,
        encoding: str = 'utf-8',
    ) -> CommandBase:
        """
        Must return a ClientCommand implementation for the command that is related
        with the concrete client.
        :param stdout:
        :param stderr:
        :param daemon:
        :param timeout:
        :param encoding:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def set_auth_mechs(self, mechs: 'Optional[str]' = None) -> None:
        """
        Implementing clients must know how to adjust mechanisms (if supported).
        :param mechs:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def set_ssl_auth(
        self,
        pem_file: 'Optional[str]' = None,
        key_file: 'Optional[str]' = None,
        keystore: 'Optional[str]' = None,
        keystore_pass: 'Optional[str]' = None,
        keystore_alias: 'Optional[str]' = None,
    ) -> None:
        """
        Allows implementing clients to use the SSL credentials according to each implementing model.
        :param pem_file:
        :param key_file:
        :param keystore:
        :param keystore_pass:
        :param keystore_alias:
        :return:
        """
