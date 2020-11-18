"""
Ansible Node implementation of Node Interface.
"""

import logging
import time

from timeit import default_timer
from docker.errors import APIError, NotFound
from docker.models.containers import Container

from iqa.system.executor.docker.executor_docker import ExecutorDocker
from iqa.system.node.node import Node
from iqa.utils.docker_util import get_container, get_container_ip

logger = logging.getLogger()


class NodeDocker(Node):
    """Docker implementation for Node interface."""

    def __init__(
            self, hostname: str,
            executor: ExecutorDocker,
            docker_host: str = '',
            docker_network: str = '',
            ip: str = ''
    ) -> None:

        logger.info('Initialization of NodeDocker: %s' % hostname)
        self.hostname: str = hostname
        self.docker_network: str = docker_network
        self.container: Container = self._get_container(docker_host=docker_host)
        super(NodeDocker, self).__init__(hostname, executor, ip)

    def ping(self) -> bool:
        """Send ping to Docker node"""
        try:
            return self.container.attrs['State']['Running']
        except Exception or APIError or NotFound:
            logger.info(
                'Unable to get container status for: %s' % self.container.name
            )
            return False

    def _get_container(self, timeout=3.0, pause=0.5, docker_host: str = ''):
        """Get Container instance"""
        logger.debug('Retrieving %s container\'s host of %s docker host.' % (self.hostname, self.docker_network))
        ref = default_timer()
        now = ref
        while (now - ref) < timeout:
            try:
                container = get_container(
                    name=self.hostname,
                    docker_host=docker_host
                )
                return container
            except Exception or APIError or NotFound:
                logger.info(
                    'Unable to get docker container for: %s' % self.hostname
                )
            time.sleep(pause)
            now = default_timer()

        raise Exception("Timeout reached while waiting on!")

    def get_ip(self) -> None:
        """Get host of Docker node"""
        logger.debug('Retrieving %s container\'s host for network: %s' % (self.hostname, self.docker_network))
        try:
            self.ip: str = get_container_ip(
                container=self.container,
                network_name=self.docker_network
            )
        except Exception or APIError or NotFound:
            logger.info(
                'Unable to get container host for: %s' % self.hostname
            )
