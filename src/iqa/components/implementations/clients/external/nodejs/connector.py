from typing import Optional
from urllib.parse import urlparse

from iqa.components.clients.external.nodejs.command.nodejs_commands import (
    NodeJSConnectorClientCommand,
)
from iqa.system.node.node import Node
from .client import ClientNodeJS


class ConnectorNodeJS(ClientNodeJS):
    """External NodeJS connector client."""

    _command: NodeJSConnectorClientCommand

    def __init__(self, name: str, node: Node, **kwargs) -> None:
        super(ConnectorNodeJS, self).__init__(name, node, **kwargs)

    def _set_url(self, url: str) -> None:
        p_url = urlparse(url)
        p_url._replace(scheme='')
        self._command.control.broker = p_url.netloc

    def set_auth_mechs(self, mechs: str) -> None:
        pass

    def set_ssl_auth(
        self,
        pem_file: Optional[str] = None,
        key_file: Optional[str] = None,
        keystore: Optional[str] = None,
        keystore_pass: Optional[str] = None,
        keystore_alias: Optional[str] = None,
    ) -> None:
        self._command.connection.conn_ssl_certificate = pem_file
        self._command.connection.conn_ssl_private_key = key_file
        self._command.connection.conn_ssl = True

    def _new_command(
        self,
        stdout: bool = True,
        stderr: bool = True,
        daemon: bool = True,
        timeout: int = ClientNodeJS.TIMEOUT,
        encoding: str = 'utf-8',
    ) -> NodeJSConnectorClientCommand:
        return NodeJSConnectorClientCommand(
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
