from iqa.components.implementations.clients.external.client_external import ClientExternal
from iqa.components.abstract.network.protocol.protocol import Protocol

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Optional, List
    from iqa.abstract.listener import Listener
    from iqa.system.node.base.node import Node
    from iqa.components.implementations.clients.external.command.client_command import ClientCommandBase


class ClientNodeJS(ClientExternal):
    """NodeJS RHEA client"""

    supported_protocols: 'List[Protocol]' = [Protocol.AMQP10]
    implementation: str = 'nodejs'
    version: str = '1.0.1'

    def __init__(self, name: str, node: 'Node', **kwargs):
        super(ClientNodeJS, self).__init__(name, node, **kwargs)

    def _new_command(
        self,
        stdout: bool = False,
        stderr: bool = False,
        daemon: bool = False,
        timeout: int = 0,
        encoding: str = 'utf-8',
    ) -> 'ClientCommandBase':
        pass

    def _set_url(self, url: str):
        pass

    def set_auth_mechs(self, mechs: str):
        pass

    def set_ssl_auth(
        self,
        pem_file: 'Optional[str]' = None,
        key_file: 'Optional[str]' = None,
        keystore: 'Optional[str]' = None,
        keystore_pass: 'Optional[str]' = None,
        keystore_alias: 'Optional[str]' = None,
    ):
        pass

    def set_endpoint(self, listener: 'Listener'):
        pass

    def connect(self) -> bool:
        raise NotImplementedError
