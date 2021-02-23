from typing import TYPE_CHECKING
from urllib.parse import urlparse, unquote

from iqa.components.implementations.clients.external.java.command.new_java_command import JavaConnectorCommand
from iqa.components.implementations.clients.external.java.client import ClientJava
import os.path

if TYPE_CHECKING:
    from os import PathLike
    from typing import Optional, Any, Union
    from iqa.abstract.listener import Listener
    from iqa.system.node.base.node import Node


class ConnectorJava(ClientJava):
    """External Java Qpid JMS connector client."""

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
        super(ConnectorJava, self).__init__(**kwargs)

    def _set_url(self, url: str) -> None:
        p_url = urlparse(url)
        self.command.control.broker = '{}://{}:{}'.format(
            p_url.scheme or 'amqp', p_url.hostname or '127.0.0.1', p_url.port or '5672'
        )

        # Java client expects unquoted username and passwords
        if p_url.username:
            self.command.connection.conn_username = unquote(p_url.username)
        if p_url.password:
            self.command.connection.conn_password = unquote(p_url.password)

    def _new_command(
        self,
        stdout: bool = True,
        stderr: bool = True,
        daemon: bool = True,
        timeout: int = ClientJava.TIMEOUT,
        encoding: str = 'utf-8',
    ) -> JavaConnectorCommand:
        path_to_exec: 'Union[str, bytes, PathLike]' = os.path.join(self.path_to_exec, self.name)
        return JavaConnectorCommand(
            path_to_exec=path_to_exec,
            stdout=stdout,
            stderr=stderr,
            daemon=daemon,
            timeout=timeout,
            encoding=encoding,
        )

    def set_endpoint(self, listener: 'Listener') -> None:
        raise NotImplementedError

    def connect(self):
        raise NotImplementedError
