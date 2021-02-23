from iqa.abstract.client.receiver import Receiver
from iqa.components.implementations.clients.external.java.client import ClientJava

from typing import TYPE_CHECKING

from iqa.components.implementations.clients.external.java.command.new_java_command import JavaReceiverCommand
import os.path

if TYPE_CHECKING:
    from os import PathLike
    from typing import Optional, Union
    from iqa.abstract.listener import Listener
    from iqa.system.node.base.node import Node


class ReceiverJava(ClientJava, Receiver):
    """External Java Qpid JMS receiver client."""

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
        super(ReceiverJava, self).__init__(**kwargs)

    def _new_command(
        self,
        stdout: bool = True,
        stderr: bool = True,
        daemon: bool = False,
        timeout: int = ClientJava.TIMEOUT,
        encoding: str = 'utf-8',
    ) -> JavaReceiverCommand:
        path_to_exec: 'Union[str, bytes, PathLike]' = os.path.join(self.path_to_exec, self.name)
        return JavaReceiverCommand(
            path_to_exec=path_to_exec,
            stdout=stdout,
            stderr=stderr,
            daemon=daemon,
            timeout=timeout,
            encoding=encoding,
        )

    def _receive(self) -> None:
        self.execution = self.node.execute(self.command)

    def set_endpoint(self, listener: 'Listener') -> None:
        raise NotImplementedError

    def connect(self):
        raise NotImplementedError
