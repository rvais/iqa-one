from abc import ABC
from iqa.components.implementations.clients.external.client_external import ClientExternal
from iqa.components.abstract.network.protocol.protocol import Protocol
from urllib.parse import urlparse, urlunparse, unquote

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from iqa.system.command.new_command_base import CommandBase
    from typing import Optional, Union, List
    from iqa.system.node.base.node import Node
    from os import PathLike


class ClientJava(ClientExternal, ABC):
    """Java Qpid JMS client (base abstract class)."""
    default_version: str = '1.0.1'

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
        super(ClientJava, self).__init__(**kwargs)

    @property
    def implementation(self) -> str:
        return 'java'

    @property
    def supported_protocols(self) -> 'List[Protocol]':
        return [Protocol.AMQP10]

    def _set_url(self, url: str) -> None:
        p_url = urlparse(url)
        self._command.options.broker = '{}://{}:{}'.format(
            p_url.scheme, p_url.hostname, p_url.port
        )
        self._command.options.address = urlunparse(
            (
                '',
                '',
                p_url.path or '',
                p_url.params or '',
                p_url.query or '',
                p_url.fragment or '',
            )
        )

        # Java client expects unquoted username and passwords
        if p_url.username:
            self._command.options.conn_username = unquote(p_url.username)
        if p_url.password:
            self._command.options.conn_password = unquote(p_url.password)

    def _new_command(
        self,
        stdout: bool = False,
        stderr: bool = False,
        daemon: bool = False,
        timeout: int = 0,
        encoding: str = 'utf-8',
    ) -> 'CommandBase':
        """
        Must return a ClientCommand implementation for the command that is related
        with the concrete client.
        :param stdout:
        :param stderr:
        :param daemon:
        :param timeout:
        :param encoding:
        :return:
        """
        raise NotImplementedError

    def set_auth_mechs(self, mechs: 'Optional[str]' = None) -> None:
        """
        Implementing clients must know how to adjust mechanisms (if supported).
        :param mechs:
        :return:
        """
        if mechs is not None:
            self.command.options.conn_auth_mechanisms = mechs

    def set_ssl_auth(
        self,
        pem_file: 'Optional[str]' = None,
        key_file: 'Optional[str]' = None,
        keystore: 'Optional[str]' = None,
        keystore_pass: 'Optional[str]' = None,
        keystore_alias: 'Optional[str]' = None,
    ) -> None:
        """
        Allows implementing clients to use the SSL credentials according to each implementing model.
        :param pem_file:
        :param key_file:
        :param keystore:
        :param keystore_pass:
        :param keystore_alias:
        :return:
        """
        self._command.options.conn_ssl_keystore_location = keystore
        self._command.options.conn_ssl_keystore_password = keystore_pass
        self._command.options.conn_ssl_key_alias = keystore_alias
        self._command.options.conn_ssl_verify_host = 'false'
        self._command.options.conn_ssl_trust_all = 'true'
