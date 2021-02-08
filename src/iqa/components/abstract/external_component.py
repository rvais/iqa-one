from abc import ABC
from typing import TYPE_CHECKING

from iqa.components.abstract.component import Component

if TYPE_CHECKING:
    from typing import Union, Optional
    from iqa.system.node.base.node import Node
    from os import PathLike


class ExternalComponent(Component, ABC):
    """
    Class that represents abstract of component external to IQA, which usually needs to be executed es external process.
    Executor may therefore need path to such process/executable/script unless it's default system command like 'ls' for
    example.
    """

    def __init__(
            self,
            path_to_exec: 'Optional[Union[str, bytes, PathLike]]' = None,
            name: 'Optional[str]' = None,
            node: 'Optional[Node]' = None, **kwargs
    ) -> None:
        super(ExternalComponent, self).__init__(name, node, **kwargs)
        self.path_to_exec: 'Optional[Union[str, bytes, PathLike]]' = path_to_exec
