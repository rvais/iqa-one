from abc import ABC

from iqa.components.abstract.component import Component
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional
    from iqa.system.node.base.node import Node


class InternalComponent(Component, ABC):
    """
    Class that represents abstract of component internal to IQA (i.e. it is handled and processed by IQA code base).
    For example it can be some sort of configuration management client or direct HTTP request. Doesn't need any kind
    of node per se, but we need to adhere to API.
    """

    def __init__(self, name: 'Optional[str]' = None, node: 'Optional[Node]' = None, **kwargs) -> None:
        super(InternalComponent, self).__init__(name, node, **kwargs)
