
"""
Utility classes to retrieve information from local docker environment.
"""
import logging
import os

import docker
from docker.errors import APIError, NotFound
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional
    from docker.models.containers import Container

logger: logging.Logger = logging.getLogger(__name__)

_env: dict = os.environ.copy()


CONTAINER_STATUS_RUNNING: str = 'running'
CONTAINER_STATUS_EXITED: str = 'exited'


def get_client(docker_host: Optional[str] = None):
    if docker_host:
        _env['DOCKER_HOST'] = docker_host
    return docker.from_env(environment=_env)


def get_container(name: str, docker_host: Optional[str] = None) -> Container:
    """
    Returns the container instance for the given name.
    A docker.errors.NotFound exception is raised in case the given
    container does not exist.
    :param docker_host:
    :param name:
    :return:
    """
    docker_host = docker_host if docker_host is not None else ''
    client = get_client(docker_host=docker_host)
    container = client.containers.get(name)
    return container


def get_container_ip(container: Container, network_name: Optional[str] = None) -> str:
    """
    Returns the IPAddress assigned to the given container name (on the given network).
    :param container:
    :param network_name:
    :return:
    """
    try:
        if network_name:
            ip_addr: str = container.attrs['NetworkSettings']['Networks'][network_name]['IPAddress']
        else:
            ip_addr: str = list(container.attrs['NetworkSettings']['Networks'].values())[0]['IPAddress']

        logger.debug('Container [%s] - IP [%s]' % (container.name, ip_addr))

    except Exception or APIError or NotFound:
        logger.debug(
            'Unable to determine IP for container: %s'
            % container.name
        )
        ip_addr = ''

    return ip_addr

