from typing import TYPE_CHECKING
from urllib.parse import urlparse, unquote

from iqa.components.implementations.clients.external.java.command.java_commands import JavaConnectorClientCommand
from iqa.components.implementations.clients.external.java.client import ClientJava

if TYPE_CHECKING:
    from os import PathLike
    from typing import Optional, Any
    from iqa.system.node.base.node import Node


class ConnectorJava(ClientJava):
    """External Java Qpid JMS connector client."""

    _command: JavaConnectorClientCommand
    path_to_exec: 'Optional[PathLike[Any]]'

    def __init__(self, name: str, node: 'Node', path_to_exec: 'Optional[PathLike[Any]]' = None, **kwargs) -> None:
        super(ConnectorJava, self).__init__(name, node, **kwargs)
        self.path_to_exec = path_to_exec

    def _set_url(self, url: str) -> None:
        p_url = urlparse(url)
        self._command.control.broker = '{}://{}:{}'.format(
            p_url.scheme or 'amqp', p_url.hostname or '127.0.0.1', p_url.port or '5672'
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
        daemon: bool = True,
        timeout: int = ClientJava.TIMEOUT,
        encoding: str = 'utf-8',
    ) -> JavaConnectorClientCommand:
        return JavaConnectorClientCommand(
            path_to_exec=self.path_to_exec,
            stdout=stdout,
            stderr=stderr,
            daemon=daemon,
            timeout=timeout,
            encoding=encoding,
        )

    def connect(self) -> bool:
        self.execution = self.node.execute(self.command)
        if self.execution.completed_successfully():
            return True
        return False
