from iqa.system.executor.asynclocalhost.execution import ExecutionAsyncio
from iqa.system.command.command_base import CommandBase

# from typing import TYPE_CHECKING
#
# if TYPE_CHECKING:
#     from typing import Optional


class ExecutionDocker(ExecutionAsyncio):
    def _run(self) -> None:
        pass

#     def _docker_command(self, docker_host, docker_args, command):
#         # define environment when docker_host provided
#         env = dict()
#         if docker_host:
#             env['DOCKER_HOST'] = docker_host
#
#         command_builder = CommandBase(args=docker_args, stdout=command.stdout, stderr=command.stderr,
#                                       timeout=command.timeout, encoding=command.encoding)
#
#         execution = ExecutionAsyncio(command=command_builder,  env=env)
#         return execution

    async def wait(self) -> None:
        pass

    def is_running(self) -> bool:
        raise NotImplemented

    def completed_successfully(self) -> bool:
        raise NotImplemented

    def on_timeout(self) -> None:
        pass

    def terminate(self) -> None:
        pass
