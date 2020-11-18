from .connection import ConnectionAsyncSsh
from iqa.system.executor.base.executor import ExecutorBase

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional
    from iqa.system.command.command_base import CommandBase


class ExecutorAsyncSsh(ExecutorBase):
    """ Executor implementation for AsyncSSH client
    """
    def __init__(self, host: str, port: int = 22, user: str = 'root', password: Optional[str] = None, **kwargs) -> None:

        super(ExecutorAsyncSsh).__init__(**kwargs)
        self._host: str = host
        self._port: int = port
        self._user: str = user
        self._password: Optional[str] = password
        self.connection: Optional[ConnectionAsyncSsh] = None

    async def __aenter__(self):
        await self._connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._disconnect()

    async def _disconnect(self) -> None:
        """ Close connection """
        self._logger.info("Host %s: Closing connection", self.host)
        await self.connection.disconnect()

    async def _connect(self) -> None:
        """ Establish connection """
        self._logger.info("Host %s: Establishing connection", self.host)
        con = ConnectionAsyncSsh(
            host=self._host,
            port=self._port,
            username=self._user,
            password=self._password,
            known_hosts=None,
            client_keys=None
        )
        self.connection = await con.connect()

    def _execute(self, command: CommandBase):
        cmd = " ".join(command.args)
        return self._send(cmd)

    async def _send(self, cmd: str) -> None:
        """ Send command to stream """
        cmd = cmd.rstrip("\n")
        await self.connection.run(cmd)

    @property
    def host(self) -> str:
        """ Return the host address """
        return self.connection.host
