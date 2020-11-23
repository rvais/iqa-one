import logging
from collections import namedtuple
from typing import Optional

import proton
from proton.reactor import Url, SSLDomain
from proton.utils import BlockingConnection, SyncRequestResponse

from iqa.components.routers.dispatch.dispatch import Dispatch


class RouterQuery(object):
    """
    Provides methods that can be used to query the Dispatch Router.
    Connections are closed after each query.
    """

    def __init__(
        self, host: str = '0.0.0.0', port: int = 5672, router: Dispatch = None
    ) -> None:

        self._logger: logging.Logger = logging.getLogger(self.__module__)
        self.port: int = port
        self.host: str = host
        self._router: Optional[Dispatch] = router
        self._connection_options: dict = {
            'sasl_enabled': False,
            'ssl_domain': None,
            'allow_insecure_mechs': True,
            'user': None,
            'password': None,
        }

        if self._router:
            # Enable SASL when credentials provided
            self._connection_options['sasl_enabled'] = (
                self._router.has_ssl_keys() or self._router.has_credentials()
            )

            # If SSL certificates provided, use them
            if self._router.has_ssl_keys():
                ssl_domain: SSLDomain = SSLDomain(SSLDomain.MODE_CLIENT)
                ssl_domain.set_credentials(
                    self._router.pem_file,
                    self._router.key_file,
                    self._router.key_password,
                )
                self._connection_options['ssl_domain'] = ssl_domain

            # If User and Password provided
            if self._router.has_credentials():
                self._connection_options['user'] = self._router.user
                self._connection_options['password'] = self._router.password

    def query(self, entity_type: str = 'org.apache.qpid.dispatch.router.node') -> list:
        """
        Queries the related router instance, retrieving information for
        the provided Entity Type. The result is an array of a named tuple,
        whose fields are the attribute names returned by the router.
        In example, if querying entity type: org.apache.qpid.dispatch.allocator,
        the results can be accessed as: result.typeName, result.typeSize, ...
        same names returned by the router.
        :param entity_type:
        :return:
        """
        # Scheme to use
        scheme: str = 'amqp'
        if self._connection_options['ssl_domain']:
            scheme = 'amqps'

        # URL to test
        url: Url = Url('%s://%s:%s/$management' % (scheme, self.host, self.port))
        self._logger.info(
            'Querying router at: %s://%s:%s/$management'
            % (scheme, self.host, self.port)
        )

        # Proton connection
        self._logger.debug('Connection options: %s' % self._connection_options)
        connection: BlockingConnection = BlockingConnection(
            url, **self._connection_options
        )

        # Proton sync client
        client: SyncRequestResponse = SyncRequestResponse(connection, url.path)

        # Request message object
        request: proton.Message = proton.Message()
        request.properties = {
            u'operation': u'QUERY',
            u'entityType': u'%s' % entity_type,
        }
        request.body = {u'attributeNames': []}

        # Sending the request
        response: client.call = client.call(request)

        # Closing connection
        client.connection.close()

        # Namedtuple that represents the query response from the router
        # so fields can be read based on their attribute names.
        RouterQueryResults = namedtuple('RouterQueryResults', response.body['attributeNames'])  # type: ignore
        records: list = []

        for record in response.body['results']:
            records.append(RouterQueryResults(*record))

        return records

    # Entities that can be queried
    def listener(self) -> list:
        return self.query(entity_type='org.apache.qpid.dispatch.listener')

    def connector(self) -> list:
        return self.query(entity_type='org.apache.qpid.dispatch.connector')

    def router(self) -> list:
        return self.query(entity_type='org.apache.qpid.dispatch.router')

    def address(self) -> list:
        return self.query(entity_type='org.apache.qpid.dispatch.router.address')

    def config_address(self) -> list:
        return self.query(entity_type='org.apache.qpid.dispatch.router.config.address')

    def config_autolink(self) -> list:
        return self.query(entity_type='org.apache.qpid.dispatch.router.config.autoLink')

    def config_linkroute(self) -> list:
        return self.query(
            entity_type='org.apache.qpid.dispatch.router.config.linkRoute'
        )

    def config_exchange(self) -> list:
        return self.query(entity_type='org.apache.qpid.dispatch.router.config.exchange')

    def config_binding(self) -> list:
        return self.query(entity_type='org.apache.qpid.dispatch.router.config.binding')

    def node(self) -> list:
        return self.query(entity_type='org.apache.qpid.dispatch.router.node')

    def ssl_profile(self) -> list:
        return self.query(entity_type='org.apache.qpid.dispatch.sslProfile')

    def connection(self) -> list:
        return self.query(entity_type='org.apache.qpid.dispatch.connection')

    def allocator(self) -> list:
        return self.query(entity_type='org.apache.qpid.dispatch.allocator')

    def log_stats(self) -> list:
        return self.query(entity_type='org.apache.qpid.dispatch.logStats')

    def router_link(self) -> list:
        return self.query(entity_type='org.apache.qpid.dispatch.router.link')

    def policy(self) -> list:
        return self.query(entity_type='org.apache.qpid.dispatch.policy')

    def vhost(self) -> list:
        return self.query(entity_type='org.apache.qpid.dispatch.vhost')

    def vhost_user_group_settings(self) -> list:
        return self.query(entity_type='org.apache.qpid.dispatch.vhostUserGroupSettings')

    def vhost_stats(self) -> list:
        return self.query(entity_type='org.apache.qpid.dispatch.vhostStats')

    def auth_service_plugin(self) -> list:
        return self.query(entity_type='org.apache.qpid.dispatch.authServicePlugin')

    def configuration_entity(self) -> list:
        return self.query(entity_type='org.apache.qpid.dispatch.configurationEntity')

    def log(self) -> list:
        return self.query(entity_type='org.apache.qpid.dispatch.log')

    def console(self) -> list:
        return self.query(entity_type='org.apache.qpid.dispatch.console')

    def management(self) -> list:
        return self.query(entity_type='org.apache.qpid.dispatch.management')
