from typing import Optional
from urllib.parse import urlparse, unquote

from iqa.components.clients.external.java.command.java_commands import (
    JavaConnectorClientCommand,
)
from iqa.system.node.node import Node
from .client import ClientJava


class ConnectorJava(ClientJava):
    """External Java Qpid JMS connector client."""

    _command: JavaConnectorClientCommand

    def __init__(self, name: str, node: Node, **kwargs) -> None:
        super(ConnectorJava, self).__init__(name, node, **kwargs)

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
        pem_file: Optional[str] = None,
        key_file: Optional[str] = None,
        keystore: Optional[str] = None,
        keystore_pass: Optional[str] = None,
        keystore_alias: Optional[str] = None,
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
