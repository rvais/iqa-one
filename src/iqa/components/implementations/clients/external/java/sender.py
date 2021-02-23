from typing import TYPE_CHECKING
from urllib.parse import urlparse, urlunparse, unquote

from iqa.abstract.client.sender import Sender
from iqa.components.implementations.clients.external.java.client import ClientJava
from iqa.components.implementations.clients.external.java.command.new_java_command import JavaSenderCommand
import os.path

if TYPE_CHECKING:
    from os import PathLike
    from typing import Optional, Union
    from iqa.system.node.base.node import Node
    from iqa.abstract.listener import Listener
    from iqa.abstract.message.message import Message


class SenderJava(ClientJava, Sender):
    """External Java Qpid JMS sender client."""

    def __init__(
        self,
        path_to_exec: 'Optional[Union[str, bytes, PathLike]]' = None,
        name: 'Optional[str]' = None,
        node: 'Optional[Node]' = None,
        **kwargs
    ) -> None:
        # dump arguments into dictionary
        inputs = locals()
        # remove self and kwargs variables as they would mess things up
        del inputs['self']
        del inputs['kwargs']
        # update kwargs to pass in super().__init__()
        if 'version' not in kwargs.keys():
            inputs['version'] = self.default_version
        kwargs.update(inputs)
        super(SenderJava, self).__init__(**kwargs)

    def _new_command(
        self,
        stdout: bool = True,
        stderr: bool = True,
        daemon: bool = True,
        timeout: int = ClientJava.TIMEOUT,
        encoding: str = 'utf-8',
    ) -> JavaSenderCommand:
        path_to_exec: 'Union[str, bytes, PathLike]' = os.path.join(self.path_to_exec, self.name)
        return JavaSenderCommand(
            path_to_exec=path_to_exec,
            stdout=stdout,
            stderr=stderr,
            daemon=daemon,
            timeout=timeout,
            encoding=encoding,
        )

    def _send(self, message: 'Message', **kwargs) -> None:
        self._command.options.msg_content = message.application_data
        self.execution = self.node.execute(self.command)

    def connect(self) -> bool:
        raise NotImplementedError

    def set_endpoint(self, listener: 'Listener') -> None:
        raise NotImplementedError
