from iqa.abstract.client.sender import Sender
from iqa.abstract.message.message import Message
from iqa.components.clients.external.command.client_command import ClientCommandBase
from iqa.components.clients.external.python.client import ClientPython
from iqa.components.clients.external.python.command.python_commands import (
    PythonSenderClientCommand,
)
from iqa.system.node.node import Node


class SenderPython(ClientPython, Sender):
    """External Python-Proton sender client."""

    # Just to enforce implementation being used
    _command: PythonSenderClientCommand

    def __init__(self, name: str, node: Node, **kwargs) -> None:
        super(SenderPython, self).__init__(name, node, **kwargs)

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
    ) -> ClientCommandBase:
        return PythonSenderClientCommand(
            stdout=stdout,
            stderr=stderr,
            daemon=daemon,
            timeout=timeout,
            encoding=encoding,
        )

    def _send(self, message: Message, **kwargs) -> None:
        self._command.message.msg_content = message.application_data
        self.execution = self.node.execute(self.command)
