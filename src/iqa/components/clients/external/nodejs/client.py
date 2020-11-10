from iqa.abstract.listener import Listener
from iqa.components.clients.external import ClientExternal
from iqa.components.clients.external.command.client_command import ClientCommandBase
from iqa.system.node.node import Node


class ClientNodeJS(ClientExternal):
    """NodeJS RHEA client"""

    supported_protocols: list = ["AMQP10"]
    implementation: str = 'nodejs'
    version: str = '1.0.1'

    def __init__(self, name: str, node: Node, **kwargs):
        super(ClientNodeJS, self).__init__(name, node, **kwargs)

    def _new_command(
        self,
        stdout: bool = False,
        stderr: bool = False,
        daemon: bool = False,
        timeout: int = 0,
        encoding: str = 'utf-8',
    ) -> ClientCommandBase:
        pass

    def _set_url(self, url: str):
        pass

    def set_auth_mechs(self, mechs: str):
        pass

    def set_ssl_auth(
        self,
        pem_file: str = None,
        key_file: str = None,
        keystore: str = None,
        keystore_pass: str = None,
        keystore_alias: str = None,
    ):
        pass

    def set_endpoint(self, listener: Listener):
        pass

    def connect(self):
        pass
