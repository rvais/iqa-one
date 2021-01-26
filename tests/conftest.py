import logging
import os
import pytest

# from iqa.system.executor.docker.executor_docker import ExecutorDocker
# from iqa.system.node import NodeDocker
# from iqa.system.node.node import Node

logging.basicConfig(level=logging.DEBUG)


# @pytest.fixture
# def node(docker_services) -> Node:
#     executor: ExecutorDocker = ExecutorDocker(
#         container_name='sshd-container'
#     )
#     node: NodeDocker = NodeDocker(hostname="sshd-container", executor=executor)
#     return node
#
#
# @pytest.fixture(scope="session")
# def docker_compose_file(pytestconfig):
#     dir_path = os.path.dirname(os.path.realpath(__file__))
#     return os.path.join(str(dir_path), "docker-compose.yml")
