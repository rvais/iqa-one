from typing import TYPE_CHECKING

from iqa.abstract.client.messaging_client import MessagingClient
from iqa.components.abstract.component import Component
from iqa.components.implementations.clients.external.command.client_command import ClientCommandBase

if TYPE_CHECKING:
    from typing import Optional
    # from os import PathLike Not used for now, but might replace path_to_exec in subclasses if appropriate
    from iqa.system.node.base.node import Node
    from iqa.abstract.listener import Listener
    from iqa.system.executor.base.execution import ExecutionBase


class ClientExternal(Component, MessagingClient):
    """
    Represents abstract clients that are executed externally as command line applications.
    """

    # Default is run forever
    # As mixing --timeout with --count is causing issues
    TIMEOUT: int = 90

    def __init__(self, name: str, node: Node, **kwargs) -> None:
        super(ClientExternal, self).__init__(name, node)
        self.execution: Optional[ExecutionBase] = None
        self._command: ClientCommandBase = ClientCommandBase([])
        self._url: Optional[str] = None
        self.reset_command()

        # initializing client from kwargs
        for func in [self.set_url, self.set_auth_mechs, self.set_ssl_auth]:
            self.call_if_all_arguments_in_kwargs(func, **kwargs)

    @property
    def command(self) -> ClientCommandBase:
        return self._command

    def reset_command(self) -> None:
        """
        Creates a new command instance based on concrete implementation.
        :return:
        """
        self._command = self._new_command(
            stdout=True, timeout=ClientExternal.TIMEOUT, daemon=True
        )

    def get_url(self) -> Optional[str]:
        return self._url

    def set_url(self, url: str) -> None:
        """
        Saves url property internally and invoke concrete _set_url implementation
        which is responsible for properly using it according to each external client needs.
        :param url:
        :return:
        """
        self._set_url(url)

    def _new_command(
        self,
        stdout: bool = False,
        stderr: bool = False,
        daemon: bool = False,
        timeout: int = 0,
        encoding: str = 'utf-8',
    ) -> ClientCommandBase:
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

    def _set_url(self, url: str) -> None:
        """
        This method must be implemented by each concrete client by adjusting url parts
        into appropriate command elements, in order to execute it correctly.
        :param url:
        :return:
        """
        raise NotImplementedError

    def set_auth_mechs(self, mechs: str):
        """
        Implementing clients must know how to adjust mechanisms (if supported).
        :param mechs:
        :return:
        """
        raise NotImplementedError

    def set_ssl_auth(
        self,
        pem_file: Optional[str] = None,
        key_file: Optional[str] = None,
        keystore: Optional[str] = None,
        keystore_pass: Optional[str] = None,
        keystore_alias: Optional[str] = None,
    ):
        """
        Allows implementing clients to use the SSL credentials according to each implementing model.
        :param pem_file:
        :param key_file:
        :param keystore:
        :param keystore_pass:
        :param keystore_alias:
        :return:
        """
        raise NotImplementedError

    def set_endpoint(self, listener: Listener) -> None:
        raise NotImplementedError

    def connect(self) -> bool:
        raise NotImplementedError

    @property
    def implementation(self) -> str:
        return 'External client'
