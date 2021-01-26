from typing import TYPE_CHECKING

from iqa.abstract.client.sender import Sender
from iqa.components.implementations.clients.external.command.client_command import ClientCommandBase
from iqa.components.implementations.clients.external.python.client import ClientPython
from iqa.components.implementations.clients.external.python.command.python_commands import (
    PythonSenderClientCommand,
)

if TYPE_CHECKING:
    from os import PathLike
    from typing import Optional, Any
    from iqa.system.node.base.node import Node
    from iqa.abstract.message.message import Message


class SenderPython(ClientPython, Sender):
    """External Python-Proton sender client."""

    # Just to enforce implementation being used
    _command: PythonSenderClientCommand
    path_to_exec: 'Optional[PathLike[Any]]'

    def __init__(self, name: str, node: 'Node', path_to_exec: 'Optional[PathLike[Any]]' = None, **kwargs) -> None:
        super(SenderPython, self).__init__(name, node, **kwargs)
        self.path_to_exec = path_to_exec

    def _set_url(self, url: str) -> None:
        self._command.control.broker_url = url

    def set_auth_mechs(self, mechs: str) -> None:
        self._command.connection.conn_allowed_mechs = mechs

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

    def _send(self, message: 'Message', **kwargs) -> None:
        self._command.message.msg_content = message.application_data
        self.execution = self.node.execute(self.command)
