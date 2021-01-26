import logging

import asyncssh
from asyncssh import SSHClientConnection, EXTENDED_DATA_STDERR
from asyncssh.stream import SSHClientStreamSession, SSHWriter, SSHReader

from iqa.abstract.connection import ConnectionBase
from iqa.system.executor.asyncssh.session import AsyncSSHSession
from iqa.utils.exceptions import IQAHostDisconnectException

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, List, Coroutine


class ConnectionAsyncSsh(ConnectionBase):
    """ SSH Connection Class """

    def __init__(self, host: str, port: int = 22, **kwargs) -> None:
        super().__init__(host, port, **kwargs)
        self._conn_dict: dict = kwargs
        self._conn: Optional[SSHClientConnection] = None
        self.sessions: List[AsyncSSHSession] = []

    async def connect(self) -> None:
        """ Establish the SSH connection """
        self._logger.info("Host %s: Establishing SSH connection on port %s", self._host, self._port)
        try:
            self._conn = await asyncssh.connect(
                self._host, self._port, **self._conn_dict,
            )
        except asyncssh.DisconnectError as error:
            raise IQAHostDisconnectException(self._host, error.reason)

    async def new_session(self, *args, **kwargs) -> AsyncSSHSession:
        """ Start interactive-session (shell) """

        session = AsyncSSHSession()

        chan, sess = await self._conn.create_session(
            SSHClientStreamSession,
            term_type="vt100",
            term_size=(2147483647, 2147483647),
            *args, **kwargs
        )
        session.stdin = SSHWriter(sess, chan)
        session.stdout = SSHReader(sess, chan)
        session.stderr = SSHReader(sess, chan, EXTENDED_DATA_STDERR)
        self.sessions.append(session)

        return session

    async def run(self, command: str) -> 'Coroutine':
        self._logger.info('Host {}: Running command "{}"'.format(self._host, command))
        result = await self._conn.run(command, check=True)
        self._logger.info('Host {}: command result"{}"'.format(self._host, result.stdout))
        return result

    async def disconnect(self) -> None:
        """ Gracefully close the SSH connection """
        self._logger.info("Host %s: Disconnecting", self.host)
        self._conn.close()
        await self._conn.wait_closed()

    @property
    def host(self) -> str:
        return self._host
