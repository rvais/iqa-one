import os

from iqa.system.executor.base.executor import ExecutorBase
from iqa.system.executor.asynclocalhost.execution import ExecutionAsyncio
from iqa.system.command.command_base import CommandBase

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, List

"""
Executor instance that runs a given Command instance using
Docker CLI against a pre-defined container (by name or id).
"""


class ExecutorDocker(ExecutorBase):
    """
    Executor that runs Command instances in a Docker container.
    """

    implementation: str = 'docker'
    name: str = 'Docker CLI executor'

    def __init__(
        self,
        container_name: str,
        user: Optional[str] = None
    ):
        super(ExecutorDocker, self).__init__()
        self.container_name: str = container_name
        self.user: str = user
        self.docker_host: str = ''
        self._command: Optional[CommandBase] = None

    def _command_inside_container(self, command: Optional[CommandBase] = None, user: Optional[str] = None):

        docker_args: List[str] = []

        if user:
            docker_args.extend(['-u', user])
        elif self.user:
            docker_args.extend(['-u', self.user])

        docker_args.append(self.container_name)

        docker_args.extend(['sh', '-c', '"'])
        docker_args += command.args
        docker_args.append('"')
        inside_command = self.docker_command(docker_command='exec', docker_args=docker_args)
        return inside_command

    def docker_command(
        self,
        docker_command: Optional[str] = None,
        docker_args: Optional[List[str]] = None,
        docker_options: Optional[List[str]] = None
    ):
        """

        Args:
            docker_args: Optional list of args used for alternative to 'command'
            docker_command:
                Management Commands:
                  builder     Manage builds
                  config      Manage Docker configs
                  container   Manage containers
                  context     Manage contexts
                  engine      Manage the docker engine
                  image       Manage images
                  network     Manage networks
                  node        Manage Swarm nodes
                  plugin      Manage plugins
                  secret      Manage Docker secrets
                  service     Manage services
                  stack       Manage Docker stacks
                  swarm       Manage Swarm
                  system      Manage Docker
                  trust       Manage trust on Docker images
                  volume      Manage volumes

                Commands:
                  attach      Attach local standard input, output, and error streams to a running container
                  build       Build an image from a Dockerfile
                  commit      Create a new image from a container's changes
                  cp          Copy files/folders between a container and the local filesystem
                  create      Create a new container
                  diff        Inspect changes to files or directories on a container's filesystem
                  events      Get real time events from the server
                  exec        Run a command in a running container
                  export      Export a container's filesystem as a tar archive
                  history     Show the history of an image
                  images      List images
                  import      Import the contents from a tarball to create a filesystem image
                  info        Display system-wide information
                  inspect     Return low-level information on Docker objects
                  kill        Kill one or more running containers
                  load        Load an image from a tar archive or STDIN
                  login       Log in to a Docker registry
                  logout      Log out from a Docker registry
                  logs        Fetch the logs of a container
                  pause       Pause all processes within one or more containers
                  port        List port mappings or a specific mapping for the container
                  ps          List containers
                  pull        Pull an image or a repository from a registry
                  push        Push an image or a repository to a registry
                  rename      Rename a container
                  restart     Restart one or more containers
                  rm          Remove one or more containers
                  rmi         Remove one or more images
                  run         Run a command in a new container
                  save        Save one or more images to a tar archive (streamed to STDOUT by default)
                  search      Search the Docker Hub for images
                  start       Start one or more stopped containers
                  stats       Display a live stream of container(s) resource usage statistics
                  stop        Stop one or more running containers
                  tag         Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE
                  top         Display the running processes of a container
                  unpause     Unpause all processes within one or more containers
                  update      Update configuration of one or more containers
                  version     Show the Docker version information
                  wait        Block until one or more containers stop, then print their exit codes

            docker_args:
            command:
            docker_options:

        Returns:

        """
        # define environment when docker_host provided

        env = {**os.environ}
        if self.docker_host:
            env['DOCKER_HOST'] = self.docker_host

        # start with building command
        docker_cmd = ['docker']
        if docker_options:
            docker_cmd.extend(docker_options)

        if docker_command:
            docker_cmd.append(docker_command)

        if docker_args:
            docker_cmd.extend(docker_args)

        docker_command_builder = CommandBase(args=docker_cmd, env=env)

        return docker_command_builder

    async def _execute(
        self,
        command: Optional[CommandBase] = None,
        user: Optional[str] = None,
        inside_container: bool = True
    ) -> ExecutionAsyncio:

        if inside_container:
            cmd = self._command_inside_container(command, user)
        else:
            cmd = command

        execution = ExecutionAsyncio(cmd)
        await execution.run()

        return execution
