from typing import TYPE_CHECKING

from iqa.system.command.command_base import CommandBase

if TYPE_CHECKING:
    from typing import Optional, List, Any, Union, Dict
    from os import PathLike


class CommandBaseAnsible(CommandBase):
    """
    Simple extension of the Command class that can be used along with the
    ExecutorAnsible in which this command can also provide the ansible
    module to use. When doing so, the 'ansible_args' parameter will be a
    single string containing exactly the same args syntax used in the CLI,
    when calling the respective module. Example: 'filter=ansible_hostname'.
    """

    def __init__(
            self,
            args: Optional[List[str]] = None,
            ansible_args: Optional[List[str]] = None,
            path_to_exec: Optional[Union[str, bytes, PathLike]] = "ansible",
            ansible_module: str = 'raw',
            stdout: bool = False,
            stderr: bool = False,
            daemon: bool = False,
            timeout: int = 0,
            wait_for: bool = False,
            encoding: str = 'utf-8',
            env: Optional[Dict[str, Any]] = None,
            **kwargs: Dict[str, Any]
    ) -> None:
        # dump arguments into dictionary
        inputs = locals()
        # remove self and kwargs variables as they would mess things up
        del inputs['self']
        del inputs['ansible_args']
        del inputs['kwargs']
        # update kwargs to pass in super().__init__()
        kwargs.update(inputs)

        super(CommandBaseAnsible, self).__init__(args, **kwargs)
        self.ansible_module: str = ansible_module
        self._ansible_args: List[str] = ansible_args if ansible_args is not None else []

    @property
    def ansible_args(self) -> List[str]:
        return self._ansible_args

    @ansible_args.setter
    def ansible_args(self, args: List[str]) -> None:
        self._ansible_args = args

    @staticmethod
    def convert(
            c: CommandBase,
            path_to_exec: Optional[Union[str, bytes, PathLike]] = "ansible",
            ansible_args: Optional[List[str]] = None,
            ansible_module: Optional[str] = None
    ) -> 'CommandBaseAnsible':
        if isinstance(c, CommandBaseAnsible):
            c.ansible_args = ansible_args
            if c.path_to_exec is None:
                c.path_to_exec = path_to_exec
            return c

        args: List[str] = [c.path_to_exec]
        args.extend(c.args)
        if ansible_args is None:
            ansible_args: Optional[List[str]] = getattr(c, 'ansible_args', None)
        if ansible_module is None:
            ansible_module: str = getattr(c, 'ansible_module', 'raw')
        stdout: bool = c.stdout
        stderr: bool = c.stderr
        daemon: bool = c.damon
        wait_for: bool = c.wait_for
        timeout: int = c.timeout
        encoding: str = c.encoding
        env: dict = c.env

        # dump collected variables into dictionary
        inputs = locals()
        # remove original command base variable
        del inputs['c']

        return CommandBaseAnsible(**inputs)
