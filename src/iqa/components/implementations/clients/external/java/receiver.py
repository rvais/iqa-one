from urllib.parse import urlparse, urlunparse, unquote
from iqa.abstract.client.receiver import Receiver
from iqa.components.implementations.clients.external.java.client import ClientJava

from typing import TYPE_CHECKING

from iqa.components.implementations.clients.external.java.command.java_commands import JavaReceiverClientCommand

if TYPE_CHECKING:
    from os import PathLike
    from typing import Optional, Any
    from iqa.system.node.base.node import Node


class ReceiverJava(ClientJava, Receiver):
    """External Java Qpid JMS receiver client."""

    _command: JavaReceiverClientCommand
    path_to_exec: 'Optional[PathLike[Any]]'

    def __init__(self, name: str, node: 'Node', path_to_exec: 'Optional[PathLike[Any]]' = None, **kwargs) -> None:
        super(ReceiverJava, self).__init__(name, node, **kwargs)
        self.path_to_exec = path_to_exec

    def _set_url(self, url: str) -> None:
        p_url = urlparse(url)
        self._command.control.broker = '{}://{}:{}'.format(
            p_url.scheme, p_url.hostname, p_url.port
        )
        self._command.control.address = urlunparse(
            (
                '',
                '',
                p_url.path or '',
                p_url.params or '',
                p_url.query or '',
                p_url.fragment or '',
            )
        )

        # Java client expects unquoted username and passwords
        if p_url.username:
            self._command.connection.conn_username = unquote(p_url.username)
        if p_url.password:
            self._command.connection.conn_password = unquote(p_url.password)

    def set_auth_mechs(self, mechs: str) -> None:
        self._command.connection.conn_auth_mechanisms = mechs

    def set_ssl_auth(
        self,
        pem_file: 'Optional[str]' = None,
        key_file: 'Optional[str]' = None,
        keystore: 'Optional[str]' = None,
        keystore_pass: 'Optional[str]' = None,
        keystore_alias: 'Optional[str]' = None,
    ) -> None:
        self._command.connection.conn_ssl_keystore_location = keystore
        self._command.connection.conn_ssl_keystore_password = keystore_pass
        self._command.connection.conn_ssl_key_alias = keystore_alias
        self._command.connection.conn_ssl_verify_host = 'false'
        self._command.connection.conn_ssl_trust_all = 'true'

    def _new_command(
        self,
        stdout: bool = True,
        stderr: bool = True,
        daemon: bool = False,
        timeout: int = ClientJava.TIMEOUT,
        encoding: str = 'utf-8',
    ) -> JavaReceiverClientCommand:
        return JavaReceiverClientCommand(
            path_to_exec=self.path_to_exec,
            stdout=stdout,
            stderr=stderr,
            daemon=daemon,
            timeout=timeout,
            encoding=encoding,
        )

    def _receive(self) -> None:
        self.execution = self.node.execute(self.command)

    def connect(self) -> bool:
        raise NotImplementedError
