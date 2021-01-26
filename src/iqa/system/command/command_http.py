from typing import TYPE_CHECKING
from iqa.system.command.command_base import CommandBase
from requests.utils import quote

if TYPE_CHECKING:
    from typing import Optional, List, Union, Tuple
    from os import PathLike


class CommandHTTP(CommandBase):
    """
    Represents a command that can be executed against different
    executors, behaving similarly across them.
    """

    __misc_key__ = "misc"

    def __init__(
        self,
        args: 'Optional[Union[List[str], List[Tuple], List[Union[Tuple, str]]]]' = None,
        method_post: bool = False,
        url: 'Optional[str]' = None,
        uses_ssl: bool = False,
        stdout: bool = False,
        stderr: bool = False,
        daemon: bool = True,
        timeout: int = 0,
        encoding: str = 'utf-8',
        wait_for: bool = False,
        env: 'Optional[dict]' = None,
        path_to_exec: 'Optional[Union[str, bytes, PathLike]]' = None,
        **kwargs
    ) -> None:
        """
        Creates an instance of a Command representation that can be passed to
        an ExecutorBase instance.
        :param args: List of arguments that compose the command to be executed
        :param path_to_exec: Path to executable represented by this command,
        if applicable.
        :param stdout: If True stdout will be available at the
        resulting Execution instance.
        :param stderr: If True stderr will be available at the
        resulting Execution instance.
        :param timeout: If a positive number provided, the process
        will be terminated on timeout and the registered timeout
        callbacks will be invoked.
        :param encoding: Encoding when reading stdout and stderr.
        """
        # override stdout and stderr settings
        stdout = False
        stderr = False
        # dump arguments into dictionary
        inputs = locals()

        # reuse path_to_exec as URL since it can contain string and it is technically PathLike
        path_to_exec: Optional[Union[str, bytes, PathLike]] = kwargs['path_to_exec']
        if url is not None:
            path_to_exec = url

        # remove self, kwargs and other variables that would mess things up
        del inputs['self']
        del inputs['args']
        del inputs['kwargs']
        del inputs['use_ssl']
        del kwargs['path_to_exec']
        # update inputs with kwargs to pass in super().__init__(), but keep kwargs intact
        inputs.update(kwargs)

        if url is not None:
            path_to_exec = url

        super(CommandHTTP).__init__(path_to_exec=path_to_exec, **inputs)
        self._ssl = uses_ssl
        self._post: bool = method_post
        self._args: List[Union[Tuple[str, str], str]] = []
        self._data: dict = {self.__misc_key__: []}

        if not isinstance(args, list):
            args = [args]

        # Process list of arguments
        for argument in args:
            if argument is str:
                argument = tuple(argument.split('=', 1))

            if isinstance(argument, tuple) and len(argument) == 2:
                self._args.append(argument)

            elif isinstance(argument, tuple) and len(argument) == 1:
                argument, = argument
                self._data[self.__misc_key__].append(argument)
            else:
                self._data[self.__misc_key__].append(argument)

        self._data.update(kwargs)

    def __str__(self) -> str:
        args = ["%s=%s" % (quote(a, safe=''), quote(b, safe='')) for (a, b) in self.args]
        url = self.url if self.url is not None else ''
        return "%s?%s" % (url, "&".join(args))

    @property
    def args(self) -> 'List[Tuple[str, str]]':
        return self._args.copy()

    @args.setter
    def args(self, args: 'List[Tuple[str, str]]') -> None:
        self._args = args

    @property
    def url(self) -> 'Optional[str]':
        return self.path_to_exec

    @url.setter
    def url(self, url: str) -> None:
        self.path_to_exec = url

    @property
    def method_post(self) -> bool:
        return self._post

    @method_post.setter
    def method_post(self, method: bool) -> None:
        self._post = method

    @property
    def data(self) -> dict:
        misc: List = self._data[self.__misc_key__]
        if isinstance(misc, list) and not misc:  # implicit boolean emptiness check
            del self._data[self.__misc_key__]

        data = self._data.copy()
        data.update(self._args)
        return data

    @staticmethod
    def convert(
        c: CommandBase,
        method_post: bool = False,
        url: 'Optional[str]' = None,
        **kwargs
    ) -> 'CommandHTTP':
        if isinstance(c, CommandHTTP):
            c.url = url
            c.method_post = method_post

        args: List[str] = c.args
        stdout: bool = c.stdout
        stderr: bool = c.stderr
        daemon: bool = c.damon
        timeout: int = c.timeout
        encoding: str = c.encoding
        wait_for: bool = c.wait_for
        env: dict = c.env

        # dump collected variables into dictionary
        inputs = locals()
        # remove original command base variable
        del inputs['c']
        del inputs['kwargs']

        inputs.update(kwargs)

        return CommandHTTP(**inputs)
