from iqa.components.clients.external.python.command.python_commands import (
    PythonConnectorClientCommand,
)
from iqa.system.node.node import Node
from .client import ClientPython


class ConnectorPython(ClientPython):
    """External Python-Proton connector client."""

    _command: PythonConnectorClientCommand

    def __init__(self, name: str, node: Node, **kwargs) -> None:
        super(ConnectorPython, self).__init__(name, node, **kwargs)

    def _set_url(self, url: str) -> None:
        self._command.control.broker_url = url

    def set_auth_mechs(self, mechs: str) -> None:
        self._command.connection.conn_allowed_mechs = mechs

    def set_ssl_auth(
        self,
        pem_file: str = None,
        key_file: str = None,
        keystore: str = None,
        keystore_pass: str = None,
        keystore_alias: str = None,
    ) -> None:
        self._command.connection.conn_ssl_certificate = pem_file
        self._command.connection.conn_ssl_private_key = key_file

    def _new_command(
        self,
        stdout: bool = True,
        stderr: bool = True,
        daemon: bool = True,
        timeout: int = ClientPython.TIMEOUT,
        encoding: str = 'utf-8',
    ) -> PythonConnectorClientCommand:
        return PythonConnectorClientCommand(
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
